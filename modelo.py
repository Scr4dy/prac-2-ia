# modelo.py
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

    # CPDs base
    cpd_edad = TabularCPD('Edad', 2, [[0.6], [0.4]])  # 0: <60, 1: >=60
    cpd_comorb = TabularCPD('Comorbilidad', 2, [[0.75], [0.25]])

    # CPDs de enfermedades
    cpd_covid = TabularCPD('COVID', 2, [
        [0.95, 0.85, 0.7, 0.5],
        [0.05, 0.15, 0.3, 0.5]
    ], evidence=['Edad', 'Comorbilidad'], evidence_card=[2, 2])

    cpd_gripe = TabularCPD('Gripe', 2, [[0.85], [0.15]])
    cpd_alergia = TabularCPD('Alergia', 2, [[0.9], [0.1]])
    cpd_neumonia = TabularCPD('Neumonía', 2, [[0.95], [0.05]])
    cpd_bronquitis = TabularCPD('Bronquitis', 2, [[0.9], [0.1]])

    # Síntomas

    cpd_fiebre = TabularCPD('Fiebre', 2, [
    [0.95, 0.85, 0.75, 0.65, 0.7, 0.6, 0.5, 0.4],
    [0.05, 0.15, 0.25, 0.35, 0.3, 0.4, 0.5, 0.6]
    ], evidence=['COVID', 'Gripe', 'Neumonía'], evidence_card=[2, 2, 2])


    cpd_tos = TabularCPD('Tos', 2, [
        [0.9, 0.8, 0.7, 0.6, 0.8, 0.7, 0.6, 0.5,
        0.7, 0.6, 0.5, 0.4, 0.6, 0.5, 0.4, 0.3],
        [0.1, 0.2, 0.3, 0.4, 0.2, 0.3, 0.4, 0.5,
        0.3, 0.4, 0.5, 0.6, 0.4, 0.5, 0.6, 0.7]
    ], evidence=['COVID', 'Gripe', 'Alergia', 'Bronquitis'], evidence_card=[2, 2, 2, 2])

    cpd_fatiga = TabularCPD('Fatiga', 2, [
        [0.9, 0.7, 0.6, 0.4],
        [0.1, 0.3, 0.4, 0.6]
    ], evidence=['COVID', 'Gripe'], evidence_card=[2, 2])

    cpd_olfato = TabularCPD('Olfato', 2, [
        [0.9, 0.6, 0.8, 0.3],
        [0.1, 0.4, 0.2, 0.7]
    ], evidence=['COVID', 'Alergia'], evidence_card=[2, 2])

    cpd_congestion = TabularCPD('Congestion', 2, [
        [0.9, 0.5, 0.7, 0.2],
        [0.1, 0.5, 0.3, 0.8]
    ], evidence=['Gripe', 'Alergia'], evidence_card=[2, 2])

    cpd_dolor = TabularCPD('Dolor', 2, [
        [0.7, 0.3],
        [0.3, 0.7]
    ], evidence=['Neumonía'], evidence_card=[2])

    cpd_respirar = TabularCPD('Respirar', 2, [
        [0.95, 0.9, 0.85, 0.8, 0.7, 0.65, 0.6, 0.5],
        [0.05, 0.1, 0.15, 0.2, 0.3, 0.35, 0.4, 0.5]
    ], evidence=['COVID', 'Neumonía', 'Bronquitis'], evidence_card=[2, 2, 2])

    model.add_cpds(
        cpd_edad, cpd_comorb, cpd_covid, cpd_gripe, cpd_alergia,
        cpd_neumonia, cpd_bronquitis, cpd_fiebre, cpd_tos, cpd_fatiga,
        cpd_olfato, cpd_congestion, cpd_dolor, cpd_respirar
    )

    assert model.check_model()
    return VariableElimination(model)
