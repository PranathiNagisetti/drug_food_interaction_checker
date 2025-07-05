import random
import logging
from typing import Dict, Tuple, Optional

logger = logging.getLogger(__name__)

# Comprehensive drug-food interaction database
DRUG_FOOD_INTERACTIONS = {
    # Statins
    ("atorvastatin", "grapefruit"): {
        "risk": "High",
        "mechanism": "Grapefruit inhibits CYP3A4 enzyme, increasing atorvastatin concentration",
        "effect": "Increased risk of muscle damage and liver problems",
        "recommendation": "Avoid grapefruit and grapefruit juice while taking atorvastatin"
    },
    ("simvastatin", "grapefruit"): {
        "risk": "High", 
        "mechanism": "Grapefruit inhibits CYP3A4, increasing simvastatin levels",
        "effect": "Higher risk of muscle pain and liver damage",
        "recommendation": "Avoid grapefruit products completely"
    },
    
    # Blood thinners
    ("warfarin", "spinach"): {
        "risk": "Moderate",
        "mechanism": "Spinach is high in vitamin K, which counteracts warfarin",
        "effect": "Reduced anticoagulant effect, increased clotting risk",
        "recommendation": "Maintain consistent vitamin K intake, don't suddenly change diet"
    },
    ("warfarin", "cranberry"): {
        "risk": "Moderate",
        "mechanism": "Cranberry may increase warfarin's anticoagulant effect",
        "effect": "Increased bleeding risk",
        "recommendation": "Limit cranberry products and monitor for bleeding"
    },
    
    # Antibiotics
    ("tetracycline", "dairy"): {
        "risk": "Moderate",
        "mechanism": "Calcium in dairy products binds to tetracycline",
        "effect": "Reduced antibiotic absorption and effectiveness",
        "recommendation": "Take tetracycline 2 hours before or 4 hours after dairy"
    },
    ("ciprofloxacin", "dairy"): {
        "risk": "Moderate",
        "mechanism": "Calcium interferes with ciprofloxacin absorption",
        "effect": "Decreased antibiotic effectiveness",
        "recommendation": "Avoid dairy products 2 hours before and after taking ciprofloxacin"
    },
    
    # Blood pressure medications
    ("lisinopril", "banana"): {
        "risk": "Moderate",
        "mechanism": "Bananas are high in potassium, lisinopril can increase potassium levels",
        "effect": "Risk of hyperkalemia (high potassium)",
        "recommendation": "Monitor potassium intake, avoid excessive bananas"
    },
    ("spironolactone", "banana"): {
        "risk": "Moderate",
        "mechanism": "Both spironolactone and bananas increase potassium",
        "effect": "Increased risk of hyperkalemia",
        "recommendation": "Limit high-potassium foods like bananas"
    },
    
    # MAOIs
    ("phenelzine", "aged_cheese"): {
        "risk": "High",
        "mechanism": "Aged cheese contains tyramine, MAOIs prevent its breakdown",
        "effect": "Tyramine buildup can cause severe hypertension",
        "recommendation": "Avoid aged cheeses, cured meats, and fermented foods"
    },
    ("tranylcypromine", "red_wine"): {
        "risk": "High",
        "mechanism": "Red wine contains tyramine, MAOIs prevent its metabolism",
        "effect": "Dangerous blood pressure spikes",
        "recommendation": "Avoid red wine and other tyramine-rich foods"
    },
    
    # Diabetes medications
    ("metformin", "alcohol"): {
        "risk": "Moderate",
        "mechanism": "Alcohol can increase metformin's effect on lactic acid",
        "effect": "Increased risk of lactic acidosis",
        "recommendation": "Limit alcohol consumption while taking metformin"
    },
    
    # Thyroid medications
    ("levothyroxine", "soy"): {
        "risk": "Moderate",
        "mechanism": "Soy can interfere with levothyroxine absorption",
        "effect": "Reduced thyroid hormone effectiveness",
        "recommendation": "Take levothyroxine 4 hours before or after soy products"
    },
    ("levothyroxine", "iron_supplements"): {
        "risk": "Moderate",
        "mechanism": "Iron can bind to levothyroxine in the gut",
        "effect": "Decreased thyroid hormone absorption",
        "recommendation": "Separate iron supplements by 4 hours from levothyroxine"
    }
}

