import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const API_BASE_URL = (process.env.API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');
const OAUTH_CLIENT_ID = process.env.OAUTH_CLIENT_ID || 'joystickjuice-api';
const OAUTH_CLIENT_SECRET = process.env.OAUTH_CLIENT_SECRET || 'joystickjuice-secret';

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', apiBaseUrl: API_BASE_URL });
});

app.post('/auth/token', async (req, res) => {
  const { username, password } = req.body;

  const formData = new URLSearchParams({
    grant_type: 'password',
    username: username || '',
    password: password || '',
    client_id: OAUTH_CLIENT_ID,
    client_secret: OAUTH_CLIENT_SECRET,
    scope: 'read write',
  });

  try {
    const response = await fetch(`${API_BASE_URL}/o/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });

    const data = await response.json().catch(() => null);
    res.status(response.status).json(data || { detail: 'Resposta invalida do servidor OAuth.' });
  } catch (error) {
    res.status(502).json({ detail: `Falha ao conectar no backend: ${error.message}` });
  }
});

app.all('/proxy/*', async (req, res) => {
  const targetPath = req.params[0] || '';
  const targetUrl = `${API_BASE_URL}/${targetPath}`;

  const headers = {};
  if (req.headers.authorization) {
    headers.Authorization = req.headers.authorization;
  }

  let body;
  if (!['GET', 'HEAD'].includes(req.method)) {
    headers['Content-Type'] = 'application/json';
    body = JSON.stringify(req.body || {});
  }

  try {
    const response = await fetch(targetUrl, {
      method: req.method,
      headers,
      body,
    });

    const text = await response.text();
    res.status(response.status);

    const contentType = response.headers.get('content-type') || 'application/json';
    res.setHeader('Content-Type', contentType);
    res.send(text);
  } catch (error) {
    res.status(502).json({ detail: `Falha ao acessar a API: ${error.message}` });
  }
});

app.listen(PORT, () => {
  console.log(`Joystick Juice client running on http://localhost:${PORT}`);
});
