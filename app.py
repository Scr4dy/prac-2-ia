# app.py
from flask import Flask, request, send_from_directory, render_template_string
from modelo import crear_modelo

app = Flask(__name__)
inferencia = crear_modelo()

@app.route('/')
def home():
    return send_from_directory('.', 'formulario.html')


@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    sintomas = {
        'Fiebre': int(request.form['fiebre']),
        'Tos': int(request.form['tos']),
        'Fatiga': int(request.form['fatiga']),
        'Olfato': int(request.form['olfato']),
        'Congestion': int(request.form['congestion']),
        'Dolor': int(request.form['dolor']),
        'Respirar': int(request.form['respirar']),
        'Edad': int(request.form['edad']),
        'Comorbilidad': int(request.form['comorbilidad'])
    }

    enfermedades = {}
    for enfermedad in ['COVID', 'Gripe', 'Alergia', 'Neumonía', 'Bronquitis']:
        resultado = inferencia.query([enfermedad], evidence=sintomas)
        prob = float(resultado.values[1])  # valor del estado 'sí'
        enfermedades[enfermedad] = round(prob, 3)

    with open('resultado.html', 'r', encoding='utf-8') as f:
        plantilla = f.read()

    return render_template_string(plantilla, enfermedades=enfermedades)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
