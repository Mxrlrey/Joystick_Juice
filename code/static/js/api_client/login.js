document.querySelector('#login-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new URLSearchParams({
        grant_type: 'password',
        username: document.querySelector('#username').value,
        password: document.querySelector('#password').value,
        client_id: apiClient.clientId,
        client_secret: apiClient.clientSecret,
        scope: 'read write',
    });

    const response = await fetch('/o/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
        apiClient.setMessage(data?.error_description || 'Nao foi possivel obter o token.', true);
        return;
    }

    apiClient.setToken(data.access_token);
    apiClient.updateTokenStatus();
    apiClient.setMessage('Login realizado. Redirecionando para a listagem...');

    window.setTimeout(() => {
        window.location.href = '/client/games/';
    }, 500);
});
