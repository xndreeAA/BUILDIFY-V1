# script_crear_usuario.py

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.core.models.usuario import Usuario

app = create_app()

with app.app_context():
    nuevo_usuario = Usuario(
        nombre="AdminBuildify",
        apellido="De Prueba",
        email="admin2@buildify.com",
        direccion="Calle Falsa 123",
        telefono="123456789",
        id_rol=3
    )

    nuevo_usuario.set_password("1234")  # Encriptar la contraseña
    db.session.add(nuevo_usuario)
    
    try:
        db.session.commit()
        print("✅ Usuario creado correctamente.")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al crear el usuario: {e}")
