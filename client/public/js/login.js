document.querySelector('#login-form').addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    username: document.querySelector('#username').value,
    password: document.querySelector('#password').value,
  };

  const response = await fetch('/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    apiClient.setMessage(data?.error_description || data?.detail || 'Nao foi possivel obter o token.', true);
    return;
  }

  apiClient.setToken(data.access_token);
  apiClient.updateTokenStatus();
  apiClient.setMessage('Login realizado. Redirecionando para a listagem...');

  window.setTimeout(() => {
    window.location.href = '/games.html';
  }, 500);
});
