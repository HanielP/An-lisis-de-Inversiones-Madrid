from flask import Flask, render_template, request
import pandas as pd
import joblib

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar el modelo entrenado y el DataFrame de plantilla
modelo = joblib.load('modelo_entrenado.pkl')  # Asegúrate de que el archivo esté en la misma carpeta
plantilla = pd.read_pickle('plantilla_entrada.pkl')  # Este archivo debe tener todas las columnas esperadas

@app.route('/')
def index():
    # Extraer solo los nombres únicos de las categorías para el formulario
    categorias_centro = [col.replace("Centro_", "") for col in plantilla.columns if col.startswith("Centro_")]
    categorias_distrito = [col.replace("Distrito_", "") for col in plantilla.columns if col.startswith("Distrito_")]
    categorias_linea_inversion = [col.replace("LineaInversion_", "") for col in plantilla.columns if col.startswith("LineaInversion_")]
    
    # Renderizar el template HTML con las listas de opciones
    return render_template('index.html', 
                           categorias_centro=categorias_centro, 
                           categorias_distrito=categorias_distrito, 
                           categorias_linea_inversion=categorias_linea_inversion)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Crear una copia del DataFrame de plantilla y establecer todos los valores en 0
        entrada_usuario = plantilla.copy()
        entrada_usuario.loc[:, :] = 0  # Resetea todos los valores a 0 para asegurarse de que partimos desde un estado neutro

        # Obtener los valores de entrada del usuario y asignarlos en el DataFrame
        entrada_usuario.at[0, 'Duración Prevista'] = float(request.form['duracion_prevista'])
        entrada_usuario.at[0, 'Duración Real'] = float(request.form['duracion_real'])
        entrada_usuario.at[0, 'Total previsto de Gasto'] = float(request.form['total_gasto'])

        # Activar las columnas de One-Hot Encoding según la selección del usuario
        entrada_usuario.at[0, f"Centro_{request.form['centro']}"] = 1
        entrada_usuario.at[0, f"Distrito_{request.form['distrito']}"] = 1
        entrada_usuario.at[0, f"LineaInversion_{request.form['linea_inversion']}"] = 1

        # Realizar la predicción
        prediccion = modelo.predict(entrada_usuario)

        # Determinar el mensaje de resultado basado en la predicción
        resultado = "El proyecto finalizará a tiempo." if prediccion[0] == 1 else "El proyecto no finalizará a tiempo."
        
        return render_template('index.html', prediction_text=resultado)

    except Exception as e:
        # En caso de error, mostrar el mensaje de error en la página
        return render_template('index.html', prediction_text=f"Resultado: Ocurrió un error: {e}")

# Ejecutar la aplicación en modo debug
if __name__ == '__main__':
    app.run(debug=True)

import os  # Asegúrate de importar el módulo os al inicio del archivo

if __name__ == '__main__':
    # Heroku asigna un puerto mediante la variable de entorno PORT
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
