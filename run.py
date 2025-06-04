# Punto de entrada para ejecutar la aplicación Flask

# Importa la función create_app desde el paquete app __init__.py
from app import create_app 
# Crea una instancia de la aplicación Flask
app = create_app()
#solo se ejecuta si este archivo es el principal
# y no si es importado como un módulo
if __name__ == '__main__':
    app.run(debug=True)