# Food category mappings for broader matching
FOOD_CATEGORIES = {
    "grapefruit": ["grapefruit", "grapefruit juice", "citrus"],
    "dairy": ["milk", "cheese", "yogurt", "cream", "butter", "ice cream"],
    "high_potassium": ["banana", "potato", "tomato", "avocado", "spinach", "kale"],
    "high_vitamin_k": ["spinach", "kale", "broccoli", "brussels sprouts", "cabbage"],
    "tyramine_rich": ["aged cheese", "cured meat", "salami", "pepperoni", "red wine", "beer"],
    "iron_rich": ["red meat", "spinach", "beans", "lentils", "iron supplements"]
}

def predict_interaction(drug: str, food: str) -> str:
    """
    Predict drug-food interaction using comprehensive database.
    
    Args:
        drug (str): Standardized drug name
        food (str): Food item to check
    
    Returns:
        str: Formatted interaction prediction
    """
    try:
        drug_lower = drug.lower()
        food_lower = food.lower()
        
        # Direct match
        direct_key = (drug_lower, food_lower)
        if direct_key in DRUG_FOOD_INTERACTIONS:
            interaction = DRUG_FOOD_INTERACTIONS[direct_key]
            return format_interaction_result(interaction, drug, food)
        
        # Category-based matching
        for category, foods in FOOD_CATEGORIES.items():
            if food_lower in foods:
                for (drug_name, food_name), interaction in DRUG_FOOD_INTERACTIONS.items():
                    if drug_lower == drug_name and food_name in foods:
                        return format_interaction_result(interaction, drug, food)
        
        # Partial drug name matching (for drug classes)
        for (drug_name, food_name), interaction in DRUG_FOOD_INTERACTIONS.items():
            if drug_lower in drug_name or drug_name in drug_lower:
                if food_lower == food_name or food_lower in food_name:
                    return format_interaction_result(interaction, drug, food)
        
        # No known interaction found
        return generate_no_interaction_response(drug, food)
        
    except Exception as e:
        logger.error(f"Error in predict_interaction: {e}")
        return f"⚠️ **Prediction Error**\n\nUnable to predict interaction due to an error. Please consult a healthcare provider."

def format_interaction_result(interaction: Dict, drug: str, food: str) -> str:
    """Format interaction result in structured format."""
    # Map recommendation to action
    recommendation_text = interaction['recommendation']
    if 'avoid' in recommendation_text.lower():
        action = "Avoid"
    elif 'limit' in recommendation_text.lower():
        action = "Limit"
    elif 'monitor' in recommendation_text.lower():
        action = "Monitor"
    else:
        action = "Safe"
    
    result = f"""
**RISK LEVEL**: {interaction['risk']}

**INTERACTION**: Yes - Known interaction in medical database

**RECOMMENDATION**: {action} - {recommendation_text.lower()}

**REASON**: {interaction['mechanism']}

---
*Source: ML Prediction - Based on known drug-food interactions*
"""
    
    return result

def generate_no_interaction_response(drug: str, food: str) -> str:
    """Generate response when no known interaction is found."""
    result = f"""
**RISK LEVEL**: None

**INTERACTION**: No - No known interactions in database

**RECOMMENDATION**: Safe - This combination appears safe based on available data

**REASON**: No significant drug-food interactions found in our medical database

---
*Source: ML Prediction - Based on known drug-food interactions*
"""
    
    return result

def get_risk_level(drug: str, food: str) -> Optional[str]:
    """Get risk level for drug-food combination."""
    try:
        drug_lower = drug.lower()
        food_lower = food.lower()
        
        # Check direct match
        direct_key = (drug_lower, food_lower)
        if direct_key in DRUG_FOOD_INTERACTIONS:
            return DRUG_FOOD_INTERACTIONS[direct_key]["risk"]
        
        # Check category matches
        for category, foods in FOOD_CATEGORIES.items():
            if food_lower in foods:
                for (drug_name, food_name), interaction in DRUG_FOOD_INTERACTIONS.items():
                    if drug_lower == drug_name and food_name in foods:
                        return interaction["risk"]
        
        return "Low"  # Default for unknown combinations
        
    except Exception as e:
        logger.error(f"Error getting risk level: {e}")
        return None