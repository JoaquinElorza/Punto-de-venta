// POS - JS mínimo para buscador en vivo
document.addEventListener('DOMContentLoaded', () => {
    console.log('POS JS cargado ✅');

    const form = document.getElementById('product-search-form');
    const input = document.getElementById('search-input');
    const clearBtn = document.getElementById('search-clear');
    const cards = document.querySelectorAll('.product-card');

    if (!input || !cards.length) {
        console.warn('No se encontraron elementos de búsqueda o cards de producto');
        return;
    }

    // Evitar que Enter recargue la página
    if (form) {
        form.addEventListener('submit', (e) => e.preventDefault());
    }

    // Función de filtrado
    const filtrar = () => {
        const q = input.value.trim().toLowerCase();
        cards.forEach(card => {
            const name = (card.dataset.name || '').toLowerCase();
            const desc = (card.dataset.desc || '').toLowerCase();

            if (!q || name.includes(q) || desc.includes(q)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    };

    // Filtrar mientras escribe
    input.addEventListener('input', filtrar);

    // Botón X: limpiar y mostrar todo
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            input.value = '';
            filtrar();
            input.focus();
        });
    }

    // Aplicar filtro inicial (por si ya hay texto)
    filtrar();
});
