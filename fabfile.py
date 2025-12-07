from fabric import task, Connection
import json

def load_config():
    """Cargar configuración desde archivo local"""
    with open('deploy_config.json') as f:
        return json.load(f)

config = load_config()

# Conexión global para todas las tareas
SERVER = Connection(
    host=config["host"],
    user=config["user"],
    connect_kwargs={
        "key_filename": config["ssh_key_path"]
    }
)

PROJECT_PATH = config["project_path"]

@task
def deploy_production(c, branch="main"):
    print(f"🚀 Desplegando producción desde {branch}...\n")

    with SERVER.cd(PROJECT_PATH):
        SERVER.run(f"git fetch --all")
        SERVER.run(f"git checkout {branch}")
        SERVER.run(f"git pull origin {branch}")

        c.run("venv/bin/pip install -r requirements.txt")


        SERVER.run("venv/bin/python manage.py migrate")
        SERVER.run("venv/bin/python manage.py collectstatic --noinput")

        SERVER.sudo("systemctl restart gunicorn")
        SERVER.sudo("systemctl restart nginx")

    print("✅ Producción actualizada!")
