#! /usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import os
import getopt
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import Cfg
import PackUpdater
import SetEncoding

def usage():
	print("useage:")
	print("\tdist.py(exe) -c(--update-c)")
	print("\tdist.py(exe) -j(--update-java)")
	print("\tdist.py(exe) -a(--update-all)")
	print("\tdist.py(exe) -r(--update-authorize)")

try:
	opts, args = getopt.getopt(sys.argv[1:], "cjar", ["update-c", "update-java", "update-all", "update-authorize"])
except getopt.GetoptError:
	usage()
	sys.exit(2)

cfg = Cfg.Cfg()
cfg.read()
cfg.printDistInfo()
yesorno = ''
while yesorno.strip().upper() != 'Y' and yesorno.strip().upper() != 'N':
    print('\n继续？Y/N')
    yesorno = sys.stdin.readline()
    if yesorno.strip().upper() == 'N':
        exit()

packUpdater = PackUpdater.PackUpdater(cfg)

for opt, arg in opts:
	if opt in ("-c", "--update-c"):
		packUpdater.updateC()
		break
	if opt in ("-j", "--update-java"):
		packUpdater.updateTomcat()
		break
	if opt in ("-a", "--update-all"):
		packUpdater.updateC()
		packUpdater.updateTomcat()
		break
	if opt in ("-r", "--update-authorize"):
		packUpdater.updateAuth()
		break

if len(opts) == 0:
	packUpdater.updateC()


