document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const notification = document.getElementById('notification');
    const confirmModal = document.getElementById('confirmModal');
    const modalMessage = document.getElementById('modalMessage');
    const confirmCancel = document.getElementById('confirmCancel');
    const confirmOk = document.getElementById('confirmOk');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const filtersForm = document.getElementById('filtersForm');

    // Variables de estado
    let pendingAction = null;
    let activeCount = 0;
    let inactiveCount = 0;

    // Inicializar contadores
    function initializeCounters() {
        const activeProducts = document.querySelectorAll('.status-active').length;
        const inactiveProducts = document.querySelectorAll('.status-inactive').length;
        
        document.getElementById('activeCount').textContent = activeProducts;
        document.getElementById('inactiveCount').textContent = inactiveProducts;
    }

    // Mostrar notificación
    function showNotification(message, type = 'info') {
        notification.textContent = message;
        notification.className = `notification ${type}`;
        notification.style.display = 'flex';
        
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }

    // Mostrar modal de confirmación
    function showConfirmModal(message, callback) {
        modalMessage.textContent = message;
        pendingAction = callback;
        confirmModal.style.display = 'flex';
    }

    // Cerrar modal
    function closeModal() {
        confirmModal.style.display = 'none';
        pendingAction = null;
    }

    // Actualizar contador de estado
    function updateStatusCounter(productId, isActive) {
        const activeCountElem = document.getElementById('activeCount');
        const inactiveCountElem = document.getElementById('inactiveCount');
        
        if (isActive) {
            activeCountElem.textContent = parseInt(activeCountElem.textContent) + 1;
            inactiveCountElem.textContent = parseInt(inactiveCountElem.textContent) - 1;
        } else {
            activeCountElem.textContent = parseInt(activeCountElem.textContent) - 1;
            inactiveCountElem.textContent = parseInt(inactiveCountElem.textContent) + 1;
        }
    }

    // Alternar estado del producto (simulado)
    function toggleProductStatus(productId, currentActive) {
        const button = document.querySelector(`.btn-toggle-status[data-id="${productId}"]`);
        const row = button.closest('tr');
        const statusBadge = row.querySelector('.status-badge');
        const statusIcon = statusBadge.querySelector('i');
        const isActive = currentActive === 'true';
        const newActiveState = !isActive;
        
        // Simular actualización en servidor (en producción sería una petición AJAX)
        setTimeout(() => {
            // Actualizar UI
            row.classList.toggle('inactive');
            
            if (newActiveState) {
                statusBadge.className = 'status-badge status-active';
                statusBadge.innerHTML = '<i class="fas fa-check-circle"></i> Activo';
                button.innerHTML = '<i class="fas fa-toggle-on"></i>';
                button.title = 'Desactivar';
                button.setAttribute('data-active', 'true');
            } else {
                statusBadge.className = 'status-badge status-inactive';
                statusBadge.innerHTML = '<i class="fas fa-times-circle"></i> Inactivo';
                button.innerHTML = '<i class="fas fa-toggle-off"></i>';
                button.title = 'Activar';
                button.setAttribute('data-active', 'false');
            }
            
            updateStatusCounter(productId, newActiveState);
            showNotification(`Producto ${newActiveState ? 'activado' : 'desactivado'} correctamente`, 'success');
        }, 300);
    }

    // Confirmar eliminación
    function confirmDelete(deleteUrl) {
        showConfirmModal('¿Está seguro que desea eliminar este producto? Esta acción no se puede deshacer.', function() {
            // En producción, redirigiría directamente
            // window.location.href = deleteUrl;
            
            // Por ahora mostramos un mensaje
            showNotification('Producto eliminado correctamente (simulación)', 'success');
            closeModal();
            
            // En producción real, sería:
            // fetch(deleteUrl, { method: 'POST' })
            //     .then(response => window.location.reload());
        });
    }

    // Limpiar filtros
    function resetFilters() {
        filtersForm.reset();
        filtersForm.submit();
    }

    // Event Listeners

    // Botones de alternar estado
    document.querySelectorAll('.btn-toggle-status').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-id');
            const currentActive = this.getAttribute('data-active');
            const action = currentActive === 'true' ? 'desactivar' : 'activar';
            
            showConfirmModal(
                `¿Está seguro que desea ${action} este producto?`,
                () => toggleProductStatus(productId, currentActive)
            );
        });
    });

    // Botones de eliminar
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            confirmDelete(this.href);
        });
    });

    // Modal de confirmación
    confirmCancel.addEventListener('click', closeModal);
    confirmOk.addEventListener('click', function() {
        if (pendingAction) {
            pendingAction();
            closeModal();
        }
    });

    // Cerrar modal al hacer clic fuera
    confirmModal.addEventListener('click', function(e) {
        if (e.target === confirmModal) {
            closeModal();
        }
    });

    // Limpiar filtros
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', resetFilters);
    }

    // Validar formulario de filtros
    if (filtersForm) {
        filtersForm.addEventListener('submit', function(e) {
            // Aquí podrías agregar validaciones adicionales
            const nombre = this.querySelector('#nombre').value.trim();
            if (nombre.length > 0 && nombre.length < 2) {
                showNotification('El término de búsqueda debe tener al menos 2 caracteres', 'error');
                e.preventDefault();
            }
        });
    }

    // Efectos visuales para filas
    document.querySelectorAll('.products-table tbody tr').forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
            this.style.transition = 'transform 0.2s';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });

    // Inicializar
    initializeCounters();

    // Verificar si hay parámetros de búsqueda en la URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.toString()) {
        showNotification('Mostrando resultados filtrados', 'info');
    }

    // Efecto de carga inicial
    setTimeout(() => {
        document.querySelectorAll('.products-table tbody tr').forEach((row, index) => {
            row.style.opacity = '0';
            row.style.transform = 'translateY(20px)';
            row.style.transition = 'all 0.3s ease';
            
            setTimeout(() => {
                row.style.opacity = '1';
                row.style.transform = 'translateY(0)';
            }, index * 50);
        });
    }, 100);
});