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
    #    input = yaml.load(self.get_fixture_content(input_file))
    #    input.update({
    #        "expected_hour": 20,
    #    })
#
    #    action = self.get_action_instance()
    #    results = action.run(**input)
