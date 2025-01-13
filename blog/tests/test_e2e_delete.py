from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from blog.models import Post  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EndToEndDeletePostTests(StaticLiveServerTestCase):
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

        self.post = Post.objects.create(
            title='Post para Exclusão',
            content='Conteúdo do post para exclusão.',
            author=self.user
        )

    def test_delete_post(self):
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

        self.driver.get(f'{self.live_server_url}/post_list/')
        self.assertIn('Blog', self.driver.title)

        delete_button = self.driver.find_element(By.XPATH, f"//a[@href='/post/{self.post.id}/delete/']")
        delete_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Excluir Post')]"))
        )
        confirm_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        confirm_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(f'{self.live_server_url}/post_list/')
        )

        with self.assertRaises(Exception):  # Se o post foi excluído, ele não será encontrado
            self.driver.find_element(By.XPATH, f"//a[@href='/post/{self.post.id}/']")
