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
    
    def _git_fetch(dir):
        return "cd {dir} && sudo git fetch -p".format(
            dir=dir
        )
    
    def _git_checkout(branch):
        return "sudo git checkout -q {branch}"
    

    def _set_regex(self, branch, expected):
        if expected == "up_to_date":
            return "grep - E '(Your)\s+(branch)\s+(is)\s+(up-to-date)\s+(with)\s+('origin\/{branch}')' | awk '{print $6}'".format(
                branch=branch
            )
        elif expected == "not_up_to_date"::
            return "grep -E '(Your)\s+(branch)\s+(is)\s+(behind)\s+('origin\/{branch}')' | awk '{print $5}'".format(
                branch=branch
            )

    def set_command(self, dir, branch, expected):
        return (
            self._git_fetch(dir) + " && " + self._git_checkout(branch) + " && sudo git status | " + self._set_regex(branch, expected)
        )
    

    def check_stdout(self, branch, stdout):
        success = False
        for line in stdout:
            if not success and re.search(r'\s*' + re.escape(branch) + '\s*'):
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
        commands = []
        stdout = []
        stderr = []

        try:
            command = self.set_command(working_dir, branch, expected)
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
