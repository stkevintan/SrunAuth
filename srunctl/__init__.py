# encoding = utf-8

from .srun import Srun
import argparse


def get_args():
    desc = 'SRUN3000 校园网登录脚本'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('action',
                        nargs='?',
                        metavar='Action',
                        default='auto-login',
                        help='脚本要执行的操作，包括: login,logout,auto-login(default)')

    parser.add_argument('--user', '-u',
                        nargs='?',
                        help='指定配置文件中的特定用户信息，默认：DEFAULT')

    parser.add_argument('--path', '-p',
                        nargs='?',
                        help='指定配置文件路径，默认：~/.srunrc.ini')
    return parser.parse_args()


def main():
    args = get_args()
    srun = Srun(args.path, args.user)
    if args.action == 'auto-login':
        srun.auto_login()
    elif args.action == 'login':
        srun.login()
    elif args.action == 'logout':
        srun.logout()
    elif args.action == 'show':
        srun.show()
