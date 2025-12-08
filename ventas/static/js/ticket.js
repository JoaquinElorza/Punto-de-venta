function descargarTicket() {
    const ticket = document.getElementById("ticket");

    // Contenido del ticket como archivo HTML
    const contenido = `
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Ticket de Venta</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
${ticket.outerHTML}
</body>
</html>
`.trim();

    // Crear archivo descargable
    const blob = new Blob([contenido], { type: "text/html" });
    const url = URL.createObjectURL(blob);

    // Descargar archivo
    const a = document.createElement("a");
    a.href = url;
    a.download = "ticket.html";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
}
