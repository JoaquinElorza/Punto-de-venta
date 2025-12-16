# Sistema Punto de Venta

Sistema web desarrollado con Django para la gestión de ventas, productos y usuarios con roles.

## Requisitos
- Python 3.11
- Django
- Gestor de base de datos (PostgreSQL / MySQL)
- pip

## Instalación
```bash
git clone https://github.com/usuario/punto-de-venta.git
cd punto-de-venta
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Variables de entorno
Crear un archivo .env en la raíz del proyecto:
SECRET_KEY=
DEBUG=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
No subir el archivo .env al repositorio.

## Inicialización
python manage.py migrate
python manage.py collectstatic
python manage.py runserver

## Produccion
El sistema se encuentra desplegado en PythonAnywhere:
https://baruc.pythonanywhere.com

