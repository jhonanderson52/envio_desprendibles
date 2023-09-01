#from app.routes import app  # Importa la instancia de la aplicación Flask desde app.py

#if __name__ == '__main__':
#   app.run(debug=True)
from app.routes import app  # Importa la instancia de la aplicación Flask desde app.py
from waitress import serve  # Importa la función serve de Waitress

if __name__ == '__main__':
    # Ejecuta la aplicación con Waitress en el puerto 8080
    serve(app, host='0.0.0.0', port=8080)
