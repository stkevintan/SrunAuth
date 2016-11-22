# SRUN3000 校园网登录脚本
---
## Description

可以为SRUN3000校园网实现自动登录，注销，多账户切换等功能。

## Requirement
`Python3` 
`setuptools`

## Installation
```shell
git clone https://github.com/stkevintan/srunctl.git
cd srunctl
python setup.py bdist
sudo python setup.py install
```
## Usage
创建 ``~/.srunrc.ini` 文件，并按照如下格式写入账户密码
```ini
[DEFAULT]
username : xxxx
password : xxxx 
[another account]
username: xxxx
password: xxxx
```

```shell
srunctl [auto-login] # 自动登录（如果碰到多用户在线自动注销再登录）
srunctl login # 登录
srunctl logout # 注销
srunctl show # 显示当前用户信息
srunctl -h # 帮助信息
```
