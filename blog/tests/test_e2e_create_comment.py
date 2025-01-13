from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from blog.models import Post  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EndToEndAddCommentTests(StaticLiveServerTestCase):
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
            title='Post para Comentário',
            content='Conteúdo do post para teste de comentário.',
            author=self.user
        )

    def test_add_comment(self):
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

        self.driver.get(f'{self.live_server_url}/post/{self.post.id}/')
        self.assertIn(self.post.title, self.driver.title)

        comment_input = self.driver.find_element(By.NAME, 'conteudo')
        comment_input.send_keys('Este é meu comentário de teste.')

        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Comentar']")
        self.driver.execute_script("arguments[0].click();", submit_button)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Este é meu comentário de teste.')]"))
        )

        comment_text = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Este é meu comentário de teste.')]")
        self.assertEqual(comment_text.text, 'Este é meu comentário de teste.')
