# API REST - Joystick Juice

Este diretório existe para atender a entrega com `/api` e documentar a API RESTful.

## Implementação
A implementação Django REST Framework está em `code/api/`:
- `code/api/views.py`
- `code/api/serializers.py`
- `code/api/urls.py`

## Autenticação
A API usa Django OAuth Toolkit com bearer token.

Fluxo utilizado:
1. Cliente solicita token em `POST /o/token/`
2. Recebe `access_token`
3. Envia `Authorization: Bearer <token>` nas rotas protegidas

## Rotas principais
- `GET/POST /api/games/`
- `GET/PUT/PATCH/DELETE /api/games/{id}/`
- `GET/POST /api/reviews/`
- `GET/PUT/PATCH/DELETE /api/reviews/{id}/`
- `GET/POST /api/comments/`
- `GET/PUT/PATCH/DELETE /api/comments/{id}/`

## Recursos e relacionamentos
- `Game`
- `Review` -> pertence a `Game` e `User`
- `Comment` -> pertence a `Review` e `User`

## Serializers
- `GameSerializer`
- `ReviewSerializer`
- `CommentSerializer`
- `UserSummarySerializer`
