from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EndToEndLoginTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login_page(self):
        self.driver.get(f'{self.live_server_url}/login')
        self.assertIn('Login', self.driver.title)

    def test_invalid_login(self):
        self.driver.get(f'{self.live_server_url}/login')
        
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('invaliduser')

        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys('wrongpassword')
        
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 100).until(EC.url_changes(f'{self.live_server_url}/login'))

        self.assertIn('Login', self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username'))
        self.assertTrue(self.driver.find_element(By.NAME, 'password'))

