// admin.js - interacciones básicas para el panel de administrador

// Confirmación de eliminación (usa en formularios onsubmit)
function confirmDelete(event, name) {
    // Si no se pasa nombre, usa texto genérico
    const label = name && name.length ? ` "${name}"` : '';
    const ok = confirm(`¿Confirma eliminar${label}? Esta acción no se puede deshacer.`);
    if (!ok) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Simple control para marcar enlace activo (usa cuando el template no lo haga)
document.addEventListener('DOMContentLoaded', function () {
    // Manejar menú activo según URL
    const links = document.querySelectorAll('.admin-nav a');
    const path = location.pathname;
    links.forEach(a => {
        try {
            // compara el atributo href con el path (coincidencia básica)
            const href = a.getAttribute('href');
            if (href && path.startsWith(href)) {
                a.classList.add('active');
            }
        } catch (e) { /* ignore */ }
    });
});

// Función para abrir modal simple (si decides añadir)
function openModal(modalId) {
    const m = document.getElementById(modalId);
    if (!m) return;
    m.style.display = 'block';
}
function closeModal(modalId) {
    const m = document.getElementById(modalId);
    if (!m) return;
    m.style.display = 'none';
}
