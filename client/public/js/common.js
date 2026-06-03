const apiClient = {
  tokenKey: 'jj_access_token',

  getToken() {
    return localStorage.getItem(this.tokenKey) || '';
  },

  setToken(token) {
    localStorage.setItem(this.tokenKey, token);
  },

  clearToken() {
    localStorage.removeItem(this.tokenKey);
  },

  setMessage(text, isError = false) {
    const message = document.querySelector('#message');
    if (!message) return;
    message.textContent = text;
    message.style.color = isError ? '#8f1d1d' : '#665f57';
  },

  updateTokenStatus() {
    const status = document.querySelector('#token-status');
    if (!status) return;

    if (this.getToken()) {
      status.textContent = 'Token ativo';
      status.className = 'status online';
      return;
    }

    status.textContent = 'Sem token';
    status.className = 'status offline';
  },

  requireToken() {
    const token = this.getToken();
    if (!token) {
      throw new Error('Faca login para obter um token antes de acessar a API.');
    }
    return token;
  },

  async fetch(path, options = {}) {
    const headers = {
      Authorization: `Bearer ${this.requireToken()}`,
      ...(options.headers || {}),
    };

    const response = await fetch(path, { ...options, headers });
    if (response.status === 204) return null;

    const data = await response.json().catch(() => null);
    if (!response.ok) {
      const detail = data?.detail || JSON.stringify(data) || response.statusText;
      throw new Error(detail);
    }
    return data;
  },

  escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  },
};

document.querySelector('#clear-token')?.addEventListener('click', () => {
  apiClient.clearToken();
  apiClient.updateTokenStatus();
  apiClient.setMessage('Token removido.');
});

apiClient.updateTokenStatus();
