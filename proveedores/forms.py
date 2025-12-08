from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    
    cantidad = forms.IntegerField(min_value=1, required=False)

    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "proveedor_nombre"]


        widgets = {
            'precio': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'cantidad': forms.NumberInput(attrs={'min': '0'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cantidad

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock
