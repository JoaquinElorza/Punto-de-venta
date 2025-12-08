/**
 * Punto de Venta - JavaScript
 * Funcionalidades para el sistema POS
 */

// Clase principal para manejar la venta
class PuntoVenta {
    constructor() {
        this.ventaTotal = parseFloat(document.getElementById('venta-total')?.textContent || 0);
        this.ventaId = document.getElementById('paga_con')?.dataset.ventaId || 0;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFormValidation();
        this.setupRealTimeCalculations();
    }

    setupEventListeners() {
        // Validación del formulario de pago
        const pagoForm = document.getElementById('pago-form');
        if (pagoForm) {
            pagoForm.addEventListener('submit', (e) => this.validarPago(e));
        }

        // Cálculo de cambio en tiempo real
        const pagaConInput = document.getElementById('paga_con');
        if (pagaConInput) {
            pagaConInput.addEventListener('input', () => this.calcularCambioEnTiempoReal());
            pagaConInput.addEventListener('blur', () => this.formatearPagoInput());
        }

        // Confirmación para acciones críticas
        this.setupConfirmaciones();
    }

    setupFormValidation() {
        const inputs = document.querySelectorAll('input[type="number"], input[required]');
        inputs.forEach(input => {
            input.addEventListener('invalid', (e) => {
                this.mostrarErrorInput(e.target);
            });
            
            input.addEventListener('input', (e) => {
                this.limpiarErrorInput(e.target);
            });
        });
    }

    setupRealTimeCalculations() {
        // Inicializar cálculo de cambio si hay valor en el input
        const pagaConInput = document.getElementById('paga_con');
        if (pagaConInput && pagaConInput.value) {
            this.calcularCambioEnTiempoReal();
        }
    }

    setupConfirmaciones() {
        // Ya están configuradas en el HTML con onclick
        console.log('Confirmaciones configuradas');
    }

    validarPago(event) {
        const pagaCon = parseFloat(document.getElementById('paga_con').value) || 0;
        
        // Validaciones
        const validaciones = [
            {
                condicion: this.ventaTotal === 0,
                mensaje: 'No hay productos en la venta.',
                preventDefault: true
            },
            {
                condicion: pagaCon === 0,
                mensaje: 'Por favor ingrese la cantidad con la que paga el cliente.',
                preventDefault: true
            },
            {
                condicion: pagaCon < this.ventaTotal,
                mensaje: 'El pago es menor al total. Por favor ingrese una cantidad mayor.',
                preventDefault: true
            }
        ];

        for (const validacion of validaciones) {
            if (validacion.condicion) {
                this.mostrarAlerta(validacion.mensaje, 'error');
                if (validacion.preventDefault) {
                    event.preventDefault();
                }
                return false;
            }
        }

        // Confirmación final
        if (!confirm('¿Finalizar venta?')) {
            event.preventDefault();
            return false;
        }

        return true;
    }

    calcularCambioEnTiempoReal() {
        const pagaConInput = document.getElementById('paga_con');
        const cambioElement = document.getElementById('cambio-mensaje');
        
        if (!pagaConInput || !cambioElement) return;

        const pagaCon = parseFloat(pagaConInput.value) || 0;
        const cambio = pagaCon - this.ventaTotal;

        if (pagaCon > 0 && cambio >= 0) {
            cambioElement.textContent = `Cambio: $${cambio.toFixed(2)}`;
            cambioElement.classList.remove('hidden');
            cambioElement.classList.add('visible');
            
            // Cambiar color según el cambio
            if (cambio === 0) {
                cambioElement.style.background = 'linear-gradient(135deg, #d1fae5, #a7f3d0)';
                cambioElement.style.borderColor = '#34d399';
                cambioElement.style.color = '#065f46';
            } else {
                cambioElement.style.background = 'linear-gradient(135deg, #e0f2fe, #bae6fd)';
                cambioElement.style.borderColor = '#7dd3fc';
                cambioElement.style.color = '#0369a1';
            }
        } else {
            cambioElement.classList.remove('visible');
            cambioElement.classList.add('hidden');
        }
    }

