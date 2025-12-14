(() => {
  document.addEventListener("DOMContentLoaded", () => {
    initLogin();
    initPosSearch();
    initTicket();
    initAdminHelpers();
    initProveedorDashboard();
    initProveedorForm();
    initProductosList();
  });

  /** ===============================
   *  LOGIN
   * =============================== */
  function initLogin() {
    const loginForm = document.getElementById("loginForm");
    const usernameInput = document.getElementById("id_username");
    const passwordInput = document.getElementById("id_password");
    const togglePassword = document.getElementById("togglePassword");
    const submitBtn = document.getElementById("submitBtn");
    const usernameError = document.getElementById("username-error");
    const passwordError = document.getElementById("password-error");

    if (!loginForm || !usernameInput || !passwordInput || !togglePassword || !submitBtn) {
      return;
    }

    let isPasswordVisible = false;
    let isSubmitting = false;

    const showError = (input, errorElement, message) => {
      if (!input || !errorElement) return;
      const group = input.parentElement;
      if (group) group.classList.add("error");
      errorElement.textContent = message;
    };

    const clearError = (input, errorElement) => {
      if (!input || !errorElement) return;
      const group = input.parentElement;
      if (group) group.classList.remove("error");
      errorElement.textContent = "";
    };

    const validateUsername = () => {
      const username = usernameInput.value.trim();
      if (!username) {
        showError(usernameInput, usernameError, "El usuario es obligatorio");
        return false;
      }
      if (username.length < 3) {
        showError(usernameInput, usernameError, "Mínimo 3 caracteres");
        return false;
      }
      clearError(usernameInput, usernameError);
      return true;
    };

    const validatePassword = () => {
      const password = passwordInput.value.trim();
      if (!password) {
        showError(passwordInput, passwordError, "La contraseña es obligatoria");
        return false;
      }
      if (password.length < 6) {
        showError(passwordInput, passwordError, "Mínimo 6 caracteres");
        return false;
      }
      clearError(passwordInput, passwordError);
      return true;
    };

    const validateForm = () => validateUsername() && validatePassword();

    const togglePasswordVisibility = () => {
      isPasswordVisible = !isPasswordVisible;
      passwordInput.type = isPasswordVisible ? "text" : "password";
      togglePassword.textContent = isPasswordVisible ? "🙈" : "👁️";
    };

    togglePassword.addEventListener("click", togglePasswordVisibility);
    usernameInput.addEventListener("input", validateUsername);
    passwordInput.addEventListener("input", validatePassword);

    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (isSubmitting) return;
      if (!validateForm()) {
        loginForm.style.animation = "shake 0.5s";
        setTimeout(() => (loginForm.style.animation = ""), 500);
        showNotification("Por favor corrige los errores del formulario", "error");
        return;
      }

      isSubmitting = true;
      submitBtn.disabled = true;
      submitBtn.classList.add("loading");
      setTimeout(() => loginForm.submit(), 400);
    });

    if (!usernameInput.value) {
      setTimeout(() => usernameInput.focus(), 100);
    }
  }

  function showNotification(message, type = "info") {
    const header = document.querySelector(".login-header") || document.body;
    const notification = document.createElement("div");
    notification.className = `message ${type}`;
    notification.innerHTML = `
      <span class="message-icon">${type === "error" ? "❌" : type === "success" ? "✅" : "ℹ️"}</span>
      <span class="message-text">${message}</span>
      <button class="message-close" onclick="this.parentElement.remove()">×</button>
    `;
    header.parentNode.insertBefore(notification, header.nextSibling);
    setTimeout(() => notification.remove(), 5000);
  }

  /** ===============================
   *  POS: BUSCADOR EN VIVO
   * =============================== */
  function initPosSearch() {
    const form = document.getElementById("product-search-form");
    const input = document.getElementById("search-input");
    const clearBtn = document.getElementById("search-clear");
    const cards = document.querySelectorAll(".product-card");
    if (!input || !cards.length) return;

    if (form) form.addEventListener("submit", (e) => e.preventDefault());

    const filtrar = () => {
      const q = input.value.trim().toLowerCase();
      cards.forEach((card) => {
        const name = (card.dataset.name || "").toLowerCase();
        const desc = (card.dataset.desc || "").toLowerCase();
        card.style.display = !q || name.includes(q) || desc.includes(q) ? "" : "none";
      });
    };

    input.addEventListener("input", filtrar);
    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        input.value = "";
        filtrar();
        input.focus();
      });
    }
    filtrar();
  }

  /** ===============================
   *  TICKET
   * =============================== */
  function initTicket() {
    const ticket = document.getElementById("ticket");
    if (!ticket) return;
    rellenarDatos();
    calcularTotales();
    wiringSalir();
    window.descargarTicket = descargarTicket;
  }

  function rellenarDatos() {
    const telEl = document.getElementById("ticket-telefono");
    if (telEl && !telEl.textContent.trim()) {
      telEl.textContent = telEl.dataset.defaultTelefono || "2202643707";
    }

    const cajeroEl = document.getElementById("ticket-cajero");
    if (cajeroEl && !cajeroEl.textContent.trim()) {
      cajeroEl.textContent = cajeroEl.dataset.defaultCajero || "1";
    }

    const now = new Date();
    const fechaEl = document.getElementById("ticket-fecha");
    const horaEl = document.getElementById("ticket-hora");
    if (fechaEl && !fechaEl.textContent.trim()) {
      fechaEl.textContent = now.toLocaleDateString("es-MX");
    }
    if (horaEl && !horaEl.textContent.trim()) {
      horaEl.textContent = now.toLocaleTimeString("es-MX", { hour12: false });
    }

    const folioEl = document.getElementById("ticket-folio");
    if (folioEl && !folioEl.textContent.trim()) {
      folioEl.textContent = generarFolio();
    }
  }

  function generarFolio() {
    return String(Math.floor(10000 + Math.random() * 90000));
  }

  function parseNumber(value) {
    if (typeof value !== "string") return Number(value) || 0;
    const cleaned = value.replace(/[^\d.-]/g, "");
    return Number(cleaned) || 0;
  }

  function formatCurrency(value) {
    return `$${Number(value || 0).toFixed(2)}`;
  }

  function calcularTotales() {
    const rows = Array.from(document.querySelectorAll(".items tbody tr"));
    let subtotal = 0;

    rows.forEach((row) => {
      const totalCell = row.cells[3];
      if (!totalCell) return;
      const totalVal = parseNumber(totalCell.textContent);
      subtotal += totalVal;
      totalCell.textContent = formatCurrency(totalVal);
    });

    const subtotalEl = document.getElementById("ticket-subtotal");
    const ivaEl = document.getElementById("ticket-iva");
    const totalEl = document.getElementById("ticket-total");
    const pagoEl = document.getElementById("ticket-pago");
    const cambioEl = document.getElementById("ticket-cambio");

    if (subtotalEl) subtotalEl.textContent = formatCurrency(subtotal);
    const iva = 0.0;
    if (ivaEl) ivaEl.textContent = formatCurrency(iva);
    const total = subtotal + iva;
    if (totalEl) totalEl.textContent = formatCurrency(total);

    if (pagoEl && !pagoEl.textContent.trim()) pagoEl.textContent = formatCurrency(total);

    if (cambioEl) {
      const pagoVal = parseNumber(pagoEl ? pagoEl.textContent : total);
      const cambioVal = pagoVal - total;
      cambioEl.textContent = formatCurrency(cambioVal);
    }
  }

  function wiringSalir() {
    const salirBtn = document.getElementById("btn-salir");
    if (!salirBtn) return;
    salirBtn.addEventListener("click", () => {
      const url = salirBtn.dataset.salirUrl;
      if (url) window.location.href = url;
    });
  }

  async function descargarTicket() {
    const ticket = document.getElementById("ticket");
    if (!ticket) return;

    const css = await obtenerCss();
    const printable = window.open("", "_blank");
    if (!printable) return;

    printable.document.write(`
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Ticket de Venta</title>
  <style>${css}</style>
</head>
<body class="ticket-page">
${ticket.outerHTML}
</body>
</html>
    `);
    printable.document.close();
    printable.focus();
    printable.print();
    printable.onafterprint = () => printable.close();
  }

  async function obtenerCss() {
    try {
      const res = await fetch("/static/css/style.css", { cache: "no-store" });
      if (res.ok) return await res.text();
    } catch (err) {
      console.warn("No se pudo cargar el CSS del ticket:", err);
    }
    return "";
  }

  /** ===============================
   *  ADMIN HELPERS
   * =============================== */
  function initAdminHelpers() {
    // Navegación activa
    const links = document.querySelectorAll(".admin-nav a");
    if (links.length) {
      const path = location.pathname;
      links.forEach((a) => {
        const href = a.getAttribute("href");
        if (href && path.startsWith(href)) {
          a.classList.add("active");
        }
      });
    }

    // Funciones globales
    window.confirmDelete = (event, name) => {
      const label = name && name.length ? ` \"${name}\"` : "";
      const ok = confirm(`¿Confirma eliminar${label}? Esta acción no se puede deshacer.`);
      if (!ok) {
        event.preventDefault();
        return false;
      }
      return true;
    };

    window.openModal = (modalId) => {
      const m = document.getElementById(modalId);
      if (m) m.style.display = "block";
    };
    window.closeModal = (modalId) => {
      const m = document.getElementById(modalId);
      if (m) m.style.display = "none";
    };
  }

  /** ===============================
   *  PROVEEDORES - DASHBOARD
   * =============================== */
  function initProveedorDashboard() {
    const filas = document.querySelectorAll("tbody tr[data-producto-id]");
    if (!filas.length) return;

    filas.forEach((fila) => {
      fila.addEventListener("click", () => {
        filas.forEach((f) => f.classList.remove("seleccionado"));
        fila.classList.add("seleccionado");
      });
    });

    const style = document.createElement("style");
    style.innerHTML = `
      .seleccionado {
        background-color: #d1f2eb !important;
      }
    `;
    document.head.appendChild(style);
  }

   /*  PROVEEDORES*/
  function initProveedorForm() {
    if (!window.location.pathname.includes("/proveedores")) return;
    const form = document.querySelector("form");
    if (!form) return;
    const inputs = form.querySelectorAll("input, textarea, select");
    if (!inputs.length) return;

    form.addEventListener("submit", (e) => {
      let valid = true;
      inputs.forEach((input) => {
        if (input.hasAttribute("required") && !input.value.trim()) {
          valid = false;
          input.style.borderColor = "red";
        } else {
          input.style.borderColor = "#ccd0d5";
        }
      });
      if (!valid) {
        e.preventDefault();
        alert("Por favor, completa todos los campos obligatorios.");
      }
    });

    inputs.forEach((input) => {
      input.addEventListener("input", () => {
        input.style.borderColor = "#3498db";
      });
    });
  }

  /** ===============================
   *  PRODUCTOS - LISTA (GESTIÓN)
   * =============================== */
  function initProductosList() {
    const notification = document.getElementById("notification");
    const confirmModal = document.getElementById("confirmModal");
    const modalMessage = document.getElementById("modalMessage");
    const confirmCancel = document.getElementById("confirmCancel");
    const confirmOk = document.getElementById("confirmOk");
    const resetFiltersBtn = document.getElementById("resetFilters");
    const filtersForm = document.getElementById("filtersForm");
    const tableRows = document.querySelectorAll(".products-table tbody tr");

    if (!notification && !confirmModal && !tableRows.length) return;

    const showNotificationList = (message, type = "info") => {
      if (!notification) return;
      notification.textContent = message;
      notification.className = `notification ${type}`;
      notification.style.display = "flex";
      setTimeout(() => (notification.style.display = "none"), 5000);
    };

    const showConfirmModal = (message, callback) => {
      if (!confirmModal || !modalMessage) return callback && callback();
      modalMessage.textContent = message;
      pendingAction = callback;
      confirmModal.style.display = "flex";
    };

    const closeModal = () => {
      if (!confirmModal) return;
      confirmModal.style.display = "none";
      pendingAction = null;
    };

    const updateStatusCounter = (isActive) => {
      const activeCountElem = document.getElementById("activeCount");
      const inactiveCountElem = document.getElementById("inactiveCount");
      if (!activeCountElem || !inactiveCountElem) return;
      if (isActive) {
        activeCountElem.textContent = parseInt(activeCountElem.textContent || "0") + 1;
        inactiveCountElem.textContent = parseInt(inactiveCountElem.textContent || "0") - 1;
      } else {
        activeCountElem.textContent = parseInt(activeCountElem.textContent || "0") - 1;
        inactiveCountElem.textContent = parseInt(inactiveCountElem.textContent || "0") + 1;
      }
    };

    const toggleProductStatus = (button, currentActive) => {
      if (!button) return;
      const row = button.closest("tr");
      const statusBadge = row ? row.querySelector(".status-badge") : null;
      const isActive = currentActive === "true";
      const newActiveState = !isActive;

      setTimeout(() => {
        if (row) row.classList.toggle("inactive");
        if (statusBadge) {
          if (newActiveState) {
            statusBadge.className = "status-badge status-active";
            statusBadge.innerHTML = '<i class="fas fa-check-circle"></i> Activo';
            button.innerHTML = '<i class="fas fa-toggle-on"></i>';
            button.title = "Desactivar";
            button.setAttribute("data-active", "true");
          } else {
            statusBadge.className = "status-badge status-inactive";
            statusBadge.innerHTML = '<i class="fas fa-times-circle"></i> Inactivo';
            button.innerHTML = '<i class="fas fa-toggle-off"></i>';
            button.title = "Activar";
            button.setAttribute("data-active", "false");
          }
        }
        updateStatusCounter(newActiveState);
        showNotificationList(`Producto ${newActiveState ? "activado" : "desactivado"} correctamente`, "success");
        closeModal();
      }, 300);
    };

    let pendingAction = null;

    document.querySelectorAll(".btn-toggle-status").forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault();
        const currentActive = this.getAttribute("data-active");
        const action = currentActive === "true" ? "desactivar" : "activar";
        showConfirmModal(`¿Está seguro que desea ${action} este producto?`, () =>
          toggleProductStatus(this, currentActive)
        );
      });
    });

    document.querySelectorAll(".btn-delete").forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault();
        showConfirmModal("¿Está seguro que desea eliminar este producto? Esta acción no se puede deshacer.", () => {
          showNotificationList("Producto eliminado correctamente (simulación)", "success");
          closeModal();
        });
      });
    });

    if (confirmCancel) confirmCancel.addEventListener("click", closeModal);
    if (confirmOk) {
      confirmOk.addEventListener("click", () => {
        if (pendingAction) pendingAction();
      });
    }

    if (confirmModal) {
      confirmModal.addEventListener("click", (e) => {
        if (e.target === confirmModal) closeModal();
      });
    }

    if (resetFiltersBtn && filtersForm) {
      resetFiltersBtn.addEventListener("click", () => {
        filtersForm.reset();
        filtersForm.submit();
      });
    }

    if (filtersForm) {
      filtersForm.addEventListener("submit", function (e) {
        const nombre = this.querySelector("#nombre");
        if (nombre && nombre.value.trim().length > 0 && nombre.value.trim().length < 2) {
          showNotificationList("El término de búsqueda debe tener al menos 2 caracteres", "error");
          e.preventDefault();
        }
      });
    }

    tableRows.forEach((row) => {
      row.addEventListener("mouseenter", function () {
        this.style.transform = "translateX(5px)";
        this.style.transition = "transform 0.2s";
      });
      row.addEventListener("mouseleave", function () {
        this.style.transform = "translateX(0)";
      });
    });

    if (document.querySelectorAll(".products-table tbody tr").length) {
      setTimeout(() => {
        document.querySelectorAll(".products-table tbody tr").forEach((row, index) => {
          row.style.opacity = "0";
          row.style.transform = "translateY(20px)";
          row.style.transition = "all 0.3s ease";
          setTimeout(() => {
            row.style.opacity = "1";
            row.style.transform = "translateY(0)";
          }, index * 50);
        });
      }, 100);
    }

    if (document.location.search && notification) {
      showNotificationList("Mostrando resultados filtrados", "info");
    }
  }
})();
