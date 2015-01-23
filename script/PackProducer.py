#! /usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import paramiko
import re
import os
import Cfg
import SSHClient

class PackProducer:
    def __init__(self, cfg):
        self.ssh_cl = SSHClient.SSHClient()
        self.source_host = cfg.source_host
        self.source_dir = cfg.source_dir

    def connectSource(self, user='root', passwd='star777!@#$'):
        try:
            self.ssh_cl.connect(self.source_host, 22, user, passwd)
        except:
            print "ssh 连接远程主机失败"
            exit()

    def updateSVN(self):
        print('更新svn...')
        cmd = 'svn update ' + self.source_dir
        self.ssh_cl.exeCmd(cmd)

    def removeDiff(self):
        modified_files = []
        print('查询版本库状态')
        cmd = 'svn status ' + self.source_dir
        stdout = self.ssh_cl.exeCmd(cmd)
        modified_pattern = re.compile('^M')
        for line in stdout.split('\n'):
            match = modified_pattern.match(line)
            if match:
                file =  line.split()[1]
                modified_files.append(file)
                print('发现与版本库冲突文件：' + file)

        if len(modified_files) > 0:
            for file in modified_files:
                print('删除文件：' + file)
                cmd = 'rm ' + file
                ssh_cl.exeCmd(cmd)
        else:
            print('未发现版本库文件冲突')


    def compile(self):
        print('开始制作安装包，需要2~3分钟时间...')
        cmd = 'cd ' + self.source_dir + 'shell/;' + './createInstall.sh'
        self.ssh_cl.exeCmd(cmd)
        print('编译授权程序')
        cmd = 'cd ' + self.source_dir + 'authorize/;' + 'mkdir -p target;' + 'make'
        self.ssh_cl.exeCmd

    def transToLocal(self):
        application_dir = '../application/'  
        release_dir = os.path.join(self.source_dir, "release/")
        auth_dir = os.path.join(self.source_dir, "authorize/target/")
        print('远程安装包目录：' + release_dir)
        print('远程授权程序目录：' + auth_dir)
        print('本地目录：' + application_dir)
        if not os.path.exists(application_dir):
            os.makedirs(application_dir)

        sftp_cl = self.ssh_cl.getSftpCl()
        
        files = sftp_cl.listdir(release_dir)
        remote_path = ""
        local_path = ""
        bin_name_pattern = re.compile(r"^update\d+.+\.bin")
        tgz_name_pattern = re.compile(r"^installdir\-v\d+\-Debian\d\-pack\d+\.tgz")
        for f in files:
            if bin_name_pattern.match(f) or tgz_name_pattern.match(f):
                remote_path = os.path.join(release_dir, f)
                local_path = os.path.join(application_dir, f)               
                sftp_cl.get(remote_path, local_path)
                print('得到文件：' + local_path)

        files = sftp_cl.listdir(auth_dir)
        for f in files:
            if f == 'authorize':
                remote_path = os.path.join(auth_dir, f)
                local_path = os.path.join(application_dir, f)
                sftp_cl.get(remote_path, local_path)
                print('得到文件：' + local_path)
                break

        sftp_cl.close()

    def pullPack(self):
        self.connectSource()
        self.updateSVN()
        self.removeDiff()
        self.compile()
        self.transToLocal()
        print('传送结束')
