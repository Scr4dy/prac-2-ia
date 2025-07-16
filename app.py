from flask import Flask, request, render_template
from modelo import crear_modelo

app = Flask(__name__)
inferencia = crear_modelo()

# Lista de nombres de síntomas esperados
SINTOMAS = [
    'Fiebre', 'Tos', 'Fatiga', 'Olfato', 'Congestion',
    'Dolor', 'Respirar', 'Edad', 'Comorbilidad'
]

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    try:
        # Extrae y convierte los valores desde el formulario
        sintomas = {sintoma: int(request.form[sintoma.lower()]) for sintoma in SINTOMAS}
    except (KeyError, ValueError):
        return "Error: Faltan datos o uno o más campos tienen formato incorrecto.", 400

    # Diagnóstico de enfermedades
    enfermedades = {}
    for enfermedad in ['COVID', 'Gripe', 'Alergia', 'Neumonía', 'Bronquitis']:
        resultado = inferencia.query([enfermedad], evidence=sintomas)
        prob = float(resultado.values[1])  # type: ignore
        enfermedades[enfermedad] = round(prob, 3)

    return render_template('resultado.html', enfermedades=enfermedades)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)