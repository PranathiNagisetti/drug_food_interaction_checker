import requests
import logging
import time
from typing import Optional, Dict
import json
import os

logger = logging.getLogger(__name__)

# Cache for drug name lookups to reduce API calls
DRUG_CACHE_FILE = "data/drug_cache.json"
DRUG_CACHE = {}

def load_drug_cache():
    """Load drug name cache from file."""
    global DRUG_CACHE
    try:
        if os.path.exists(DRUG_CACHE_FILE):
            with open(DRUG_CACHE_FILE, 'r') as f:
                DRUG_CACHE = json.load(f)
            logger.info(f"Loaded {len(DRUG_CACHE)} cached drug names")
    except Exception as e:
        logger.warning(f"Could not load drug cache: {e}")
        DRUG_CACHE = {}

def save_drug_cache():
    """Save drug name cache to file."""
    try:
        os.makedirs(os.path.dirname(DRUG_CACHE_FILE), exist_ok=True)
        with open(DRUG_CACHE_FILE, 'w') as f:
            json.dump(DRUG_CACHE, f, indent=2)
        logger.info(f"Saved {len(DRUG_CACHE)} drug names to cache")
    except Exception as e:
        logger.warning(f"Could not save drug cache: {e}")

# Load cache on module import
load_drug_cache()

def get_generic_name(drug_name: str) -> str:
    """
    Get standardized generic name for a drug using RxNorm API.
    
    Args:
        drug_name (str): Drug name (brand or generic)
    
    Returns:
        str: Standardized generic name or original name if not found
    """
    if not drug_name or not drug_name.strip():
        return drug_name
    
    drug_name = drug_name.strip()
    
    # Check cache first
    if drug_name.lower() in DRUG_CACHE:
        logger.info(f"Cache hit for: {drug_name}")
        return DRUG_CACHE[drug_name.lower()]
    
    try:
        logger.info(f"Querying RxNorm for: {drug_name}")
        
        # Step 1: Get RxCUI (RxNorm Concept Unique Identifier)
        base_url = "https://rxnav.nlm.nih.gov/REST"
        search_url = f"{base_url}/drugs.json?name={drug_name}"
        
        response = requests.get(search_url, timeout=10, verify=False)
        response.raise_for_status()
        
        data = response.json()
        drug_group = data.get("drugGroup", {})
        concept_group = drug_group.get("conceptGroup", [])
        
        # Find the best match (prefer generic names)
        best_match = None
        for group in concept_group:
            if "conceptProperties" in group:
                concepts = group["conceptProperties"]
                for concept in concepts:
                    # Prefer generic names over brand names
                    if concept.get("synonymType") == "BN" and not best_match:
                        best_match = concept.get("name", drug_name)
                    elif concept.get("synonymType") == "IN" and not best_match:
                        best_match = concept.get("name", drug_name)
                    elif not best_match:
                        best_match = concept.get("name", drug_name)
        
        if best_match and best_match != drug_name:
            # Cache the result
            DRUG_CACHE[drug_name.lower()] = best_match
            save_drug_cache()
            logger.info(f"Standardized {drug_name} -> {best_match}")
            return best_match
        
        # If no match found, try alternative approach
        return get_generic_name_alternative(drug_name)
        
    except requests.RequestException as e:
        logger.error(f"Request error for {drug_name}: {e}")
        return drug_name
    except Exception as e:
        logger.error(f"Error standardizing {drug_name}: {e}")
        return drug_name

def get_generic_name_alternative(drug_name: str) -> str:
    """
    Alternative method to get generic name using RxCUI lookup.
    """
    try:
        base_url = "https://rxnav.nlm.nih.gov/REST"
        
        # Try to get RxCUI directly
        rxcui_url = f"{base_url}/rxcui.json?name={drug_name}"
        response = requests.get(rxcui_url, timeout=10, verify=False)
        response.raise_for_status()
        
        rxcui_data = response.json()
        rxcui = rxcui_data.get("idGroup", {}).get("rxnormId", [None])[0]
        
        if rxcui:
            # Get properties for this RxCUI
            props_url = f"{base_url}/rxcui/{rxcui}/properties.json"
            props_response = requests.get(props_url, timeout=10, verify=False)
            props_response.raise_for_status()
            
            props_data = props_response.json()
            properties = props_data.get("properties", {})
            
            # Look for generic name
            generic_name = properties.get("name", drug_name)
            
            if generic_name != drug_name:
                DRUG_CACHE[drug_name.lower()] = generic_name
                save_drug_cache()
                logger.info(f"Alternative method: {drug_name} -> {generic_name}")
                return generic_name
        
        # If still no match, cache the original name
        DRUG_CACHE[drug_name.lower()] = drug_name
        save_drug_cache()
        return drug_name
        
    except Exception as e:
        logger.error(f"Alternative method failed for {drug_name}: {e}")
        return drug_name

def get_drug_info(drug_name: str) -> Optional[Dict]:
    """
    Get comprehensive drug information from RxNorm.
    
    Args:
        drug_name (str): Drug name to look up
    
    Returns:
        Dict: Drug information or None if not found
    """
    try:
        generic_name = get_generic_name(drug_name)
        
        base_url = "https://rxnav.nlm.nih.gov/REST"
        search_url = f"{base_url}/drugs.json?name={generic_name}"
        
        response = requests.get(search_url, timeout=10, verify=False)
        response.raise_for_status()
        
        data = response.json()
        drug_group = data.get("drugGroup", {})
        
        return {
            "original_name": drug_name,
            "generic_name": generic_name,
            "drug_group": drug_group
        }
        
    except Exception as e:
        logger.error(f"Error getting drug info for {drug_name}: {e}")
        return None

# Common drug name mappings for quick lookup
COMMON_DRUG_MAPPINGS = {
    "lipitor": "atorvastatin",
    "zocor": "simvastatin",
    "coumadin": "warfarin",
    "tylenol": "acetaminophen",
    "advil": "ibuprofen",
    "aspirin": "acetylsalicylic acid",
    "prozac": "fluoxetine",
    "zoloft": "sertraline",
    "paxil": "paroxetine",
    "lexapro": "escitalopram",
    "celexa": "citalopram",
    "wellbutrin": "bupropion",
    "effexor": "venlafaxine",
    "cymbalta": "duloxetine",
    "abilify": "aripiprazole",
    "zyprexa": "olanzapine",
    "risperdal": "risperidone",
    "seroquel": "quetiapine",
    "geodon": "ziprasidone",
    "clozaril": "clozapine"
}

def get_generic_name_quick(drug_name: str) -> str:
    """
    Quick lookup for common drug names without API calls.
    
    Args:
        drug_name (str): Drug name to look up
    
    Returns:
        str: Generic name or original name
    """
    drug_lower = drug_name.lower()
    
    # Check common mappings first
    if drug_lower in COMMON_DRUG_MAPPINGS:
        return COMMON_DRUG_MAPPINGS[drug_lower]
    
    # Check cache
    if drug_lower in DRUG_CACHE:
        return DRUG_CACHE[drug_lower]
    
    # Fall back to API call
    return get_generic_name(drug_name)