    formatearPagoInput() {
        const input = document.getElementById('paga_con');
        if (!input) return;

        const valor = parseFloat(input.value);
        if (!isNaN(valor) && valor > 0) {
            input.value = valor.toFixed(2);
        }
    }

    mostrarErrorInput(input) {
        input.style.borderColor = 'var(--danger-color)';
        input.style.boxShadow = '0 0 0 3px rgba(220, 38, 38, 0.1)';
        
        // Crear mensaje de error si no existe
        if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('error-mensaje')) {
            const errorMsg = document.createElement('div');
            errorMsg.className = 'error-mensaje';
            errorMsg.style.color = 'var(--danger-color)';
            errorMsg.style.fontSize = '0.875rem';
            errorMsg.style.marginTop = '0.25rem';
            errorMsg.textContent = 'Por favor ingrese un valor válido';
            input.parentNode.appendChild(errorMsg);
        }
    }

    limpiarErrorInput(input) {
        input.style.borderColor = '';
        input.style.boxShadow = '';
        
        // Remover mensaje de error si existe
        const errorMsg = input.nextElementSibling;
        if (errorMsg && errorMsg.classList.contains('error-mensaje')) {
            errorMsg.remove();
        }
    }

    mostrarAlerta(mensaje, tipo = 'info') {
        // Crear alerta temporal
        const alerta = document.createElement('div');
        alerta.className = `alerta-temporal alerta-${tipo}`;
        alerta.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            background: ${tipo === 'error' ? '#fee2e2' : '#d1fae5'};
            color: ${tipo === 'error' ? '#991b1b' : '#065f46'};
            border: 2px solid ${tipo === 'error' ? '#fecaca' : '#a7f3d0'};
            z-index: 9999;
            animation: slideIn 0.3s ease-out;
            box-shadow: var(--shadow-lg);
            font-weight: 500;
            max-width: 300px;
        `;
        
        // Crear CSS para animación si no existe
        if (!document.getElementById('alerta-estilos')) {
            const style = document.createElement('style');
            style.id = 'alerta-estilos';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        alerta.textContent = mensaje;
        document.body.appendChild(alerta);

        // Auto-remover después de 3 segundos
        setTimeout(() => {
            alerta.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => alerta.remove(), 300);
        }, 3000);
    }

    // Método para actualizar el total si cambia dinámicamente
    actualizarTotal(nuevoTotal) {
        this.ventaTotal = parseFloat(nuevoTotal);
        const totalElement = document.getElementById('venta-total');
        if (totalElement) {
            totalElement.textContent = nuevoTotal.toFixed(2);
        }
        // Recalcular cambio si hay valor en el input
        this.calcularCambioEnTiempoReal();
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.puntoVenta = new PuntoVenta();
    
    // Hacer disponible para debugging
    console.log('Punto de Venta JavaScript cargado');
    console.log('Total de venta:', window.puntoVenta.ventaTotal);
    console.log('ID de venta:', window.puntoVenta.ventaId);
});

// Utilidades adicionales
const Utilidades = {
    formatearDinero: (cantidad) => {
        return new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: 'MXN'
        }).format(cantidad);
    },

    validarNumeroPositivo: (valor) => {
        const num = parseFloat(valor);
        return !isNaN(num) && num >= 0;
    },

    mostrarCargando: (mostrar = true) => {
        if (mostrar) {
            const cargando = document.createElement('div');
            cargando.id = 'cargando-overlay';
            cargando.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            `;
            cargando.innerHTML = `
                <div style="text-align: center;">
                    <div style="
                        width: 40px;
                        height: 40px;
                        border: 3px solid #e2e8f0;
                        border-top-color: #2563eb;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                        margin: 0 auto 1rem;
                    "></div>
                    <p style="color: #475569; font-weight: 500;">Procesando...</p>
                </div>
            `;
            document.body.appendChild(cargando);
        } else {
            const cargando = document.getElementById('cargando-overlay');
            if (cargando) cargando.remove();
        }
    }
};

// Añadir utilidades al objeto global
window.Utilidades = Utilidades;