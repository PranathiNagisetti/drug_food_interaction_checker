import requests
from bs4 import BeautifulSoup
import json
import re
import logging
from llm.gemini_fallback import model

logger = logging.getLogger(__name__)

# Load drug lookup data
try:
    with open("data/drug_lookup.json") as f:
        DRUG_LOOKUP = json.load(f)
except FileNotFoundError:
    logger.warning("drug_lookup.json not found, using empty lookup")
    DRUG_LOOKUP = {}

def simplify_with_ai(official_text: str, drug: str, food: str) -> str:
    """
    Use Gemini AI to simplify official medical text into user-friendly explanation.
    
    Args:
        official_text (str): Raw official medical information
        drug (str): Drug name
        food (str): Food name
    
    Returns:
        str: Simplified, user-friendly explanation
    """
    if not model:
        # Fallback: return first 100 characters
        return official_text[:100] + "..." if len(official_text) > 100 else official_text
    
    try:
        prompt = f"""
        Simplify this official medical information about {drug} and {food} interaction into 1-2 clear, simple sentences that a patient can easily understand:

        Official text: {official_text[:500]}...

        Provide only the simplified explanation, no additional formatting or disclaimers.
        Focus on what the patient needs to know in simple terms.
        """
        
        response = model.generate_content(prompt)
        if response and response.text:
            simplified = response.text.strip()
            # Remove any quotes or extra formatting
            simplified = re.sub(r'^["\']|["\']$', '', simplified)
            return simplified
        
        return official_text[:100] + "..." if len(official_text) > 100 else official_text
        
    except Exception as e:
        logger.error(f"Error simplifying with AI: {e}")
        return official_text[:100] + "..." if len(official_text) > 100 else official_text

def extract_generic_name(rxnorm_name):
    """
    Extract generic drug name from RxNorm standardized name.
    
    Args:
        rxnorm_name (str): Full RxNorm name like "atorvastatin 80 MG Oral Tablet [Lipitor]"
    
    Returns:
        str: Generic name like "atorvastatin"
    """
    if not rxnorm_name:
        return rxnorm_name
    
    # Remove dosage, form, and brand name information
    # Pattern: "generic_name dosage form [brand_name]" -> "generic_name"
    name = rxnorm_name.lower()
    
    # Remove dosage information (e.g., "80 MG", "10 MG")
    name = re.sub(r'\d+\s*mg', '', name)
    
    # Remove common dosage forms
    forms = ['oral tablet', 'oral capsule', 'oral solution', 'injection', 'cream', 'gel', 'patch']
    for form in forms:
        name = name.replace(form, '')
    
    # Remove brand names in brackets
    name = re.sub(r'\[.*?\]', '', name)
    
    # Remove common salt forms and extra words
    salts = ['sodium', 'hydrochloride', 'sulfate', 'phosphate', 'acetate', 'citrate', 'tartrate']
    for salt in salts:
        name = name.replace(salt, '')
    
    # Remove extra spaces and clean up
    name = re.sub(r'\s+', ' ', name).strip()
    
    # If the result is empty or too short, try to extract just the first word
    if len(name) < 3:
        # Fallback: take the first word before any space
        first_word = rxnorm_name.split()[0].lower()
        return first_word
    
    return name

