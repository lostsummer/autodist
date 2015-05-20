#! /usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import paramiko
import re
import os
import Cfg
import SSHClient

class PackUpdater:
    def __init__(self, cfg):
        self.ssh_cl = SSHClient.SSHClient()
        self.host = cfg.dist_host
        self.debian_version = "7"
        self.need_auth = cfg.dist_need_auth
        self.disk_type  = cfg.dist_disk_type
        self.nic_cnt = cfg.dist_nic_cnt
        self.source_pack = cfg.source_pack
        self.application_dir = '../application/'
        self.c_tmp_dir = '/dev/shm/'
        self.webapps_dir = '/usr/share/tomcat6/webapps/'
        self.tgzfile = 'MyAudit.tgz'

    def connectDist(self, user='root', passwd='star777!@#$'):
        try:
            print("连接目标主机")
            self.ssh_cl.connect(self.host, 22, user, passwd)
        except:
            print "ssh 建立连接失败"
            exit()

        try:
            cmd = 'lsb_release -a |grep Release | tr : " " | awk \'{printf "%d\\n",$2}\''
            self.debian_version = self.ssh_cl.exeCmd(cmd).strip()
        except:
            print "ssh 获取系统版本失败"
            exit()

        print('Debian 版本：' + self.debian_version)

    def closeSSH(self):
        self.ssh_cl.close()
        print "断开 ssh 连接"

    def getNewestPack(self):
        tar_name = ''
        files = os.listdir(self.application_dir)
        tar_name_pattern = re.compile('installdir\-v\d{8}\-Debian' 
                + self.debian_version 
                + '\-pack' 
                + self.source_pack 
                + '\.tgz')

        for f in files:
            if tar_name_pattern.match(f) and cmp(f, tar_name) > 0:
                tar_name = f

        return tar_name

    def uploadAuth(self):
    	auth_local_path = self.application_dir + 'authorize'
        auth_dist_path = self.c_tmp_dir + 'authorize'
        print('上传授权程序...')
        sftp_cl = self.ssh_cl.getSftpCl()
        sftp_cl.put(auth_local_path, auth_dist_path)
        sftp_cl.close()

    def genAuthXml(self):
    	if self.disk_type == '0':
            cmd = 'cd ' + self.c_tmp_dir + ' && chmod u+x authorize && ./authorize -d 0 -n ' + self.nic_cnt + ' && cp auth.xml /usr/local/myaudit/config/'
        else:
            cmd = 'cd ' + self.c_tmp_dir + ' && chmod u+x authorize && ./authorize && cp auth.xml /usr/local/myaudit/config'
        self.ssh_cl.exeCmd(cmd)

    def restartC(self):
    	cmd = '/etc/init.d/startmyaudit.sh restart'
    	self.ssh_cl.exeCmd(cmd)

    def uploadC(self):
        auth_local_path = self.application_dir + 'authorize'
        auth_dist_path = self.c_tmp_dir + 'authorize'
        tarName = self.getNewestPack()
        if tarName == "":
            print "没有发现合适安装包"
            exit()
        print('使用安装包：' + tarName)
        install_local_path = self.application_dir + tarName
        install_dist_path = self.c_tmp_dir + 'installdir.tgz'
        print('上传安装包和授权程序...')
        sftp_cl = self.ssh_cl.getSftpCl()
        sftp_cl.put(auth_local_path, auth_dist_path)
        sftp_cl.put(install_local_path, install_dist_path)
        sftp_cl.close()

    def installC(self):      
        if self.need_auth == '1':
            if self.disk_type == '0':
                cmd = 'cd ' + self.c_tmp_dir + ' && chmod u+x authorize && ./authorize -d 0 -n ' + self.nic_cnt + ' && cp auth.xml /usr/local/myaudit/config/'
            else:
                cmd = 'cd ' + self.c_tmp_dir + ' && chmod u+x authorize && ./authorize && cp auth.xml /usr/local/myaudit/config'
            self.ssh_cl.exeCmd(cmd)
        cmd = 'cd /dev/shm && tar xvzf installdir.tgz && cd installdir && ./installmyaudit.sh'
        self.ssh_cl.exeCmd(cmd)

    def uploadJava(self):
        java_local_path = self.application_dir + self.tgzfile
        java_dist_path = self.webapps_dir + self.tgzfile
        if not os.path.exists(java_local_path):       
            print "没有发现Java程序包" + self.tgzfile
            exit()
        print('上传安Java程序包...')
        sftp_cl = self.ssh_cl.getSftpCl()
        sftp_cl.put(java_local_path, java_dist_path)
        sftp_cl.close()

    def installJava(self):
        cmd = 'cd ' + self.webapps_dir + ' && mv MyAudit MyAudit_bak && tar xvzf ' + self.tgzfile
        self.ssh_cl.exeCmd(cmd)

    def updateC(self):
        self.connectDist()
        self.uploadC()
        self.installC()
        self.closeSSH()
        print('MyAudit 底层程序已更新')

    def updateAuth(self):
    	self.connectDist()
    	self.uploadAuth()
    	self.genAuthXml()
    	self.restartC()
    	self.closeSSH()

    def updateTomcat(self):
        self.connectDist('root')
        if self.debian_version == '7':
            stopcmd = '/etc/init.d/tomcat6 stop'
            tomcatuser = 'tomcat6'
            self.webapps_dir = '/usr/share/tomcat6/webapps/'
        else:
            stopcmd = '/etc/init.d/tomcat5.5 stop'
            tomcatuser = 'tomcat55'
            self.webapps_dir = '/usr/share/tomcat5.5/webapps'
        self.ssh_cl.exeCmd(stopcmd)
        self.closeSSH()

        self.connectDist(tomcatuser)
        self.uploadJava()
        self.installJava()
        self.closeSSH()
        print('MyAudit Tomcat 程序已更新，请手动重启服务，确认无错误再手动删除MyAudit_bak目录')

