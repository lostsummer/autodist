#! /usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import os
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import Cfg
import PackProducer
import SetEncoding

cfg = Cfg.Cfg()
cfg.read()
cfg.printSourceInfo()
yesorno = ''
while yesorno.strip().upper() != 'Y' and yesorno.strip().upper() != 'N':
    print('\n继续？Y/N')
    yesorno = sys.stdin.readline()
    if yesorno.strip().upper() == 'N':
        exit()

packProducer = PackProducer.PackProducer(cfg)
packProducer.pullPack()
