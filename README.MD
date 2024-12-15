# Blog Django

## 1. Membros do Grupo
- **Alan Cabral Trindade Prado** 
- **Igor Eduardo Martins Braga** 

---

## 2. Sobre o Sistema

O PostSphere é um sistema de gerenciamento de postagens que permite aos usuários autenticar-se, criar, editar, visualizar e excluir postagens. Ele inclui autenticação de usuários para proteger operações sensíveis, garantindo que apenas pessoas autorizadas possam gerenciar o conteúdo.

### Funcionalidades Principais:
1. **Autenticação de Usuários:**
   - Permite que os usuários façam login e logout de forma segura.
   - Apenas usuários autenticados podem acessar funcionalidades protegidas, como criar, editar ou excluir postagens.
   - Caso um usuário não autenticado tente acessar uma página protegida, ele será redirecionado automaticamente para a página de login, garantindo a segurança do sistema.

2. **Gerenciamento de Postagens:**
   - **Criar novas postagens:** Usuários podem adicionar postagens com título e conteúdo. Cada postagem é associada ao autor que a criou e inclui informações de data de criação e última atualização.
   - **Editar postagens existentes:** É possível modificar o conteúdo de postagens já criadas. Apenas usuários autenticados podem realizar essa ação.
   - **Excluir postagens:** Usuários podem remover postagens de forma definitiva, garantindo controle total sobre o conteúdo.
   - **Visualizar uma lista de postagens:** Todas as postagens são exibidas em ordem cronológica reversa, com os itens mais recentes aparecendo primeiro, facilitando a navegação e o acompanhamento do conteúdo.

3. **Página Inicial:**
   - A página inicial do sistema adapta-se ao status do usuário:
     - **Não autenticado:** Redireciona para a página de login, solicitando credenciais para acessar o sistema.
     - **Autenticado:** Redireciona para a lista de postagens, permitindo acesso direto às funcionalidades disponíveis.

---

## 3. Tecnologias Utilizadas

- **Python 3.12.3**
- **Django 5.1.4**
- **SQLite3**
- **Bootstrap 5**

---

## 4. Estrutura do Projeto

### Pastas e Arquivos Principais:
- **blog/**: Diretório principal do app.
  - `models.py`: Define o modelo `Post`.
  - `views.py`: Contém a lógica para gerenciamento de postagens e autenticação.
  - `forms.py`: Define o formulário para criação e edição de postagens.
  - `urls.py`: Configuração das rotas do app.
  - `templates/`: Contém os templates HTML usados no sistema.
- **blog_project/**: Diretório principal do projeto.
  - `settings.py`: Configuração global do projeto.
  - `urls.py`: Configuração das rotas globais do projeto.

---

## 5. Como Rodar o Projeto

### Pré-requisitos:
- Python 3.12 ou superior instalado.
- Pip (gerenciador de pacotes do Python).
- Ambiente virtual (opcional, mas recomendado).

### Passos para Instalação e Execução:
1. **Clone o Repositório:**
   ```bash
   git clone https://github.com/seu-repositorio/blog-django.git
   cd blog-django

1. **Crie e Ative o Ambiente Virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    venv\Scripts\activate     # Para Windows
    
1. **Instale as Dependências:**
   ```bash
    pip install django


1. **Configure o Banco de Dados:**
   ```bash
    python manage.py migrate


1. **Crie um Superusuário (Admin):**
   ```bash
    python manage.py createsuperuser

1. **Inicie o Servidor:**
   ```bash
    python manage.py runserver
