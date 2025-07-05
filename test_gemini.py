#!/usr/bin/env python3
"""
Test script to verify Gemini API key configuration
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_config():
    """Test if Gemini API is properly configured."""
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key exists
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("\nTo fix this:")
        print("1. Create a .env file in your project root")
        print("2. Add: GEMINI_API_KEY=your_actual_api_key_here")
        print("3. Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    if api_key == "your_gemini_api_key_here":
        print("❌ Please replace the placeholder with your actual API key")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Try different model names
        model_names = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        
        for model_name in model_names:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'Hello, Gemini is working!'")
                
                if response and response.text:
                    print(f"✅ Gemini API is working correctly with model: {model_name}")
                    print(f"Response: {response.text}")
                    return True
                    
            except Exception as model_error:
                print(f"❌ Model {model_name} failed: {model_error}")
                continue
        
        print("❌ All model attempts failed")
        return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini API: {e}")
        return False

if __name__ == "__main__":
    print("Testing Gemini API configuration...")
    test_gemini_config() 