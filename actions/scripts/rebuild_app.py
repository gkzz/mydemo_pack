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

    def set_command(self, dir, ptns):
        return (
            "cd {dir} && sudo docker container ls grep -E '{former}|{latter}'".format(
                dir=dir,
                former=ptn[0],
                latter=ptn[1]
            )
        )
    
    def _set_regex(self, ptns):
        redict = {
            'former': re.compile(
                #  0                  1
                r'([\d+|\D+]+)\s+(' + re.escape(ptns[0]) + ')'
            ),
            'latter': re.compile(
                #  0                  1
                #r'([\d+|\D+]+)\s+(' + re.escape(ptns[1])
                r'([\d+|\D+]+)\s+(' + re.escape(ptns[1]) + ')'
            ),
        }
        return redict
    
    def get_regex(array, redict):
        found = []
        success = False
        for line in array:
            m = redict['former'].search(line) or redict['latter'].search(line)
            if m:
                found.append(m.group(0))
        
        if len(found) == 2:
            success = True
        
        return success, found

    
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
       

    def write_result(self, cmds, bool, stdout, stderr):
        self.result.update({
            "command": self._to_str(cmds),
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
        commands = ''

        try:
            ls_command = self.set_command(working_dir, ptn)
            bool, stdout, stderr = self.common.execute_command(ls_command)
            if not bool:
                pass
            else:
                commands, bool, stdout, stderr = self.rebuild(stdout)
                self.result = self.write_result(commands, bool, stdout, stderr)
        except:
            stderr = traceback.format_exc()

        finally:
            self.result = self.write_result(commands, bool, stdout, stderr)
        
        return self.result
