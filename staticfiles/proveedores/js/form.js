document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const inputs = form.querySelectorAll("input, textarea, select");

    // Validación rápida en frontend
    form.addEventListener("submit", function (e) {
        let valid = true;
        inputs.forEach(input => {
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

    // Feedback visual al escribir
    inputs.forEach(input => {
        input.addEventListener("input", () => {
            input.style.borderColor = "#3498db";
        });
    });
});
