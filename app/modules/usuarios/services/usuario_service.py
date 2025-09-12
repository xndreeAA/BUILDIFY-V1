import stripe
from flask import request, current_app
from flask_login import current_user
from app import db
from app.core.models.usuario import Usuario

class UsuarioService:
    
    @staticmethod
    def obtener_current_user(*args, **kwargs):        
        # Retorna el usuario autenticado actual (solo id_usuario para mayor seguridad)
        is_authenticated = current_user.is_authenticated
        
        if is_authenticated:
            return {
                "success": True, 
                "data": {
                    "id_usuario": getattr(current_user, "id_usuario", None)
                }
            }, 200
        return {"error": "not authenticated"}, 401
    
    @staticmethod
    def obtener_usuarios(*args, **kwargs):        
        # Se obtienen todos los usuarios sin exponer el hash de contraseña
        usuarios = Usuario.query.all()
        usuarios_data = [
            {
                "id_usuario": u.id_usuario,
                "nombre": u.nombre,
                "apellido": u.apellido,
                "email": u.email,
                "direccion": u.direccion,
                "telefono": u.telefono,
                "id_rol": u.id_rol,
                "rol_nombre": u.rol_rel.rol if u.rol_rel else None,  # 👈 agregado
                "stripe_customer_id": u.stripe_customer_id
            } for u in usuarios
        ]
        return {"success": True, "data": usuarios_data}, 200
    
    @staticmethod
    def crear_usuario(payload):
        # Configuración de Stripe en cada operación que lo requiera
        stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

        # Se inicializa el nuevo usuario sin exponer password plano
        nuevo_usuario = Usuario(
            nombre=payload.get("nombre"),
            apellido=payload.get("apellido"),
            email=payload.get("email"),
            direccion=payload.get("direccion"),
            telefono=payload.get("telefono"),
            id_rol=payload.get("id_rol")
        )

        # Password se maneja con hashing seguro mediante set_password()
        if payload.get("password"):
            nuevo_usuario.set_password(payload.get("password"))

        try:
            # Si no tiene customer en Stripe, se crea automáticamente
            if not nuevo_usuario.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=payload.get("email"),
                    name=f"{payload.get('nombre')} {payload.get('apellido')}",
                    address={
                        "line1": payload.get("direccion"),
                        "country": "CO"
                    }
                )
                nuevo_usuario.stripe_customer_id = customer.id
            else:
                # Validación de cliente existente en Stripe
                try:
                    stripe.Customer.retrieve(nuevo_usuario.stripe_customer_id)
                except stripe.error.InvalidRequestError:
                    customer = stripe.Customer.create(
                        email=payload.get("email"),
                        name=f"{payload.get('nombre')} {payload.get('apellido')}",
                        address={
                            "line1": payload.get("direccion"),
                            "country": "CO"
                        }
                    )
                    nuevo_usuario.stripe_customer_id = customer.id

            db.session.add(nuevo_usuario)
            db.session.commit()

            return {"success": True, "data": {"id_usuario": nuevo_usuario.id_usuario}}, 201

        # Manejo específico de errores de Stripe y rollback en DB
        except stripe.error.StripeError as e:
            db.session.rollback()
            return {"success": False, "error": f"Error en Stripe: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}, 500
        
    @staticmethod
    def traer_un_usuario(id_usuario):
        # Obtiene un usuario por ID sin exponer hash de password
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return {"success": False, "error": "Usuario no encontrado."}, 404
        
        return {
            "success": True,
            "data": {
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "direccion": usuario.direccion,
                "telefono": usuario.telefono,
                "id_rol": usuario.id_rol,
                "rol_nombre": usuario.rol_rel.rol if usuario.rol_rel else None,  # 👈 agregado
                "stripe_customer_id": usuario.stripe_customer_id
            }
        }, 200

    @staticmethod
    def modificar_un_usuario(id_usuario, payload):
        # Configuración de Stripe en cada actualización
        stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return {"success": False, "error": "Usuario no encontrado."}, 404
        
        try:
            # Si no existe cliente en Stripe, se crea; si ya existe, se actualiza
            if not usuario.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=payload["email"],
                    name=f"{payload['nombre']} {payload['apellido']}",
                    address={
                        "line1": payload["direccion"],
                        "country": "CO"
                    }
                )
                usuario.stripe_customer_id = customer.id
            else:
                stripe.Customer.modify(
                    usuario.stripe_customer_id,
                    email=payload["email"],
                    name=f"{payload['nombre']} {payload['apellido']}",
                    address={
                        "line1": payload["direccion"],
                        "country": "CO"
                    }
                )

            # Actualización de datos del usuario en la DB
            usuario.nombre = payload["nombre"]
            usuario.apellido = payload["apellido"]
            usuario.email = payload["email"]
            usuario.direccion = payload["direccion"]
            usuario.telefono = payload["telefono"]
            usuario.id_rol = payload["id_rol"]

            # Hash seguro de password si se actualiza
            if "password" in payload and payload["password"]:
                usuario.set_password(payload["password"])

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error al sincronizar con Stripe: {str(e)}")
            return {"success": False, "error": "Error al sincronizar con Stripe"}, 500

        return {"success": True}, 200
    
    @staticmethod
    def eliminar_un_usuario(id_usuario):
        # Eliminación de usuario en DB (no elimina cliente en Stripe por seguridad)
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return {"success": False, "error": "Usuario no encontrado."}, 404
        
        db.session.delete(usuario)
        db.session.commit()
        
        return { "success": True, "data": { "id_usuario": id_usuario }}, 200
