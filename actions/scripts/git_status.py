#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from st2actions.runners.pythonrunner import Action

from common_mydemo import Common

class GitStatusAction(Action):
    """Action class for st2"""

    def __init__(self, working_dir, branch, expected):
        self.output = []
        self.result = {}
        self.command = "cd {dir} && sudo git status".format(dir=working_dir)
        self.branch = branch
        self.expected = expected
        self.redict = {
            'up_to_date': re.compile(
                #   1       2          3      4              5        6
                "r(Your)\s+(branch)\s+(is)\s+(up-to-date)\s+(with)\s+('origin/" + re.escape(self.branch) + "')"
            ),
            'not_up_to_date': re.compile(
                "r(Your)\s+(branch)\s+(is)\s+(behind)\s+('origin/" + re.escape(self.branch) + "')"
            ),
        }
        for r in [
            "command", "branch", "expected", "bool", "stdout", "stderr"
        ]:
            self.result[r] = None 

        self.common = Common()


    
    def _set_regex(self):
        ptn = None
        if self.expected == "up_to_date":
            ptn = self.redict['up_to_date']
        elif self.expected == "not_up_to_date":
            ptn = self.redict['not_up_to_date']
        else:
            pass

        return ptn
    

    def check_stdout(self, stdout):
        success = False
        ptn = self._set_regex()
        for line in stdout:
            if not success and ptn.search(line):
                success = True
            else:
                pass

        if type(stdout) == list:
            stdout = ','.join(str_list)
        else:
            pass

        return success, stdout
    

    def write_result(self, bool, stdout, stderr):
        result.update({
            "command": self.command,
            "branch": self.branch,
            "expected": self.expected,
            "bool": self.bool,
            "stdout": stdout,
            "stderr": stderr,
        })

        return result
    

    def run(self, working_dir, branch, expected):
        """ Entrypoint for st2 """

        bool = False
        stdout = []
        stderr = []

        try:
            self.bool, stdout, stderr = self.common.execute_command(self.command)
            bool, stdout = self.check_stdout(stdout)
            self.output = self.write_result(bool, stdout, stderr)
        except:
            pass

        finally:
            self.result = self.write_result(bool, stdout, stderr)
        
        self.output.append(self.result)

        return self.output 










