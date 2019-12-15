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

input_file = "git_status.yaml"
resp_file = BASE_DIR + "/tests/git_status/response.yaml"

from git_status import GitStatusAction

class TestGitStatusAction(BaseActionTestCase):

    action_cls = GitStatusAction

    def test00_no_mock_st2(self):
        input = yaml.load(
            self.get_fixture_content(input_file), Loader=yaml.FullLoader
        )

        action = self.get_action_instance()
        result = action.run(**input)
        print('result: {r}'.format(r=result))

        self.assertEquals(len(reuslt), 6)
        self.assertEqual(result["bool"], True)
    
    @patch("common_mydemo.Common.execute_command")
    def test01_mock_st2(self, execute):
        input = yaml.load(
            self.get_fixture_content(input_file), Loader=yaml.FullLoader
        )

        def _execute_command(_cmd):
            bool = True
            #stdout = ["Your branch is up-to-date with 'origin/devel-views'"]
            #stderr = [""]

            resp = yaml.load(open(resp_file), Loader=yaml.FullLoader)
            stdout = resp["succeeded"]["up_to_date"]["stdout"]
            stderr = resp["succeeded"]["up_to_date"]["stderr"]

            return bool, stdout, stderr

        execute.side_effect = _execute_command

        action = self.get_action_instance()
        result = action.run(**input)
        print('result: {r}'.format(r=result))

        self.assertEquals(len(reuslt), 6)
        self.assertEqual(result["bool"], True)


