from django import forms
from .models import Venta, DetalleVenta
from productos.models import Producto

class DetalleVentaForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(activo=True, stock__gt=0),
        label="Producto"
    )
    
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['producto'].disabled = True

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['paga_con']
        widgets = {
            'paga_con': forms.NumberInput(attrs={
                'step': '0.01', 
                'class': 'form-control',
                'placeholder': '0.00'
            }),
        }