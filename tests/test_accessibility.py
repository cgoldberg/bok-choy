"""
Test accessibility reporting.
"""
import json
import requests

from bok_choy.web_app_test import WebAppTest
from .pages import VisiblePage

class AccessibilityTest(WebAppTest):
    """
    Test element visibility.
    """
    def setUp(self):
        super(AccessibilityTest, self).setUp()

    def test_visible(self):
        # (Pdb) self.browser.service.service_url
        # 'http://localhost:33225/wd/hub'
        # figure out what session
        # see https://groups.google.com/forum/#!topic/phantomjs/tW2p3dlJ9Gw
        self.page = VisiblePage(self.browser).visit()
        ghostdriver_url = self.browser.service.service_url
        resp = requests.get('{}/sessions'.format(ghostdriver_url))
        sessions = resp.json()
        value = sessions.get('value')
        session_id = value[0].get('id')
        print session_id

        # OK this works
        resp = requests.get('{}/session/{}/title'.format(ghostdriver_url, session_id))
        print resp.text

        # this works too
        resp = requests.get('{}/session/{}/url'.format(ghostdriver_url, session_id))
        print resp.text

        # payload = {"url": "http://localhost:8003/selector.html"}
        # resp = requests.post('{}/session/{}/url'.format(ghostdriver_url, session_id), data=json.dumps(payload))
        # print resp.text

        payload = {"script": "return arguments[0] + arguments[0]", "args": [1]}
        resp = requests.post('{}/session/{}/phantom/execute'.format(ghostdriver_url, session_id), data=json.dumps(payload))
        print resp.text

        self.assertEqual(2, resp.json().get('value'))
        # from nose.tools import set_trace; set_trace()


        self.assertTrue(self.page.is_visible('superman'))
