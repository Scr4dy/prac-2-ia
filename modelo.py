from pgmpy.models import DiscreteBayesianNetwork as BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def crear_modelo():
    model = BayesianModel([
        ('Edad', 'COVID'),
        ('Comorbilidad', 'COVID'),
        ('COVID', 'Fiebre'),
        ('COVID', 'Tos'),
        ('COVID', 'Fatiga'),
        ('COVID', 'Olfato'),
        ('COVID', 'Respirar'),

        ('Gripe', 'Fiebre'),
        ('Gripe', 'Tos'),
        ('Gripe', 'Fatiga'),
        ('Gripe', 'Congestion'),

        ('Alergia', 'Tos'),
        ('Alergia', 'Congestion'),
        ('Alergia', 'Olfato'),

        ('Neumonía', 'Dolor'),
        ('Neumonía', 'Respirar'),
        ('Neumonía', 'Fiebre'),

        ('Bronquitis', 'Tos'),
        ('Bronquitis', 'Respirar'),
    ])

    # Variables independientes
    cpd_edad = TabularCPD('Edad', 8, [[0.1], [0.1], [0.1], [0.1], [0.15], [0.15], [0.2], [0.1]])
    cpd_comorb = TabularCPD('Comorbilidad', 2, [[0.75], [0.25]])

    # Probabilidades condicionales para enfermedades
    cpd_covid = TabularCPD('COVID', 2, [
        [0.95, 0.93, 0.90, 0.85, 0.80, 0.70, 0.60, 0.50,
        0.90, 0.85, 0.80, 0.75, 0.70, 0.60, 0.50, 0.40],
        [0.05, 0.07, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50,
        0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60]
    ], evidence=['Edad', 'Comorbilidad'], evidence_card=[8, 2])

    cpd_gripe = TabularCPD('Gripe', 2, [[0.8], [0.2]])
    cpd_alergia = TabularCPD('Alergia', 2, [[0.85], [0.15]])
    cpd_neumonia = TabularCPD('Neumonía', 2, [[0.9], [0.1]])
    cpd_bronquitis = TabularCPD('Bronquitis', 2, [[0.88], [0.12]])

    # Síntomas con múltiples causas
    cpd_fiebre = TabularCPD('Fiebre', 4, [
        [0.6, 0.55, 0.5, 0.4, 0.45, 0.4, 0.35, 0.3],
        [0.2, 0.25, 0.25, 0.3, 0.3, 0.35, 0.35, 0.35],
        [0.15, 0.15, 0.2, 0.2, 0.2, 0.2, 0.2, 0.25],
        [0.05, 0.05, 0.05, 0.1, 0.05, 0.05, 0.1, 0.1],
    ], evidence=['COVID', 'Gripe', 'Neumonía'], evidence_card=[2, 2, 2])

    cpd_tos = TabularCPD('Tos', 4, [
        [0.55, 0.5, 0.45, 0.4, 0.5, 0.4, 0.35, 0.3, 0.45, 0.4, 0.35, 0.3, 0.4, 0.35, 0.3, 0.25],  # corregido columna 8: 0.45 en lugar de 0.5
        [0.25, 0.25, 0.3, 0.3, 0.3, 0.35, 0.4, 0.4, 0.3, 0.35, 0.4, 0.4, 0.3, 0.4, 0.45, 0.5],
        [0.15, 0.2, 0.2, 0.2, 0.15, 0.2, 0.15, 0.15, 0.2, 0.2, 0.15, 0.15, 0.2, 0.15, 0.15, 0.15],
        [0.05, 0.05, 0.05, 0.1, 0.05, 0.05, 0.1, 0.15, 0.05, 0.05, 0.1, 0.15, 0.1, 0.1, 0.1, 0.1],
    ], evidence=['COVID', 'Gripe', 'Alergia', 'Bronquitis'], evidence_card=[2, 2, 2, 2])

    cpd_fatiga = TabularCPD('Fatiga', 4, [
        [0.7, 0.6, 0.5, 0.4],
        [0.15, 0.2, 0.25, 0.25],
        [0.1, 0.15, 0.2, 0.25],
        [0.05, 0.05, 0.05, 0.1],
    ], evidence=['COVID', 'Gripe'], evidence_card=[2, 2])

    cpd_olfato = TabularCPD('Olfato', 2, [
        [0.95, 0.85, 0.75, 0.6],
        [0.05, 0.15, 0.25, 0.4]
    ], evidence=['COVID', 'Alergia'], evidence_card=[2, 2])

    cpd_congestion = TabularCPD('Congestion', 2, [
        [0.9, 0.5, 0.7, 0.2],
        [0.1, 0.5, 0.3, 0.8]
    ], evidence=['Gripe', 'Alergia'], evidence_card=[2, 2])

    cpd_dolor = TabularCPD('Dolor', 2, [
        [0.8, 0.3],
        [0.2, 0.7]
    ], evidence=['Neumonía'], evidence_card=[2])

    cpd_respirar = TabularCPD('Respirar', 2, [
        [0.9, 0.8, 0.7, 0.6, 0.75, 0.65, 0.5, 0.4],
        [0.1, 0.2, 0.3, 0.4, 0.25, 0.35, 0.5, 0.6]
    ], evidence=['COVID', 'Neumonía', 'Bronquitis'], evidence_card=[2, 2, 2])

    model.add_cpds(
        cpd_edad, cpd_comorb, cpd_covid, cpd_gripe, cpd_alergia,
        cpd_neumonia, cpd_bronquitis, cpd_fiebre, cpd_tos, cpd_fatiga,
        cpd_olfato, cpd_congestion, cpd_dolor, cpd_respirar
    )

    assert model.check_model()
    return VariableElimination(model)