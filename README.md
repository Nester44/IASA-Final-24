# IASA-Champ-24

## Deploying with Docker

### Development

Copy .env.example as .env and edit the necessary variables.

``docker compose up --build``

Frontend part of the application is available on port $FRONTEND_PORT (default: 3000).
Backend part of the application is available on port $BACKEND_PORT (default: 8000).

## Run

### Frontend

Set up .env in the frontned directory from example with port http://localhost:5000 as API path

```
npm i
npm run dev
```

It will be available on http://localhost:5173

### Backend

Set up .env in backend directory from .env.example

```pip install -r requirements.txt```
```flask run```