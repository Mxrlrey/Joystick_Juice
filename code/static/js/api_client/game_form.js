const fields = {
    id: document.querySelector('#game-id'),
    title: document.querySelector('#title'),
    genre: document.querySelector('#genre'),
    releaseDate: document.querySelector('#release-date'),
    developer: document.querySelector('#developer'),
    synopsis: document.querySelector('#synopsis'),
    coverUrl: document.querySelector('#cover-url'),
    bannerUrl: document.querySelector('#banner-url'),
    trailerUrl: document.querySelector('#trailer-url'),
};

const editId = new URLSearchParams(window.location.search).get('id');

async function loadGameForEdit() {
    if (!editId) {
        return;
    }

    try {
        const game = await apiClient.fetch(`/api/games/${editId}/`);
        document.querySelector('#form-title').textContent = 'Editar jogo';
        fields.id.value = game.id;
        fields.title.value = game.title || '';
        fields.genre.value = game.genre || '';
        fields.releaseDate.value = game.release_date || '';
        fields.developer.value = game.developer || '';
        fields.synopsis.value = game.synopsis || '';
        fields.coverUrl.value = game.cover_url || '';
        fields.bannerUrl.value = game.banner_url || '';
        fields.trailerUrl.value = game.trailer_url || '';
        apiClient.setMessage(`Editando ${game.title}.`);
    } catch (error) {
        apiClient.setMessage(error.message, true);
    }
}

async function saveGame(event) {
    event.preventDefault();

    const payload = {
        title: fields.title.value,
        genre: fields.genre.value,
        release_date: fields.releaseDate.value,
        synopsis: fields.synopsis.value,
        developer: fields.developer.value,
        cover_url: fields.coverUrl.value || null,
        banner_url: fields.bannerUrl.value || null,
        trailer_url: fields.trailerUrl.value || null,
    };

    const id = fields.id.value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/games/${id}/` : '/api/games/';

    try {
        await apiClient.fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        apiClient.setMessage(id ? 'Jogo atualizado pela API.' : 'Jogo criado pela API.');

        window.setTimeout(() => {
            window.location.href = '/client/games/';
        }, 600);
    } catch (error) {
        apiClient.setMessage(error.message, true);
    }
}

document.querySelector('#game-form').addEventListener('submit', saveGame);
document.querySelector('#clear-form').addEventListener('click', () => {
    document.querySelector('#game-form').reset();
    fields.id.value = '';
    document.querySelector('#form-title').textContent = 'Adicionar jogo';
});

loadGameForEdit();
