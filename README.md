# autodist

exe程序的目录结构是 ：  
 >     autodist─┬─application───maketgz.bat
             └─   tools   ─┬─autodist.cfg
                           ├─dist.exe
                           └─getpack.exe

python脚本的目录结构是：
>     autodist─┬─application───maketgz.bat
             └─   script  ─┬─autodist.cfg
                           ├─dist.py
                           ├─getpack.py
                           └─*.py (其他py文件，非入口)

二者用法相同，getpack.exe(py) 从远程编译机执行 svn 更新代码和编译代码的命令，并待编译完成后将最新底层tgz安装包，bin 升级包， 授权程序 scp 到本地 application 目录中；dist.exe(py) 可以将 application 中的底层安装包上传到待部署目标机并执行安装。

配置文件 autodis.cfg ：

    [source]
    host=10.10.10.134

    # 需要以/结尾 
    dir=/usr/local/src/cplusplus/c/

    # 定义包大小
    pack=2200        

    [dist]
    host=10.10.10.129

    # 是否需要重新授权
    need_auth=1

    # 0: 虚拟机或阵列虚拟磁盘； 1：物理磁盘
    disk_type=0  

    # 虚拟机网卡数
    nic_cnt=2

其中 [source] 标签下为编译机的相关配置，[dist] 标签下为部署目标机的相关配置。
