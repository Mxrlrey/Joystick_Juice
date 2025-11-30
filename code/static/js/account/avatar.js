// static/js/account/avatar.js
document.addEventListener('DOMContentLoaded', function () {
  const fileInput = document.getElementById('avatarFileInput');
  const chooseBtn = document.getElementById('chooseImageBtn');
  const resetBtn = document.getElementById('resetImageBtn');
  const fileNameEl = document.getElementById('fileName');
  const previewWrap = document.getElementById('avatarPreview');
  const previewImg = document.getElementById('avatarPreviewImg');

  function resetPreview() {
    if (fileInput) fileInput.value = '';
    fileNameEl.textContent = 'Nenhum arquivo selecionado';
    previewWrap.classList.remove('has-image');
    previewImg.removeAttribute('src');
  }

  // Abrir seletor de arquivos
  if (chooseBtn) {
    chooseBtn.addEventListener('click', () => {
      if (fileInput) fileInput.click();
    });
  }

  // Resetar seleção
  if (resetBtn) {
    resetBtn.addEventListener('click', (e) => {
      e.preventDefault();
      resetPreview();
    });
  }

  // Processar mudança de arquivo
  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      
      if (!file) {
        resetPreview();
        return;
      }
      
      // Validar tipo de arquivo
      if (!file.type.startsWith('image/')) {
        alert('Por favor selecione uma imagem (JPG/PNG).');
        resetPreview();
        return;
      }
      
      // Validar tamanho do arquivo
      if (file.size && file.size > 5 * 1024 * 1024) {
        alert('Arquivo muito grande. Máx. 5MB.');
        resetPreview();
        return;
      }
      
      // Atualizar informações do arquivo
      fileNameEl.textContent = file.name;
      
      // Criar preview
      const reader = new FileReader();
      reader.onload = function (ev) {
        previewImg.src = ev.target.result;
        previewWrap.classList.add('has-image');
      };
      reader.readAsDataURL(file);
    });
  }
});