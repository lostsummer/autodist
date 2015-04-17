#!/bin/bash

# 一次性无人值守获取4个最新底层安装包的脚步
# 10.10.10.133， 10.10.10.134 分别是本人在vmware 上跑的Debian5和Debian7编译环境
# 2200 和 8900 是包大小

rm ./application/install*.tgz
rm ./application/update*.bin

cd script
gp()
{
h="host=10.10.10.$1"
p="pack=$2"
sed -i "2 c$h" autodist.cfg 
sed -i "8 c$p" autodist.cfg 
expect <<!
set timeout 120
spawn ./getpack.py
expect "Y/N"
send "Y\r"
expect "$ "
!
}

gp 133 2200
gp 133 8900
gp 134 2200
gp 134 8900

