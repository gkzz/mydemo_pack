#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
from subprocess import Popen, PIPE


class Common:
    """ Common for mydemo """
    
    def __init__(self):
        pass
    
    def execute_command(self, command):
        bool = False
        try:
            stdout, stderr = Popen(
                command, shell=True, stdout=PIPE, stderr=PIPE
            ).communicate()
            stdout = stdout.splitlines()
            stderr = stderr.splitlines()
            bool = True
        except:
            stdout = None
            stderr = traceback.format_exc()
                
        return bool, stdout, stderr