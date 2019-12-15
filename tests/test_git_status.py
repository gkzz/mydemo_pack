from st2tests.base import BaseActionTestCase
from mock import MagicMock, patch
import json
import yaml
import os
import sys
import re
sys.path.append('/opt/stackstorm/packs/mydemo_pack/actions/scripts')
sys.path.append('/opt/stackstorm/virtualenvs/mydemo_pack/lib/python2.7/site-packages')
sys.path.append('/opt/stackstorm/st2/lib/python2.7/site-packages')


BASE_DIR = "/opt/stackstorm/packs/mydemo_pack"
sys.path.append(BASE_DIR)

input_file = "git_status.yaml"

from git_status import GitStatusAction

class TestGitStatusAction(BaseActionTestCase):

    action_cls = GitStatusAction

    def test00_no_mock_st2(self):
        input = yaml.load(self.get_fixture_content(input_file))

        action = self.get_action_instance()
        output = action.run(**input)
        print('output: {output}'.format(output=output))

        self.assertEquals(len(output), 1)
        result = output[0]
        self.assertEqual(result["bool"], True)
    
    @patch("common_mydemo.Common.execute_command")
    def test00_mock_st2(self, execute):
        input = yaml.load(self.get_fixture_content(input_file))
        #input.update({
        #    "key": value,
        #})

        def _execute_command():
            bool = True
            stdout = ["Your branch is up-to-date with 'origin/devel-views"]
            stderr = [""]

            return boolm stdout, stderr

        execute.side_effect = _execute_command

        action = self.get_action_instance()
        results = action.run(**input)

        print('results: {}'.format(results))

        self.assertEquals(len(output), 1)
        result = output[0]
        self.assertEqual(result["bool"], True)


