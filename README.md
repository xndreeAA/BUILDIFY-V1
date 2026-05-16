# BUILDIFY V1

Plataforma e-commerce especializada en venta de componentes de ordenadores. Sistema completo con autenticación de usuarios, carrito de compras, pagos integrados con Stripe, y gestión de pedidos.

## 🎯 Características

- **Autenticación de Usuarios**: Registro, login, recuperación de contraseña
- **Catálogo de Productos**: Visualización de componentes con filtros y búsqueda
- **Carrito de Compras**: Gestión de items, cálculo de totales
- **Sistema de Pagos**: Integración con Stripe para procesar transacciones
- **Gestión de Pedidos**: Historial de compras, seguimiento de estado
- **Panel de Administración**: Gestión de productos, usuarios y órdenes
- **Email Marketing**: Notificaciones vía SendGrid
- **CDN de Imágenes**: Almacenamiento de assets con Cloudinary
- **API RESTful**: Endpoints para integración frontend

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.10+**
- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM
- **Flask-Login** - Autenticación
- **Flask-JWT-Extended** - Tokens JWT
- **Flask-Mail** - Envío de emails
- **Flask-Migrate** - Migraciones de BD
- **Gunicorn** - Servidor WSGI

### Base de Datos
- **MySQL 5.7+** (producción)
- **SQLAlchemy 2.0** - SQL Toolkit

### Servicios Externos
- **Stripe** - Procesamiento de pagos
- **SendGrid** - Envío de emails
- **Cloudinary** - Almacenamiento de imágenes
- **Supabase** - Base de datos en la nube (opcional)

## 📋 Requisitos Previos

- Python 3.10+
- MySQL 5.7+ instalado y ejecutándose
- Cuenta en Stripe (desarrollo o producción)
- Cuenta en SendGrid
- Cuenta en Cloudinary (opcional)
- Git

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd BUILDIFY-V1
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar el archivo ejemplo y completar con tus credenciales
cp .example.env .env
```

Editar `.env` con tus valores:
```
# Base de Datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3406
DB_NAME=buildify

# Seguridad
SECRET_KEY=tu_clave_secreta_super_segura
JWT_SECRET_KEY=otra_clave_secreta_para_jwt

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_KEY=whsec_...
STRIPE_SUCCESS_URL=http://localhost:5000/pagos/success
STRIPE_CANCEL_URL=http://localhost:5000/pagos/cancel

# SendGrid
SENDGRID_API_KEY=SG.xxx...
SENDGRID_SENDER=noreply@buildify.com

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu_cloud
CLOUDINARY_API_KEY=xxx...
CLOUDINARY_API_SECRET=xxx...

# Supabase (opcional)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyxxxx...
```

### 5. Crear base de datos
```bash
# Crear la BD en MySQL
mysql -u root -p
CREATE DATABASE buildify CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 6. Ejecutar migraciones
```bash
flask db upgrade
```

### 7. Crear usuario administrador (opcional)
```bash
python create_user.py
```

## 🏃 Ejecutar la Aplicación

### Modo Desarrollo
```bash
python run.py
```
La app estará disponible en `http://localhost:5000`

### Modo Producción
```bash
gunicorn run:app --workers 3 --bind 0.0.0.0:8000
```

## 📁 Estructura del Proyecto

```
BUILDIFY-V1/
├── app/
│   ├── core/                 # Configuración y modelos centrales
│   │   ├── models/          # Usuario, Rol
│   │   ├── static/          # CSS, JS, imágenes globales
│   │   └── templates/       # Plantillas base
│   ├── modules/             # Módulos funcionales
│   │   ├── auth/            # Autenticación y recuperación contraseña
│   │   ├── carrito/         # Gestión de carrito
│   │   ├── pagos/           # Integración Stripe
│   │   ├── pedidos/         # Historial de órdenes
│   │   ├── productos/       # Catálogo de componentes
│   │   ├── usuarios/        # Gestión de usuarios
│   │   └── landing/         # Página de inicio
│   ├── interfaces/          # Rutas y blueprints
│   │   ├── api/             # Endpoints REST
│   │   └── web/             # Rutas tradicionales
│   └── config.py            # Configuración por entorno
├── migrations/              # Migraciones de BD (Alembic)
├── database/                # Scripts de BD
├── requirements.txt         # Dependencias Python
├── run.py                   # Punto de entrada
├── .example.env            # Template de variables de entorno
└── Procfile                 # Configuración para Railway/Heroku
```

## 🔑 Variables de Entorno

