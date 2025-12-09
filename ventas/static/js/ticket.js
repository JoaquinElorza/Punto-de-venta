document.addEventListener("DOMContentLoaded", () => {
    rellenarDatos();
    calcularTotales();
    wiringSalir();
});

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

    rows.forEach(row => {
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
        if (url) {
            window.location.href = url;
        }
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
        if (res.ok) {
            return await res.text();
        }
    } catch (err) {
        console.warn("No se pudo cargar el CSS del ticket:", err);
    }
    return "";
}
