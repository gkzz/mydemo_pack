#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import traceback
from st2actions.runners.pythonrunner import Action

from common_mydemo import Common

class GitStatusAction(Action):
    """Action class for st2"""

    def __init__(self, config):
        self.config = config
        self.result = {}
        for r in [
            "command", "branch", "expected", "bool", "stdout", "stderr"        
        ]:
            self.result[r] = None 

        self.common = Common()
        return

    def set_command(self, dir):
      return "cd {dir} && sudo git status".format(dir=dir)

    def _set_regex(self, branch, expected):
        redict = {
            'up_to_date': re.compile(
                #   1       2          3      4              5        6
                r"(Your)\s+(branch)\s+(is)\s+(up-to-date)\s+(with)\s+('origin\/"+ re.escape(branch)  +"')"
            ),
            'not_up_to_date': re.compile(
                r"(Your)\s+(branch)\s+(is)\s+(behind)\s+('origin\/"+ re.escape(branch)  +"')"
            ),
        }

        ptn = None
        if expected == "up_to_date":
            ptn = redict['up_to_date']
        elif expected == "not_up_to_date":
            ptn = redict['not_up_to_date']
        else:
            pass

        return ptn
    

    def check_stdout(self, branch, expected, stdout):
        success = False
        ptn = self._set_regex(branch, expected)
        for line in stdout:
            if not success and ptn.search(line):
                success = True
            else:
                pass

        return success, stdout
    

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
    

    def run(self, working_dir, branch, expected):
        """ Entrypoint for st2 """

        bool = False
        stdout = ''
        stderr = ''

        try:
            command = self.set_command(working_dir)
            bool, stdout, stderr = self.common.execute_command(command)
            if not bool:
                pass
            else:
                bool, stdout = self.check_stdout(branch, expected, stdout)
                self.result = self.write_result(command, branch, expected, bool, stdout, stderr)
        except:
            stderr = traceback.format_exc()

        finally:
            self.result = self.write_result(command, branch, expected, bool, stdout, stderr)
        
        return self.result
