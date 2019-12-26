#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import traceback
from st2actions.runners.pythonrunner import Action

from common_mydemo import Common

class RebuildAppAction(Action):
    """Action class for st2"""

    def __init__(self, config):
        self.config = config
        self.result = {}
        for r in [
            "command", "branch", "bool", "stdout", "stderr"        
        ]:
            self.result[r] = None 

        self.common = Common()
        return

    def set_command(self, working_dir, ptn):
        return (
            "cd {dir} && sudo docker container ls grep -E '{ptn}' | awk '{print $1}'".format(
                dir=dir,
                ptn=ptn
            )
        )

    
    def rebuild(ids):
        bool = False
        cmds = []
        stdout = []
        stderr = []
        counter = 0
        for id in ids:
            cmd = "sudo docker container stop {id} && sudo docker container rm {id}".format(id=id)
            bool, res, err = self.common.execute_command(cmd)
            cmds.append(cmd) 
            stdout = stdout + res
            stderr = stderr + err
            if not bool:
                break
            else:
                counter += 1
        
        if len(ids) == 0 or counter == 2:
            cmd = "sudo docker-compose up -d --build"
            bool, res, err = self.common.execute_command(cmd)
            cmds.append(cmd) 
            stdout = stdout + res
            stderr = stderr + err
        
        return cmds, bool, stdout, stderr

    

    def _to_str(self, target):
        """ Convert $target to string """

        if type(target) == list:
           return '\n'.join(map(str, target))
        elif type(target) == str:
           return target
        else:
           return str(target)
       

    def write_result(self, command, branch, expected, bool, stdout, stderr):
        self.result.update({
            "command": command,
            "branch": branch,
            "expected": expected,
            "bool": bool,
            "stdout": self._to_str(stdout),
            "stderr": self._to_str(stderr),
        })

        return self.result
    

    def run(self, working_dir, ptn):
        """ Entrypoint for st2 """

        bool = False
        stdout = ''
        stderr = ''

        try:
            ls_command = self.set_command(working_dir, ptn)
            bool, stdout, stderr = self.common.execute_command(ls_command)
            if not bool:
                pass
            else:
                bool, stdout, stderr = self.rebuild(stdout)
                self.result = self.write_result(command, branch, expected, bool, stdout, stderr)
        except:
            stderr = traceback.format_exc()

        finally:
            self.result = self.write_result(command, branch, expected, bool, stdout, stderr)
        
        return self.result
