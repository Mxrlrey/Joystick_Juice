const gamesEl = document.querySelector('#games');

async function loadGames() {
  try {
    const games = await apiClient.fetch('/proxy/api/games/');
    renderGames(games);
    apiClient.setMessage(`${games.length} jogo(s) carregado(s) pela rota protegida.`);
  } catch (error) {
    gamesEl.innerHTML = '';
    apiClient.setMessage(error.message, true);
  }
}

function renderGames(games) {
  gamesEl.innerHTML = '';

  if (!games.length) {
    gamesEl.innerHTML = '<p class="muted">Nenhum jogo encontrado.</p>';
    return;
  }

  for (const game of games) {
    const row = document.createElement('article');
    row.className = 'game-row';
    row.innerHTML = `
      <div>
        <div class="game-title">${apiClient.escapeHtml(game.title)}</div>
        <div class="game-meta">${apiClient.escapeHtml(game.genre)} | ${apiClient.escapeHtml(game.developer)} | ${game.release_date}</div>
      </div>
      <div class="actions">
        <a class="button secondary" href="/game-form.html?id=${game.id}">Editar</a>
        <button class="danger" type="button" data-delete="${game.id}">Excluir</button>
      </div>
    `;
    gamesEl.appendChild(row);
  }
}

async function deleteGame(id) {
  try {
    await apiClient.fetch(`/proxy/api/games/${id}/`, { method: 'DELETE' });
    await loadGames();
    apiClient.setMessage('Jogo excluido pela API.');
  } catch (error) {
    apiClient.setMessage(error.message, true);
  }
}

document.querySelector('#refresh-games').addEventListener('click', loadGames);

gamesEl.addEventListener('click', (event) => {
  const deleteId = event.target.dataset.delete;
  if (deleteId) {
    deleteGame(deleteId);
  }
});

loadGames();
