#! /usr/bin/env python
# -*- coding: utf-8 -*-

from st2tests.base import BaseActionTestCase
from mock import MagicMock, patch
import json
import yaml
import os
import sys
import re

BASE_DIR = '/opt/stackstorm/packs/mydemo_pack'
sys.path.append(BASE_DIR)
sys.path.append(BASE_DIR + '/actions/scripts')
sys.path.append('/opt/stackstorm/virtualenvs/mydemo_pack/lib/python2.7/site-packages')
sys.path.append('/opt/stackstorm/st2/lib/python2.7/site-packages')

input_file = "rebuild_app.yaml"
res_file = BASE_DIR + "/tests/rebuild_app/response.yaml"

from rebuild_app import RebuildAppAction

class TestRebuildAppAction(BaseActionTestCase):

    action_cls = RebuildAppAction
    class_common = "common_mydemo.Common"
    method_execute = class_common + ".execute_command"

    def test00_no_mock_st2(self):
        input = yaml.load(
            self.get_fixture_content(input_file), Loader=yaml.FullLoader
        )

        action = self.get_action_instance()
        result = action.run(**input)
        print('result: {r}'.format(r=result))

        #self.assertEquals(len(reuslt), 6)
        self.assertEqual(result["bool"], True)
    
    @patch(method_execute)
    def test01_mock_st2(self, execute):
        input = yaml.load(
            self.get_fixture_content(input_file), Loader=yaml.FullLoader
        )

        def _execute_command(_cmd):
            _bool = False
            stdout = []
            stderr = []
            _res = yaml.load(open(res_file), Loader=yaml.FullLoader)

            if 'ls' in _cmd and 'grep' in _cmd:
                _bool = True
                _stdout = _res["succeeded"]["ls"]["stdout"]
                _stderr = _res["succeeded"]["ls"]["stderr"]


            elif 'stop' in _cmd and 'rm' in _cmd:
                _bool = True
                _stderr = _res["succeeded"]["rm"]["stderr"]
                if _execute.call_count == 2:
                    _stdout = _res["succeeded"]["rm"]["former"]["stdout"]
                elif _execute.call_count == 3:
                    _stdout = _res["succeeded"]["rm"]["latter"]["stdout"]
                else:
                    _bool = False
                    raise Error("docker_container_rm_err")


            elif '--build' in _cmd:
                _bool = True
                _stdout = _res["succeeded"]["build"]["stdout"]
                _stderr = _res["succeeded"]["build"]["stderr"]
            
            else:
                raise Error("_excute_command_err")


            return _bool, _stdout, _stderr

        execute.side_effect = _execute_command

        action = self.get_action_instance()
        result = action.run(**input)
        print('result: {r}'.format(r=result))

        self.assertEquals(len(result), 4)
        self.assertEqual(result["bool"], True)



