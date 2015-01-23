#! /usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import paramiko
import os


class SSHClient:
    def __init__(self):
        self.cl = paramiko.SSHClient()

    def connect(self, ip, port, user, passwd):
        print('ssh 连接 host: ' + ip)
        self.cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.cl.connect(ip, port, user, passwd)
        print('ssh 连接成功')

    def exeCmd(self, cmd):
        print('在远程主机上执行命令：' + cmd)
        stdin, stdout, stderr = self.cl.exec_command(cmd)
        retstr = stdout.read()
        print retstr
        return retstr

    def getSftpCl(self):
        return self.cl.open_sftp()

    def close(self):
        self.cl.close()

