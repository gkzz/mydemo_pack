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
            "command", "bool", "stdout", "stderr"        
        ]:
            self.result[r] = None 

        self.common = Common()
        return

    def set_command(self, dir, ptns=None, id=None):
        try:
            if ptns is None and id is None:
                return (
                    "cd {dir} && sudo docker-compose up -d --build".format(
                        dir=dir
                    )
                )
            elif ptns is not None and id is None:
                return (
                    "cd {dir} && sudo docker container ls | grep -E '{former}|{latter}'".format(
                        dir=dir,
                        former=ptns[0],
                        latter=ptns[1]
                    )
                )
            elif ptns is None and id is not None:
                return (
                    "cd {dir} && sudo docker container stop {id} && sudo docker container rm {id}".format(
                        dir=dir,
                        id=id
                    )
                )
            else:
                raise ArgumentError("""
                   The following arguments are unexpected
                   {dir}, {ptns}, {id}
                """.format(dir=dir, ptns=ptns, id=id))

        except ArgumentError as ae:
            return traceback.format_exc()


    
    def _set_regex(self, ptns):
        redict = {
            #'former': re.compile(
            #    #  0                  1
            #    r'([\d+|\D+]+)\s+(' + re.escape(ptns[0]) + ')'
            #),
            #'latter': re.compile(
            #    #  0                  1
            #    #r'([\d+|\D+]+)\s+(' + re.escape(ptns[1])
            #    r'([\d+|\D+]+)\s+(' + re.escape(ptns[1]) + ')'
            #),
            'target': re.compile(
                r'(\S+)\s+(' + re.escape(ptns[0]) + '|'   + re.escape(ptns[1]) +  ')'
            )
        }
        return redict
    
    def get_regex(self, array, ptns):
        found = []
        redict = self._set_regex(ptns)
        for line in array:
            m =  redict['target'].search(line)
            if m:
                found.append(m.group(1))
        
        return found

    
    def rebuild(self, dir, ids):
        bool = False
        cmds = []
        stdout = []
        stderr = []
        counter = 0
        for id in ids:
            # "cd {dir} && sudo docker container stop {id} && sudo docker container rm {id}"
            cmd = self.set_command(dir=dir, id=id)
            bool, res, err = self.common.execute_command(cmd)
            cmds.append(cmd) 
            stdout += res
            stderr += err
            if bool:
                counter += 1
            else:
                break
                
        
        if len(ids) == 0 or counter == 2:
            # "cd {dir} && sudo docker-compose up -d --build"
            cmd = self.set_command(dir=dir)
            bool, res, err = self.common.execute_command(cmd)
            cmds.append(cmd) 
            stdout += res
            stderr += err
        
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
            "bool": bool,
            "command": self._to_str(cmds),
            "stdout": self._to_str(stdout),
            "stderr": self._to_str(stderr),
        })

        return self.result
    

    def run(self, working_dir, ptns):
        """ Entrypoint for st2 """

        bool = False
        stdout = []
        stderr = []
        commands = []

        try:
            # "cd {dir} && sudo docker container ls grep -E '{former}|{latter}'"
            ls_command = self.set_command(dir=working_dir, ptns=ptns)
            bool, stdout, stderr = self.common.execute_command(ls_command)
            if bool:
                ids = self.get_regex(stdout, ptns)
                commands, bool, stdout, stderr = self.rebuild(working_dir, ids)
                commands.insert(0, ls_command)
                self.result = self.write_result(commands, bool, stdout, stderr)
            else:
                self.result = self.write_result(ls_command, bool, stdout, stderr)

        except:
            stderr = traceback.format_exc()
            self.result = self.write_result('', bool, stdout, stderr)

        #finally:
        #    self.result = self.write_result(commands, bool, stdout, stderr)
            
        
        return self.result
