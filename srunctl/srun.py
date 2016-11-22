#!/usr/bin/env python
# encoding = utf-8
import sys
import configparser
import hashlib
import os
from time import sleep
from urllib import request, parse, error
import re
from collections import OrderedDict


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Srun:
    parser = configparser.ConfigParser()
    host = 'http://192.0.0.6'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
        'Accept': '*/*',
        'Origin': 'http://192.0.0.6',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'Referer': 'http://192.0.0.6/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive'
    }
    external_params = {
        'drop': 0,
        'type': 1,
        'n': 1
    }

    def __init__(self, path=None, section=None):
        self.path = os.path.expanduser(path or '~/.srunrc.ini')
        self.section = section or 'DEFAULT'
        self.data = self.get_config()
        self.data.update(self.external_params)

    def get_config(self):
        if not os.path.exists(self.path):
            raise 'config file is not founded in path: ' + self.path
        self.parser.read(self.path, encoding='utf-8')
        config = self.parser[self.section]
        return OrderedDict([
            ('username', config['username']),
            ('password', config['password'])
        ])

    def show(self):
        self.out('current user: %s, id: %s' % (self.section, self.data['username']))

    def login(self):
        self.out('开始登录')
        url = parse.urljoin(self.host, '/cgi-bin/do_login').rstrip('/')
        data = self.data.copy()
        data['password'] = hashlib.md5(str(data['password']).encode('utf-8')).hexdigest()[8:24]
        body = bytes(parse.urlencode(data), encoding='utf-8')
        req = request.Request(url, body, self.headers, method='GET')
        try:
            msg = request.urlopen(req).read().decode('utf-8')
            # if login succeeded the response message is a digital string
            msg = 'login_ok' if re.fullmatch(r'\d+', msg) else msg
        except error.URLError:
            msg = 'network_error'

        self.out(msg, 'SUCCESS' if msg == 'login_ok' else 'ERROR')
        return msg

    def logout(self):
        self.out('开始注销')
        url = parse.urljoin(self.host, 'cgi-bin/force_logout').rstrip('/')
        body = bytes(parse.urlencode(self.data), encoding='utf-8')
        req = request.Request(url, body, self.headers, method='POST')
        try:
            msg = request.urlopen(req).read().decode('utf-8')
        except error.URLError:
            msg = 'network_error'

        self.out(msg, 'SUCCESS' if msg == 'logout_ok' else 'ERROR')
        return msg

    def auto_login(self):
        while self.login() == 'online_num_error':
            self.out('等待60s重试登录')
            self.draw_progress(60)
    @staticmethod
    def draw_progress(total):
        for i in range(0, total + 1):
            bar = '=' * i + '-' * (total - i)
            end = '\r' if i < total else '\n'
            sys.stdout.write(('[%s] current: %2ds | total: %ds' + end) % (bar, i, total))
            sys.stdout.flush()
            sleep(1)

    def out(self, text='', tag='INFO'):
        colors = {
            'INFO': Color.BLUE,
            'ERROR': Color.RED,
            'SUCCESS': Color.GREEN,
            'DEFAULT': Color.CYAN
        }
        print('[\033[1m%(color)s%(tag)s\033[0m\033[0m]%(blank)s %(message)s' % {
            'color': colors.get(tag, 'DEFAULT'),
            'tag': tag,
            'blank': ' ' * (7 - len(tag)),
            'message': self.map.get(text, text)
        })

    map = {
        'user_tab_error': '认证程序未启动',
        'username_error': '用户名错误',
        'non_auth_error': '您无须认证，可直接上网',
        'password_error': '密码错误',
        'status_error': '用户已欠费，请尽快充值。',
        'available_error': '用户已禁用',
        'ip_exist_error': '该网络已被其他帐号登录',
        'usernum_error': '用户数已达上限',
        'mode_error': '系统已禁止WEB方式登录，请使用客户端',
        'time_policy_error': '当前时段不允许连接',
        'flux_error': '您的流量已超支',
        'minutes_error': '您的时长已超支',
        'ip_error': '您的IP地址不合法',
        'mac_error': '您的MAC地址不合法',
        'sync_error': '您的资料已修改，正在等待同步，请2分钟后再试。',
        'logout_error': '您不在线上',
        'lack_user_info': '缺少用户信息',
        'login_ok': '登陆成功',
        'online_num_error': '登录人数超过限额',
        'logout_ok': '注销成功',
        'network_error': '网络无连接'
    }

