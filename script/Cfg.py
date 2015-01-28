# -*- coding: utf-8 -*-

import ConfigParser

class Cfg:
    def __init__(self, file_path = 'autodist.cfg'):
        self.cfg_file =     file_path
        self.source_host =  "10.10.10.134"
        self.source_dir =   "/usr/local/src/cplusplus/c/"
        self.source_pack = '2200'
        self.dist_host =    "10.10.10.18"
        self.dist_need_auth = "1"
        self.dist_disk_type = "1"
        self.dist_nic_cnt = "3"

    def read(self):
        try:
            cfg = ConfigParser.ConfigParser()
            cfg.read(self.cfg_file)
            self.source_host =      cfg.get('source', 'host')
            self.source_dir =       cfg.get('source', 'dir')
            self.source_pack =      cfg.get('source', 'pack')           
            
            if int(self.source_pack) < 1500:
                self.source_pack = '1500'
            elif int(self.source_pack) > 8900:
                self.source_pack = '8900'

            self.dist_host =        cfg.get('dist', 'host')
            self.dist_need_auth =   cfg.get('dist', 'need_auth')
            self.dist_disk_type =   cfg.get('dist', 'disk_type')
            self.dist_nic_cnt =     cfg.get('dist', 'nic_cnt')

        except:
            print('读取配置文件时发生异常\n')

    def printSourceInfo(self):
        print("%32s : %16s" %('编译机地址',         self.source_host))     
        print("%32s : %16s" %('编译机代码目录',     self.source_dir))
        print("%32s : %16s" %('pack size',          self.source_pack))
        
    def printDistInfo(self):
        print("%32s : %16s" %('目标机地址',         self.dist_host))
        print("%32s : %16s" %('是否需要授权（0：否/1：是）',         self.dist_need_auth))
        print("%32s : %16s" %('磁盘模式（0：虚拟/1：实体）',         self.dist_disk_type))
        print("%32s : %16s" %('虚拟网络接口数量',   self.dist_nic_cnt))

    def write(self):
        cfg = ConfigParser.ConfigParser()
        sec_source = 'source'
        cfg.add_section(sec_source)
        cfg.set(sec_source, 'host', self.source_host)
        cfg.set(sec_source, 'dir', self.source_dir)
        sec_dist = 'dist'
        cfg.add_section(sec_dist)
        cfg.set(sec_dist, 'host', self.dist_host)
        cfg.set(sec_dist, 'need_auth', self.dist_need_auth)
        cfg.set(sec_dist, 'disk_type', self.dist_disk_type)
        cfg.set(sec_dist, 'nic_cnt', self.dist_nic_cnt)

        with open(self.cfg_file, 'wb') as cfg_file_obj:
            cfg.write(cfg_file_obj)


