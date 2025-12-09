import os
from fabric import task, Connection, Config
import json

def load_config():
    """Cargar configuración de conexión SSH desde archivo local"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'deploy_config.json')
    
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    
    return config

config = load_config()

SERVER = Connection(
    host=config['host'],
    user=config['user'],
    connect_kwargs={"key_filename": config['ssh_key_path']},
    config=Config(overrides={'sudo': {'password': None}})
)

PROJECT_PATH = config["project_path"]

@task
def deploy_production(c, branch="main"):
    print(f"🚀 Desplegando producción desde {branch}...\n")

    with SERVER.cd(PROJECT_PATH):
        print("📥 Actualizando código...")
        SERVER.run(f"git fetch --all")
        SERVER.run(f"git checkout {branch}")
        SERVER.run(f"git pull origin {branch}")

        print("📦 Instalando dependencias...")
        SERVER.run("venv/bin/pip install -r requirements.txt")

        print("🔄 Aplicando migraciones...")
        SERVER.run("venv/bin/python manage.py migrate")
        
        print("📁 Recolectando archivos estáticos...")
        SERVER.run("venv/bin/python manage.py collectstatic --noinput")

    # ← Los sudo van FUERA del contexto cd()
    print("🔄 Reiniciando servicios...")
    SERVER.sudo("systemctl restart gunicorn")
    SERVER.sudo("systemctl restart nginx")

    print("✅ Producción actualizada!")
    #