"""
Medical Diagnosis Knowledge Base
Contains rules and initial facts for the medical diagnosis expert system.
"""
from expert_system_core import Rule, Fact

def load_medical_knowledge_base():
    """
    Load the medical knowledge base with rules for diagnosis.
    Returns a list of rules for the expert system.
    """
    rules = [
        # Flu diagnosis rules
        Rule(
            name="R1",
            antecedents=["fever", "headache", "body_ache"],
            consequents=["possible_flu"],
            description="Basic flu symptoms suggest possible flu"
        ),
        Rule(
            name="R2",
            antecedents=["possible_flu", "sore_throat"],
            consequents=["likely_flu"],
            description="Flu symptoms with sore throat increase likelihood of flu"
        ),
        Rule(
            name="R3",
            antecedents=["likely_flu", "fatigue"],
            consequents=["flu"],
            description="Comprehensive flu symptoms confirm flu diagnosis"
        ),
        
        # COVID-19 diagnosis rules
        Rule(
            name="R4",
            antecedents=["fever", "dry_cough"],
            consequents=["possible_covid"],
            description="Basic COVID symptoms suggest possible COVID-19"
        ),
        Rule(
            name="R5",
            antecedents=["possible_covid", "loss_of_taste"],
            consequents=["likely_covid"],
            description="COVID symptoms with taste loss increase COVID likelihood"
        ),
        Rule(
            name="R6",
            antecedents=["likely_covid", "shortness_of_breath"],
            consequents=["covid"],
            description="Severe symptoms confirm COVID-19 diagnosis"
        ),
        
        # Common cold diagnosis rules
        Rule(
            name="R7",
            antecedents=["runny_nose", "sneezing"],
            consequents=["possible_cold"],
            description="Basic cold symptoms suggest possible common cold"
        ),
        Rule(
            name="R8",
            antecedents=["possible_cold", "sore_throat"],
            consequents=["cold"],
            description="Cold symptoms with sore throat confirm common cold"
        ),
        
        # Allergic reaction rules
        Rule(
            name="R9",
            antecedents=["sneezing", "itchy_eyes"],
            consequents=["possible_allergy"],
            description="Basic allergy symptoms suggest possible allergic reaction"
        ),
        Rule(
            name="R10",
            antecedents=["possible_allergy", "runny_nose", "no_fever"],
            consequents=["allergy"],
            description="Allergy symptoms without fever confirm allergic reaction"
        ),
        
        # Treatment recommendation rules
        Rule(
            name="T1",
            antecedents=["flu"],
            consequents=["recommend_rest", "recommend_fluids", "consider_antiviral"],
            description="Standard flu treatment recommendations"
        ),
        Rule(
            name="T2",
            antecedents=["covid"],
            consequents=["recommend_isolation", "recommend_rest", "monitor_oxygen_levels"],
            description="Standard COVID-19 treatment recommendations"
        ),
        Rule(
            name="T3",
            antecedents=["cold"],
            consequents=["recommend_rest", "recommend_fluids", "consider_decongestant"],
            description="Standard cold treatment recommendations"
        ),
        Rule(
            name="T4",
            antecedents=["allergy"],
            consequents=["recommend_antihistamine", "avoid_allergens"],
            description="Standard allergy treatment recommendations"
        ),
        
        # Test recommendation rules
        Rule(
            name="D1",
            antecedents=["possible_covid"],
            consequents=["recommend_covid_test"],
            description="Recommend COVID test for possible COVID cases"
        ),
        Rule(
            name="D2",
            antecedents=["possible_flu", "winter_season"],
            consequents=["recommend_flu_test"],
            description="Recommend flu test for possible flu during winter"
        ),
        
        # Negation rules
        Rule(
            name="N1",
            antecedents=["no_fever", "runny_nose"],
            consequents=["unlikely_flu"],
            description="Without fever, flu is less likely"
        ),
        Rule(
            name="N2",
            antecedents=["no_cough", "no_shortness_of_breath"],
            consequents=["unlikely_covid"],
            description="Without respiratory symptoms, COVID is less likely"
        )
    ]
    
    return rules

def get_symptom_descriptions():
    """
    Returns descriptions of symptoms for the user interface.
    """
    return {
        "fever": "Elevated body temperature above normal",
        "headache": "Pain or discomfort in the head",
        "body_ache": "Pain or soreness in muscles",
        "sore_throat": "Pain or irritation in the throat",
        "fatigue": "Feeling of extreme tiredness or exhaustion",
        "dry_cough": "Cough without producing mucus",
        "loss_of_taste": "Diminished ability to taste food",
        "shortness_of_breath": "Difficulty breathing or catching breath",
        "runny_nose": "Excess nasal drainage or discharge",
        "sneezing": "Sudden, forceful expulsion of air through nose/mouth",
        "itchy_eyes": "Irritation and itchiness in the eyes",
        "winter_season": "Currently in winter months",
        "no_fever": "Normal body temperature",
        "no_cough": "Absence of coughing",
        "no_shortness_of_breath": "Normal breathing"
    }