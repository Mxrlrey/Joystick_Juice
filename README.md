# Joystick Juice

Aplicacao com backend Django + Django REST Framework e autenticacao OAuth2 via Django OAuth Toolkit, acompanhada de um cliente separado em Node.js para demonstrar o consumo seguro da API.

## Estrutura de entrega
- `api/`: documentacao da API entregue no trabalho
- `client/`: cliente separado do Django, implementado em Node.js + Express + JavaScript
- `code/api/`: implementacao real da API DRF dentro do projeto Django
- `code/game/`, `code/review/`, `code/user/`, `code/collection/`, `code/club/`: apps da aplicacao
- `code/joystickjuice/`: settings, urls e configuracoes do projeto

## Requisitos atendidos
### API
- Django REST Framework: implementado em `code/api/`
- OAuth2 com Django OAuth Toolkit: configurado em `code/joystickjuice/settings.py`, `code/joystickjuice/urls.py` e `code/entrypoint.sh`
- Tres models relacionados: `Game`, `Review`, `Comment`
- CRUD completo de model principal: `Game` em `/api/games/`
- Serializers: `GameSerializer`, `ReviewSerializer`, `CommentSerializer`

### Cliente
- Tecnologia diferente de Python/Django: Node.js + Express no servidor do cliente e JavaScript no navegador
- Login OAuth2 com obtencao de token: `POST /auth/token` no cliente, que encaminha para `POST /o/token/` no Django
- Acesso a rota protegida: CRUD de `/api/games/` via proxy do cliente
- Interface funcional: paginas HTML em `client/public/`

## Modelos e relacionamentos
- `Game`
- `Review` -> relacionamento com `Game` e `User`
- `Comment` -> relacionamento com `Review` e `User`

## Rotas da API
### OAuth2
- `POST /o/token/`

### Recursos
- `GET /api/games/`
- `POST /api/games/`
- `GET /api/games/{id}/`
- `PUT/PATCH /api/games/{id}/`
- `DELETE /api/games/{id}/`
- `GET /api/reviews/`
- `POST /api/reviews/`
- `GET /api/comments/`
- `POST /api/comments/`

## Como executar o backend
### 1. Clonar o repositorio
```bash
git clone https://github.com/Mxrlrey/Joystick_Juice.git
cd Joystick_Juice
```

### 2. Configurar variaveis de ambiente
Copie `.env-exemplo` para `.env` e preencha os valores:
```bash
cp .env-exemplo .env
```

Campos importantes:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `DJANGO_SETTINGS_MODULE=joystickjuice.settings`
- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`
- `OAUTH_CLIENT_ID`
- `OAUTH_CLIENT_SECRET`
- `CLIENT_ID`
- `CLIENT_SECRET`

### 3. Subir containers
```bash
docker compose up --build -d
```

Esse comando sobe:
- `db` em `localhost` interno do Compose
- `web` em `http://localhost:8000`
- `client` em `http://localhost:3000`
- `pgadminjuice` em `http://localhost:5051`

### 4. Aplicar migrations
```bash
docker compose exec web python manage.py migrate
```

Observacao: o `entrypoint.sh` do backend ja executa `migrate` automaticamente ao subir o container.

### 5. Acessar o backend
- Aplicacao Django: `http://localhost:8000/`
- Admin Django: `http://localhost:8000/admin/`
- Token OAuth2: `http://localhost:8000/o/token/`
- API DRF: `http://localhost:8000/api/games/`

## Como executar o cliente separado
O cliente oficial da entrega esta na pasta `client/`.

### 1. Configurar ambiente do cliente
```bash
cd client
cp .env.example .env
```

Ajuste os valores conforme seu backend. Exemplo:
```env
PORT=3000
API_BASE_URL=http://localhost:8000
OAUTH_CLIENT_ID=joystickjuice-api
OAUTH_CLIENT_SECRET=joystickjuice-secret
```

### 2. Instalar dependencias
```bash
npm install
```

### 3. Executar o cliente
```bash
npm run start
```

### 4. Acessar o cliente
Abra:
- `http://localhost:3000/`

Se voce subiu tudo com Docker Compose, nao precisa instalar Node localmente para testar o cliente.

Fluxo esperado:
1. Fazer login com usuario e senha
2. Cliente solicita token ao proprio servidor Node em `/auth/token`
3. Servidor Node troca credenciais com o Django OAuth Toolkit
4. Navegador recebe `access_token`
5. Cliente acessa `/proxy/api/games/` para listar, criar, editar e excluir jogos

## Como o cliente se comunica com a API
- Navegador -> `client/server.js`
- `client/server.js` -> backend Django
- O `client_secret` fica no servidor Node, nao no JavaScript do navegador
- O token OAuth2 e enviado como `Bearer Token` nas chamadas protegidas

## Cliente legado dentro do Django
Ainda existe uma demonstracao antiga servida pelo proprio Django em:
- `http://localhost:8000/client/`

Ela foi mantida como referencia, mas a entrega principal do requisito `cliente separado` agora esta em `client/`.

## Equipe
- Djavan Teixeira
- Gabriel Rocha
- Marley Meira

## Video
Inclua no repositorio o link do video final mostrando:
1. Obtencao do token OAuth2
2. Consumo de rota protegida
3. CRUD do recurso principal
4. Integracao Cliente <-> API