def scrape_medlineplus(drug_name, food_item=None):
    """
    Scrape MedlinePlus for drug-food interactions.
    
    Args:
        drug_name (str): Standardized drug name
        food_item (str): Specific food item to search for
    
    Returns:
        str: Formatted interaction information or None if not found
    """
    try:
        # Extract generic name for lookup
        generic_name = extract_generic_name(drug_name)
        logger.info(f"Looking up generic name: {generic_name} from: {drug_name}")
        
        # Get URL from lookup
        url = DRUG_LOOKUP.get(generic_name.lower())
        if not url:
            logger.info(f"No URL found for drug: {drug_name} (generic: {generic_name})")
            return None
        
        logger.info(f"Scraping URL: {url}")
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Look for specific sections that might contain food interaction info
        interaction_sections = []
        
        # Common section headers that might contain food interactions
        food_related_headers = [
            "food", "diet", "grapefruit", "alcohol", "meals", "eating",
            "nutrition", "supplements", "vitamins", "minerals"
        ]
        
        # Find all headings and paragraphs
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'div']):
            text = element.get_text().lower()
            
            # Check if this section is relevant to food interactions
            if any(header in text for header in food_related_headers):
                # Get the full section content
                section_content = extract_section_content(element, soup)
                if section_content:
                    interaction_sections.append(section_content)
        
        # If no specific food sections found, look for general interaction info
        if not interaction_sections:
            general_sections = soup.find_all(['p', 'li'])
            for element in general_sections:
                text = element.get_text().lower()
                # Look for food-related keywords
                food_keywords = [
                    'food', 'grapefruit', 'drink', 'eat', 'meal', 'cheese', 
                    'tyramine', 'alcohol', 'diet', 'nutrition', 'supplement',
                    'vitamin', 'mineral', 'herb', 'spice', 'juice'
                ]
                if any(keyword in text for keyword in food_keywords):
                    interaction_sections.append(element.get_text().strip())
        
        # If specific food item provided, filter for relevant content
        if food_item and interaction_sections:
            food_specific_sections = []
            food_lower = food_item.lower()
            for section in interaction_sections:
                if food_lower in section.lower():
                    food_specific_sections.append(section)
            
            if food_specific_sections:
                interaction_sections = food_specific_sections
        
        # Format the results
        if interaction_sections:
            result = format_interaction_results(interaction_sections, drug_name, food_item)
            logger.info(f"Found {len(interaction_sections)} relevant sections")
            return result
        else:
            logger.info("No food interaction information found")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error scraping MedlinePlus: {e}")
        return None

def extract_section_content(element, soup):
    """Extract content from a section starting with the given element."""
    content = []
    
    # Get the element's text
    if element.get_text().strip():
        content.append(element.get_text().strip())
    
    # Get subsequent siblings until next heading
    current = element.find_next_sibling()
    while current and current.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        if current.name in ['p', 'li', 'div'] and current.get_text().strip():
            content.append(current.get_text().strip())
        current = current.find_next_sibling()
    
    return ' '.join(content) if content else None

def format_interaction_results(sections, drug_name, food_item=None):
    """Format the interaction results in a concise, structured way."""
    if not sections:
        return None
    
    # Analyze the content to determine risk level and recommendation
    content_text = ' '.join(sections).lower()
    
    # Determine risk level based on keywords
    risk_level = "Low"
    recommendation = "Monitor"
    
    if any(word in content_text for word in ['avoid', 'contraindicated', 'dangerous', 'severe', 'serious']):
        risk_level = "High"
        recommendation = "Avoid"
    elif any(word in content_text for word in ['limit', 'reduce', 'moderate', 'caution']):
        risk_level = "Moderate"
        recommendation = "Limit"
    elif any(word in content_text for word in ['safe', 'no interaction', 'no effect']):
        risk_level = "None"
        recommendation = "Safe"
    
    # Determine if there's an interaction
    has_interaction = "Yes" if risk_level != "None" else "No"
    
    # Use AI to simplify the official information
    full_text = ' '.join(sections)
    food_name = food_item if food_item else "this food"
    simplified_reason = simplify_with_ai(full_text, drug_name, food_name)
    
    formatted_result = f"""
**RISK LEVEL**: {risk_level}

**INTERACTION**: {has_interaction} - Found in official medical database

**RECOMMENDATION**: {recommendation} - {recommendation.lower()} {food_item.lower() if food_item else 'this food'}

**REASON**: {simplified_reason}

---
*Source: MedlinePlus.gov - Official Medical Database*
"""
    
    return formatted_result