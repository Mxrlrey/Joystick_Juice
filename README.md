# 🎮 Joystick Juice - Plataforma para Avaliação de Jogos

Este é o repositório do **Joystick Juice**, um sistema web completo desenvolvido com Django que permite gerenciar jogos, clubes, coleções, avaliações e comentários. Além disso, a plataforma integra a **API do IGDB** para importar jogos automaticamente.

> 🔗 **Repositório:** [https://github.com/Mxrlrey/Joystick_Juice.git](https://github.com/Mxrlrey/Joystick_Juice.git)

---

## 🚀 O que este projeto faz
A plataforma funciona como um aplicativo social de jogos, permitindo que os usuários:

- Criem suas próprias listas de jogos.  
- Avaliem jogos, adicionem notas e escrevam reviews detalhados.  
- Recebam comentários de outros usuários nas suas avaliações.  
- Entrem em **clubes de nichos específicos** (por exemplo: clubes de filmes de terror, fantasia, etc.) e participem de conversas temáticas no chat do clube.  
- Recebam e troquem recomendações sobre jogos dentro dos clubes.  
---

## ⚙️ Requisitos
Antes de iniciar, você precisa ter instalado:
- 🐳 **Docker** e **Docker Compose**
- 💻 **Git** (para clonar o repositório)
---

## 📁 Estrutura importante do projeto

| Pasta | Descrição |
|-------|-----------|
| `code/club` | App responsável por gerenciar os clubes de usuários, incluindo chat, membros e tópicos. |
| `code/collection` | App para gerenciar collections de jogos, listas personalizadas de usuários. |
| `code/game` | App principal para CRUD de jogos, integração com a API do IGDB. |
| `code/joystickjuice` | Pasta do projeto Django com configurações, URLs, WSGI, ASGI e utilitários gerais. |
| `code/media` | Arquivos de mídia enviados pelos usuários, como avatars e imagens de jogos. |
| `code/review` | App para criar, editar e listar reviews de jogos, incluindo comentários e avaliações. |
| `code/static` | Arquivos estáticos (CSS, JS, imagens) utilizados pelo front-end da aplicação. |
| `code/templates` | Templates HTML do projeto, incluindo páginas de CRUD, autenticação e layouts gerais. |
| `code/user` | App de gerenciamento de usuários, perfis, autenticação, formulários e dados relacionados. |
| `docker-compose.yml` | Configuração de containers Docker (Django, DB, etc.). |
| `Dockerfile` | Define a imagem Docker do projeto para execução do servidor. |
| `README.md` | Documento de instruções, descrição do projeto e informações de uso. |

---

## 🧰 Instalação e execução

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/Mxrlrey/Joystick_Juice.git
```
---
### 2️⃣ Instalar dependências e rodar o projeto via Docker 🐳 

O projeto **JoystickJuice** utiliza Docker para criar um ambiente isolado com Python 3.13, PostgreSQL e todas as dependências listadas em `requirements.txt`. Isso garante que todos os usuários tenham o mesmo ambiente, sem precisar instalar nada localmente.

#### 💡 Configurar o arquivo `.env`
Para facilitar a configuração, disponibilizamos um arquivo na raiz chamado `.env-exemplo`.  
Renomeie-o para `.env` e preencha os valores de acordo com a tabela abaixo:

| Variável | Categoria | Descrição | O que o usuário deve fazer |
|----------|----------|-----------|---------------------------|
| POSTGRES_DB | Banco de Dados | Nome do banco de dados que o Django irá usar | Ex: `joystickjuice_db` |
| POSTGRES_USER | Banco de Dados | Usuário que terá acesso ao banco | Ex: `admin` |
| POSTGRES_PASSWORD | Banco de Dados | Senha do usuário do banco | Definir senha segura |
| DJANGO_SETTINGS_MODULE | Django | Caminho do módulo de configurações do Django | `joystickjuice.settings` |
| DB_HOST | Django | Host onde o Django vai acessar o banco | Normalmente o serviço Docker `db` |
| POSTGRES_HOST | Django | Host do PostgreSQL | Normalmente igual a `DB_HOST` |
| PGADMIN_DEFAULT_EMAIL | PGAdmin | E-mail de login do PGAdmin | Ex: `admin@example.com` |
| PGADMIN_DEFAULT_PASSWORD | PGAdmin | Senha de login do PGAdmin | Definir senha segura |
| CLIENT_ID | API IGDB | Client ID da API IGDB | Inserir Client ID fornecido pela IGDB |
| CLIENT_SECRET | API IGDB | Client Secret da API IGDB | Inserir Client Secret fornecido pela IGDB |

> ⚠️ **Importante:** Não suba os containers antes de configurar o `.env`, caso contrário o Django pode não conseguir se conectar ao banco ou carregar as configurações.

#### 💡 Subir os containers Docker e instalar dependências
Dentro da pasta do projeto, execute:

```bash
docker compose -f docker-compose.yml up --build -d
```

Verifique se está rodando:
```bash
docker ps
```

### Você verá algo como:

| CONTAINER ID | IMAGE                   | STATUS | PORTS                  |
|--------------|------------------------|--------|-----------------------|
| xxxxxx       | joystickjuice_web       | Up     | 0.0.0.0:8000->8000/tcp |
| xxxxxx       | joystickjuice_db        | Up     | 5432/tcp              |
| xxxxxx       | pgadmin/pgadmin         | Up     | 5050/tcp              |

---
### 4️⃣ Inicializar o banco de dados e aplicar migrations:

Após configurar o `.env` e subir os containers, execute os comandos abaixo **via Docker Compose**:

### Criar migrations (caso você tenha alterado modelos)

```bash
docker compose exec web python manage.py makemigrations
```
### Aplicar migrations existentes
```bash
docker compose exec web python manage.py migrate
```
---
### 5️⃣ Acessar a aplicação
Abra o navegador e vá para:

> http://localhost:8000/account/signup

A aplicação deverá abrir com a tela inicial de Cadastro.


Após se cadastrar, você será redirecionado para a página de login. Coloque os dados cadastrados anteriormente.
> http://localhost:8000/access/login/

Quando esta etapa de cadastro/login estiver finalizada, você será redirecionado para a tela inicial. 
> http://localhost:8000/home/
---

### 6️⃣ Conclusão 
Agora você pode aproveitar a aplicação acessando, pelas telas e via Navbar, as funcionalidades que desejar.

---

### 👥 Equipe do projeto

Este trabalho foi desenvolvido pelos membros do grupo abaixo, para a disciplina **Web1** lecionada pelo Prof. Carlos Anderson.

- **Djavan Teixeira** – GitHub: [@Djavantl](https://github.com/Djavantl)  
- **Gabriel Rocha** – GitHub: [@Rocha0919](https://github.com/Rocha0919)  
- **Marley Meira** – GitHub: [@Mxrlrey](https://github.com/Mxrlrey)  
- **Prof. Carlos Anderson O. Silva** – GitHub: [@profcarlosanderson](https://github.com/profcarlosanderson)  

