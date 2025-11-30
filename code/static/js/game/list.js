document.addEventListener('DOMContentLoaded', function() {
    const radios = document.querySelectorAll('.select-game');
    const editBtn = document.getElementById('edit-btn');
    const deleteBtn = document.getElementById('delete-btn');
    const editUrlTemplate = editBtn.getAttribute('data-edit-url');
    const deleteUrlTemplate = deleteBtn.getAttribute('data-delete-url');

    function updateActionButtons() {
        const selectedRadio = document.querySelector('.select-game:checked');

        if (selectedRadio) {
            const selectedId = selectedRadio.value;
            editBtn.disabled = false;
            deleteBtn.disabled = false;
            editBtn.onclick = () => {
                window.location.href = editUrlTemplate.replace("/0/", `/${selectedId}/`);
            };
            deleteBtn.onclick = () => {
                window.location.href = deleteUrlTemplate.replace("/0/", `/${selectedId}/`);
            };
        } else {
            editBtn.disabled = true;
            deleteBtn.disabled = true;
            editBtn.onclick = null;
            deleteBtn.onclick = null;
        }
    }

    radios.forEach(radio => {
        radio.addEventListener('change', updateActionButtons);
    });
    updateActionButtons();
});