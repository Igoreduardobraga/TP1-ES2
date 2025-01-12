from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EndToEndRegisterTests(StaticLiveServerTestCase):
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

    def test_register_page(self):
        self.driver.get(f'{self.live_server_url}/registro')
        self.assertIn('Registro', self.driver.title)

    def test_valid_register(self):
        self.driver.get(f'{self.live_server_url}/registro')
        
        username_input = self.driver.find_element(By.NAME, 'username')
        email_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password1')
        password_confirmation_input = self.driver.find_element(By.NAME, 'password2')

        username_input.send_keys('some_username')
        email_input.send_keys('username@email.com')
        password_input.send_keys('some_password')
        password_confirmation_input.send_keys('some_password')
        
        password_confirmation_input.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 100).until(EC.url_changes(f'{self.live_server_url}/post_list'))

        self.assertIn('Blog', self.driver.title)
        span = self.driver.find_element(By.XPATH, "//span[text()='Bem-vindo, some_username!']")
        self.assertIsNotNone(span)

