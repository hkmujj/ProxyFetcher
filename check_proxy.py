# coding:utf-8
"""检查代理的一些操作

1: socket 去ping 一个代理
2: 用代理去访问一个网站,看能否访问
"""

import socket

import requests

from configs.logger_config import get_logger
from configs.user_agent_config import get_user_agent

logger = get_logger(__name__)  # 日志配置
# 构造代理格式化字符串
http_proxy_format = 'http://{0}:{1}'
https_proxy_format = 'https://{0}:{1}'


def ping(host='127.0.0.1', port=8000, timeout=3):
    """ ping 一个ip
    :param host: 代理ip
    :param port:  代理端口(int 类型)
    :param timeout: 超时时间
    :return:
    """

    try:
        socket.setdefaulttimeout(timeout)
        # 代理和端口元组中,端口是int类型的,不是str
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
            (host, int(port)))
        logger.info('[检测代理] ping验证通过; 代理: %s port: %s 验证通过;', host, port)
        return True
    except Exception as e:
        print(e)
        logger.error('[检测代理] ping超时; 代理: %s port: %s ;', host, port)
        return False


def check_visit_website(ip_info, website):
    """
    用代理去访问网站
    :param ip_info: class:`ProxyItem` object
    :param website:  网站host; 比如'douban.com'
    :return:
    """

    url = website
    if not website.startswith('http'):
        url = 'http://' + website
    # if not isinstance(ip_info, ProxyItem):
    #     raise Exception
    proxy_type = ip_info['proxy_type']
    proxies = {}
    if proxy_type == 'HTTP':
        proxies['http'] = http_proxy_format.format(ip_info['ip'],
                                                   ip_info['port'])
    elif proxy_type == 'HTTPS':
        proxies['https'] = https_proxy_format.format(ip_info['ip'],
                                                     ip_info['port'])
    elif proxy_type == 'SOCKS4/5':
        pass
    else:
        logger.error('[检测代理] 暂不支持此种类型代理; 代理类型: %s, 代理信息:%s',
                     proxy_type, ip_info)
        raise Exception
    try:
        user_agent = get_user_agent()
        res = requests.get(url=url, proxies=proxies, headers={
            'User-Agent': user_agent}, timeout=10)
        status_code = res.status_code
        if status_code < 200 or status_code >= 400:
            logger.error('[检测代理] 用代理:%s 访问网站:%s 失败, 状态码:%s',
                         proxies, url, status_code)
            return False
        logger.info('[检测代理] 用代理:%s 访问网站:%s 成功, 状态码:%s',
                    proxies, url, status_code)
        return True
    except requests.exceptions.RequestException as e:
        print(e)
        logger.error('[检测代理] 用代理:%s 访问网站:%s 异常', proxies, url)
        return False
