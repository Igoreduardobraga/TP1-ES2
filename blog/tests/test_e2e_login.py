from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class MyEndToEndTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_example(self):
        self.driver.get(f'{self.live_server_url}/')
        self.assertIn('Login', self.driver.title)
