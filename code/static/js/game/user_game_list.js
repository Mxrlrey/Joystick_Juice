document.addEventListener('DOMContentLoaded', function() {
    var dropdowns = document.querySelectorAll('.status-dropdown-container');

    dropdowns.forEach(function(dropdown) {
        var listItem = dropdown.closest('.game-list-item');
        dropdown.addEventListener('show.bs.dropdown', function () {
            if (listItem) {
                listItem.classList.add('dropdown-active');
            }
        });
        dropdown.addEventListener('hidden.bs.dropdown', function () {
            if (listItem) {
                setTimeout(() => {
                    listItem.classList.remove('dropdown-active');
                }, 100);
            }
        });
    });
});