from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'stock': 'Stock',
            'activo': 'Activo'
        }
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo')
        return stock
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio

# Formulario para búsqueda de productos
class ProductoBusquedaForm(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )
    
    activo = forms.ChoiceField(
        choices=[('', 'Todos'), ('1', 'Activos'), ('0', 'Inactivos')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def filtrar(self):
        productos = Producto.objects.all()
        
        if self.is_valid():
            nombre = self.cleaned_data.get('nombre')
            activo = self.cleaned_data.get('activo')
            
            if nombre:
                productos = productos.filter(nombre__icontains=nombre)
            
            if activo == '1':
                productos = productos.filter(activo=True)
            elif activo == '0':
                productos = productos.filter(activo=False)
        
        return productos.order_by('nombre')