from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EndToEndCreatePostTests(StaticLiveServerTestCase):
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

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_post(self):
        self.driver.get(f'{self.live_server_url}/login/')
        self.assertIn('Login', self.driver.title)

        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')

        username_input.send_keys('testuser')
        password_input.send_keys('password')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Bem-vindo, testuser!')]"))
        )

        self.driver.get(f'{self.live_server_url}/post/new')
        self.assertIn('Criar/Editar Post', self.driver.title)

        title_input = self.driver.find_element(By.NAME, 'title')
        content_input = self.driver.find_element(By.NAME, 'content')

        title_input.send_keys('Meu Primeiro Post')
        content_input.send_keys('Este é o conteúdo do meu primeiro post no blog.')

        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.driver.execute_script("arguments[0].click();", submit_button)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Meu Primeiro Post')]"))
        )

        post_title = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Meu Primeiro Post')]")
        self.assertEqual(post_title.text, 'Meu Primeiro Post')