Ver `.example.env` para lista completa. Variables críticas:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `FLASK_ENV` | Entorno de ejecución | `development` o `production` |
| `SECRET_KEY` | Clave para sesiones | `tu-clave-aleatoria-aqui` |
| `DB_HOST` | Host de MySQL | `localhost` o `db.supabase.co` |
| `STRIPE_SECRET_KEY` | API key de Stripe | `sk_test_...` |
| `SENDGRID_API_KEY` | API key de SendGrid | `SG.xxx...` |

## 🗄️ Base de Datos

### Migraciones

Crear una migración después de cambiar modelos:
```bash
flask db migrate -m "Descripción del cambio"
flask db upgrade
```

Revertir última migración:
```bash
flask db downgrade
```

### Versiones de BD (Historial)

| Versión | Cambio |
|---------|--------|
| 2.0 | Creación inicial |
| 3.0 | Correcciones de formato SQL |
| 4.0 | Implementación cascada |
| 4.1 | Refactorización cascada |
| 5.0 | Nuevas columnas |
| 5.1-5.4 | Ajustes y tablas de carrito |
| 6.0-6.1 | Integración Stripe |

## 🔗 API Endpoints

### Autenticación
- `POST /api/v1/auth/register` - Registrar usuario
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout
- `POST /api/v1/auth/forgot-password` - Solicitar reset

### Productos
- `GET /api/v1/productos` - Listar productos
- `GET /api/v1/productos/<id>` - Detalles de producto
- `POST /api/v1/productos` - Crear (admin)
- `PUT /api/v1/productos/<id>` - Actualizar (admin)
- `DELETE /api/v1/productos/<id>` - Eliminar (admin)

### Carrito
- `GET /api/v1/carrito` - Ver carrito
- `POST /api/v1/carrito/items` - Agregar item
- `PUT /api/v1/carrito/items/<id>` - Actualizar cantidad
- `DELETE /api/v1/carrito/items/<id>` - Eliminar item

### Pagos
- `POST /api/v1/pagos/checkout` - Crear sesión Stripe
- `POST /api/v1/pagos/webhook` - Webhook de Stripe

### Pedidos
- `GET /api/v1/pedidos` - Mis pedidos
- `GET /api/v1/pedidos/<id>` - Detalles del pedido

### Usuarios
- `GET /api/v1/usuarios/perfil` - Mi perfil
- `PUT /api/v1/usuarios/perfil` - Actualizar perfil

## 🔐 Seguridad

- Contraseñas hasheadas con Werkzeug
- CSRF protection en formularios
- JWT para APIs
- SQL Injection prevención con SQLAlchemy
- Validación de entrada en todas las rutas
- HTTPS en producción (SESSION_COOKIE_SECURE = True)

## 📧 Email

Sistema integrado con SendGrid:
- Confirmación de registro
- Recuperación de contraseña
- Notificaciones de pedido

## 💳 Integraciones Stripe

### Desarrollo
```bash
# Usar claves de testing
STRIPE_SECRET_KEY=sk_test_...
```

### Webhooks
Registrar webhook en dashboard de Stripe apuntando a:
```
https://tu-dominio.com/api/v1/pagos/webhook
```

Eventos manejados:
- `checkout.session.completed` - Pago completado
- `payment_intent.succeeded` - Intención de pago exitosa

## 🚀 Despliegue

### Railway
```bash
# 1. Conectar repositorio
# 2. Agregar variables de entorno en Railway dashboard
# 3. Railway detectará Procfile y desplegará automáticamente
```

### Heroku
```bash
heroku login
heroku create tu-app-name
git push heroku main
heroku config:set VARIABLE=valor
```

## 🐛 Debugging

Activar logs detallados:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Ver logs en producción:
```bash
# Railway
railway logs

# Heroku
heroku logs --tail
```

## 📦 Dependencias Principales

Ver `requirements.txt` para lista completa.

- flask==3.1.1
- flask-sqlalchemy==3.1.1
- flask-login==0.6.3
- flask-jwt-extended==4.7.1
- stripe==12.3.0
- sendgrid==6.12.5
- cloudinary==1.44.1
- flask-migrate==4.1.0

## 🤝 Contribuir

1. Crear una rama para tu feature: `git checkout -b feature/my-feature`
2. Commit cambios: `git commit -am 'Add my feature'`
3. Push a la rama: `git push origin feature/my-feature`
4. Crear Pull Request

## 📝 Licencia

Proyecto privado. Todos los derechos reservados.

## 👤 Autor

**Cairon29** (Jose W. Junco)

## 📞 Soporte

Para reportar bugs o solicitar features, crear un issue en el repositorio.

---

**Última actualización**: Mayo 2026  
**Versión actual**: 1.0
