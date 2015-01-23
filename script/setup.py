#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import sys

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")
  
options = {"py2exe":   
            {   "compressed": 1,   
                "optimize": 2,
                "bundle_files": 1,
                "includes" : "paramiko",
                "optimize": 1
            }   
          }   

script = ["getpack.py", "dist.py"]

setup(      
    version = "0.1.0",   
    description = "Auto compile and dist myaudit c part.",   
    name = "Auto Dist",   
    options = options,   
    zipfile=None,   
    console=script  
    )   
