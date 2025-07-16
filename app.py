from flask import Flask, request, render_template
from modelo import crear_modelo

app = Flask(__name__)
inferencia = crear_modelo()

# Lista de nombres de síntomas esperados (según el formulario)
SINTOMAS = [
    'fiebre', 'tos', 'fatiga', 'olfato', 'congestion',
    'dolor', 'respirar', 'edad', 'comorbilidad'
]

# Mapeo a nombres usados en el modelo
form_to_model = {
    'fiebre': 'Fiebre',
    'tos': 'Tos',
    'fatiga': 'Fatiga',
    'olfato': 'Olfato',
    'congestion': 'Congestion',
    'dolor': 'Dolor',
    'respirar': 'Respirar',
    'edad': 'Edad',
    'comorbilidad': 'Comorbilidad'
}

# Síntomas relacionados por enfermedad (en minúscula como en el formulario)
sintomas_por_enfermedad = {
    "COVID": ["fiebre", "tos", "fatiga", "olfato", "respirar"],
    "Gripe": ["fiebre", "tos", "fatiga", "congestion"],
    "Alergia": ["tos", "congestion", "olfato"],
    "Neumonía": ["dolor", "respirar", "fiebre"],
    "Bronquitis": ["tos", "respirar"]
}

# Recomendaciones de medicamentos por síntoma
recomendaciones = {
    "fiebre": [
        {"medicamento": "Paracetamol", "requiere_receta": False},
        {"medicamento": "Ibuprofeno", "requiere_receta": False}
    ],
    "tos": [
        {"medicamento": "Ambroxol", "requiere_receta": False},
        {"medicamento": "Codeína", "requiere_receta": True}
    ],
    "fatiga": [
        {"medicamento": "Complejo B", "requiere_receta": False}
    ],
    "dolor": [
        {"medicamento": "Naproxeno", "requiere_receta": True}
    ],
    "congestion": [
        {"medicamento": "Loratadina", "requiere_receta": False}
    ],
    "olfato": [
        {"medicamento": "Consulta con otorrinolaringólogo", "requiere_receta": True}
    ],
    "respirar": [
        {"medicamento": "Salbutamol (inhalador)", "requiere_receta": True}
    ]
}

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    try:
        # Extraer síntomas del formulario
        sintomas_form = {sintoma: int(request.form[sintoma]) for sintoma in SINTOMAS}
    except (KeyError, ValueError):
        return "Error: Faltan datos o uno o más campos tienen formato incorrecto.", 400

    # Convertir claves a las usadas por el modelo bayesiano
    sintomas = {form_to_model[k]: v for k, v in sintomas_form.items()}

    # Diagnóstico de enfermedades
    enfermedades = {}
    for enfermedad in ['COVID', 'Gripe', 'Alergia', 'Neumonía', 'Bronquitis']:
        resultado = inferencia.query([enfermedad], evidence=sintomas)
        prob = float(resultado.values[1])  # type: ignore
        enfermedades[enfermedad] = round(prob, 3)

    # Recomendaciones según síntomas vinculados a enfermedades con prob > 0.40
    recomendaciones_por_enfermedad = {}
    for enfermedad, probabilidad in enfermedades.items():
        if probabilidad >= 0.40:
            sintomas_relacionados = sintomas_por_enfermedad.get(enfermedad, [])
            for sintoma in sintomas_relacionados:
                if sintoma in recomendaciones and sintoma not in recomendaciones_por_enfermedad:
                    recomendaciones_por_enfermedad[sintoma] = recomendaciones[sintoma]

    return render_template(
        "resultado.html",
        enfermedades=enfermedades,
        recomendaciones_por_enfermedad=recomendaciones_por_enfermedad
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)