"""
Test accessibility reporting.
"""
import json
import requests
from textwrap import dedent

from bok_choy.web_app_test import WebAppTest
from .pages import VisiblePage

AXS_URL = "https://raw.githubusercontent.com/GoogleChrome/accessibility-developer-tools/stable/dist/js/axs_testing.js"
AXS_FILE = 'tests/axs_testing.js'

class AccessibilityTest(WebAppTest):
    """
    Test element visibility.
    """
    def setUp(self):
        super(AccessibilityTest, self).setUp()
        self.page = VisiblePage(self.browser).visit()

    def test_phantom_execute(self):
        # Get the session_id from ghostdriver so that we can inject JS into the page
        # The ghostdriver URL will be something like this: 'http://localhost:33225/wd/hub'
        self.assertTrue(self.page.is_visible('superman'))
        ghostdriver_url = self.browser.service.service_url
        resp = requests.get('{}/sessions'.format(ghostdriver_url))
        sessions = resp.json()
        value = sessions.get('value')
        session_id = value[0].get('id')

        script = dedent("""
            var page = this;
            return page.injectJs(arguments[0]);
        """)
        payload = {"script": script, "args": [AXS_FILE]}
        resp = requests.post('{}/session/{}/phantom/execute'.format(ghostdriver_url, session_id), data=json.dumps(payload))
        self.assertEqual(True, resp.json().get('value'))

        script = dedent("""
            var page = this;
            page.injectJs(arguments[0]);
            var report = page.evaluate(function() {
              var results = axs.Audit.run();
              return results;
            });
            return report;
        """)
        payload = {"script": script, "args": [AXS_FILE]}
        resp = requests.post('{}/session/{}/phantom/execute'.format(ghostdriver_url, session_id), data=json.dumps(payload))
        report = resp.json().get('value')

