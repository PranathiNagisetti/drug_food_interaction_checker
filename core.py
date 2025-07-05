from rxnorm import get_generic_name
from medline_scraper import scrape_medlineplus
from llm.gemini_fallback import query_interaction_gemini
from ml_model.predict import predict_interaction
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_interaction(drug, food):
    """
    Main function to check drug-food interactions.
    Returns tuple: (source, response, generic_drug_name)
    source can be: "official", "ai", "ml", "error"
    """
    try:
        # Step 1: Standardize drug name using RxNorm API
        logger.info(f"Standardizing drug name: {drug}")
        generic_drug = get_generic_name(drug)
        logger.info(f"Standardized to: {generic_drug}")
        
        # Step 2: Check MedlinePlus for official interactions
        logger.info(f"Checking MedlinePlus for {generic_drug}")
        official_result = scrape_medlineplus(generic_drug,food)
        
        if official_result and official_result.strip():
            logger.info("Found official interaction data")
            return ("official", official_result, generic_drug)
        
        # Step 3: If no official data, use Gemini AI
        logger.info("No official data found, querying Gemini AI")
        ai_response = query_interaction_gemini(generic_drug, food)
        
        # Step 4: If AI says no interaction, use ML model as backup
        if ai_response and "no known interaction" in ai_response.lower():
            logger.info("AI indicates no interaction, using ML model")
            ml_prediction = predict_interaction(generic_drug, food)
            return ("ml", ml_prediction, generic_drug)
        
        # Step 5: Return AI response with disclaimer
        logger.info("Returning AI-generated response")
        return ("ai", ai_response, generic_drug)
        
    except Exception as e:
        logger.error(f"Error in check_interaction: {str(e)}")
        return ("error", f"An error occurred while checking interactions: {str(e)}", drug)