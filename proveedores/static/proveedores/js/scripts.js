document.addEventListener("DOMContentLoaded", () => {
    console.log("Dashboard cargado correctamente.");

    // Ejemplo: resaltar fila seleccionada
    const filas = document.querySelectorAll("tbody tr[data-producto-id]");
    filas.forEach(fila => {
        fila.addEventListener("click", () => {
            filas.forEach(f => f.classList.remove("seleccionado"));
            fila.classList.add("seleccionado");
            console.log("Producto seleccionado ID:", fila.dataset.productoId);
        });
    });
});

// Estilo dinámico para fila seleccionada
// (puedes añadirlo en CSS también)
const style = document.createElement("style");
style.innerHTML = `
    .seleccionado {
        background-color: #d1f2eb !important;
    }
`;
document.head.appendChild(style);
