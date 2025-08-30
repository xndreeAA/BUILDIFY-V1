from flask import Blueprint, jsonify, request, abort, current_app
from flask_login import login_required, current_user
from app.core.models.usuario import Usuario
from app import db
import stripe


usuarios_api_bp = Blueprint('api_usuarios', __name__, url_prefix='/usuarios')

@login_required
@usuarios_api_bp.route('/current_user', methods=['GET'])
def get_current_user():
    
    is_authenticated = current_user.is_authenticated
    
    if is_authenticated:
        return jsonify({
            "success": True, 
            "data": {
                "current_user": current_user.to_dict() if hasattr(current_user, "to_dict") else {
                    "id_usuario": getattr(current_user, "id_usuario", None),
                    "nombre": getattr(current_user, "nombre", None),
                    "apellido": getattr(current_user, "apellido", None),
                    "email": getattr(current_user, "email", None),
                    "direccion": getattr(current_user, "direccion", None),
                    "telefono": getattr(current_user, "telefono", None),
                    "id_rol": getattr(current_user, "id_rol", None),
                    "stripe_customer_id": getattr(current_user, "stripe_customer_id", None)
                }
            }
        })
    return jsonify({"error": "not authenticated"}), 401

@usuarios_api_bp.route('/', methods=['GET', 'POST'])
def api_usuarios():

    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

    if request.method == 'GET':
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
                "password": u.password,
                "stripe_customer_id": u.stripe_customer_id
            } for u in usuarios
        ]
        return jsonify({"success": True, "data": usuarios_data})
    
    elif request.method == 'POST':
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        nuevo_usuario = Usuario(**payload)

        try:
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

            return jsonify({"success": True, "data": {"id_usuario": nuevo_usuario.id_usuario}}), 201

        except stripe.error.StripeError as e:
            db.session.rollback()
            return jsonify({"success": False, "error": f"Error en Stripe: {str(e)}"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)}), 500


@usuarios_api_bp.route('/<int:id_usuario>', methods=['GET', 'PUT', 'DELETE'])
def api_usuario_individual(id_usuario):

    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

    usuario = Usuario.query.get_or_404(id_usuario, description="Usuario no encontrado.")

    if request.method == 'GET':
        return jsonify({
            "success": True,
            "data": {
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "direccion": usuario.direccion,
                "telefono": usuario.telefono,
                "id_rol": usuario.id_rol,
                "password": usuario.password,
                "stripe_customer_id": usuario.stripe_customer_id
            }
        })
    
    elif request.method == 'PUT':
        payload = request.get_json(silent=True)
        if not payload:
            abort(400, description="Request body debe ser JSON válido.")

        campos = ["nombre", "apellido", "email", "direccion", "telefono", "id_rol", "password"]
        for campo in campos:
            if campo not in payload:
                abort(400, description=f"Falta el campo requerido: {campo}")

        try:

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

            usuario.nombre = payload["nombre"]
            usuario.apellido = payload["apellido"]
            usuario.email = payload["email"]
            usuario.direccion = payload["direccion"]
            usuario.telefono = payload["telefono"]
            usuario.id_rol = payload["id_rol"]
            usuario.password = payload["password"]

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error al sincronizar con Stripe: {str(e)}")
            return jsonify({"success": False, "error": "Error al sincronizar con Stripe"}), 500

        return jsonify({"success": True})
    elif request.method == 'DELETE':
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({ "success": True, "data": { "id_usuario": id_usuario }})
