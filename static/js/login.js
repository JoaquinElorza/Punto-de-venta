document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('id_username');
    const passwordInput = document.getElementById('id_password');
    const togglePassword = document.getElementById('togglePassword');
    const submitBtn = document.getElementById('submitBtn');
    const usernameError = document.getElementById('username-error');
    const passwordError = document.getElementById('password-error');

    let isPasswordVisible = false;
    let isSubmitting = false;

    /** ===============================
     *   VISIBILIDAD DE CONTRASEÑA
     *  =============================== */
    function togglePasswordVisibility() {
        isPasswordVisible = !isPasswordVisible;
        passwordInput.type = isPasswordVisible ? 'text' : 'password';
        togglePassword.textContent = isPasswordVisible ? '🙈' : '👁️';
    }

    togglePassword.addEventListener('click', togglePasswordVisibility);


    /** ===============================
     *           VALIDACIONES
     *  =============================== */
    function showError(input, errorElement, message) {
        input.parentElement.classList.add('error');
        input.parentElement.classList.remove('success');
        errorElement.textContent = message;
    }

    function clearError(input, errorElement) {
        input.parentElement.classList.remove('error');
        errorElement.textContent = '';
    }

    function validateUsername() {
        const username = usernameInput.value.trim();
        if (!username) {
            showError(usernameInput, usernameError, 'El usuario es obligatorio');
            return false;
        }
        if (username.length < 3) {
            showError(usernameInput, usernameError, 'Mínimo 3 caracteres');
            return false;
        }
        clearError(usernameInput, usernameError);
        return true;
    }

    function validatePassword() {
        const password = passwordInput.value.trim();
        if (!password) {
            showError(passwordInput, passwordError, 'La contraseña es obligatoria');
            return false;
        }
        if (password.length < 6) {
            showError(passwordInput, passwordError, 'Mínimo 6 caracteres');
            return false;
        }
        clearError(passwordInput, passwordError);
        return true;
    }

    function validateForm() {
        return validateUsername() && validatePassword();
    }


    /** ===============================
     *         NOTIFICACIONES
     *  =============================== */
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `message ${type}`;
        notification.innerHTML = `
            <span class="message-icon">${type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️'}</span>
            <span class="message-text">${message}</span>
            <button class="message-close" onclick="this.parentElement.remove()">×</button>
        `;
        const header = document.querySelector('.login-header');
        header.parentNode.insertBefore(notification, header.nextSibling);

        setTimeout(() => notification.remove(), 5000);
    }


    /** ===============================
     *              SUBMIT
     *  =============================== */
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Evitar doble clic
        if (isSubmitting) return;

        if (!validateForm()) {
            loginForm.style.animation = 'shake 0.5s';
            setTimeout(() => loginForm.style.animation = '', 500);
            showNotification('Por favor corrige los errores del formulario', 'error');
            return;
        }

        isSubmitting = true;
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');

        // Pequeño delay para animación
        setTimeout(() => {
            loginForm.submit();
        }, 400);
    });


    /** ===============================
     *              EXTRAS
     *  =============================== */
    usernameInput.addEventListener('input', validateUsername);
    passwordInput.addEventListener('input', validatePassword);

    if (!usernameInput.value) {
        setTimeout(() => usernameInput.focus(), 100);
    }
});
