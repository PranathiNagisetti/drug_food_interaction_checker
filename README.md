# 💊 Drug–Food Interaction Checker

> An AI-powered web application to identify and explain possible interactions between medications and foods, using trusted medical sources with Gemini AI as a fallback.

## 🌐 Live Demo

**Try the application live:** [https://drugfood-interaction-checker.streamlit.app/](https://drugfood-interaction-checker.streamlit.app/)

---

## 🎯 Overview

This application helps users check for potential drug-food interactions by:

1. **Standardizing drug names** using the RxNorm API  
2. **Checking official sources** (MedlinePlus.gov) for known interactions  
3. **Using AI analysis** (Google Gemini) when no official data exists  
4. **Providing ML predictions** based on known interaction patterns  
5. **Displaying comprehensive results** with safety recommendations

## 🏗️ System Architecture

```plaintext
User Input (Drug + Food)
      ↓
Standardize Drug Name (RxNorm API)
      ↓
Scrape MedlinePlus for interactions
      ↓
✅ If found → Show official result
❌ If not found → Ask Gemini AI for explanation
      ↓
Show interaction + disclaimer (if AI)
```

## 🧱 Tech Stack

| Component         | Technology         |
|-------------------|-------------------|
| **Frontend**      | Streamlit         |
| **Backend**       | Python 3.8+       |
| **Drug Standardization** | RxNorm API  |
| **Official Data** | MedlinePlus Web Scraping |
| **AI Fallback**   | Google Gemini API |
| **Data Storage**  | JSON files        |
| **Web Scraping**  | BeautifulSoup4    |

## 📂 Project Structure

```
drug_food_interaction_checker_final/
├── app.py                  # Streamlit UI
├── core.py                 # Main logic handler
├── rxnorm.py               # Drug name standardizer
├── medline_scraper.py      # MedlinePlus scraper
├── llm/
│   └── gemini_fallback.py  # Gemini AI integration
├── ml_model/
│   └── predict.py          # ML prediction engine
├── data/
│   ├── drug_lookup.json    # Drug URL mappings
│   └── drug_cache.json     # Cached drug names
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (optional, for AI features)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SowmyaKurapati26/drug_food_interaction_checker.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API (optional):**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 🧠 How It Works

- **Drug Name Standardization:** Uses RxNorm API to convert brand names to generic names, caches results, and handles common variations.
- **Official Data Lookup:** Scrapes MedlinePlus.gov for drug information, searches for food interaction sections, and extracts relevant safety info.
- **AI Analysis (Fallback):** Uses Google Gemini AI when no official data exists, providing comprehensive interaction analysis.
- **ML Predictions:** Uses a database of known drug-food interactions for risk assessment and recommendations.

## 📊 Features

- **Multi-source data:** Official (MedlinePlus) + AI (Gemini) + ML predictions
- **Drug standardization:** Handles brand/generic names
- **Comprehensive coverage:** 100+ medications in database
- **Risk assessment:** High/Moderate/Low risk levels
- **Detailed explanations:** Mechanisms and recommendations
- **Modern UI:** Clean, responsive Streamlit interface
- **Clear results:** Color-coded risk levels and sources

## ⚠️ Limitations & Disclaimers

- **Not medical advice:** For informational purposes only
- **Consult professionals:** Always check with healthcare providers
- **Individual variation:** Responses may vary between people
- **No liability:** Use at your own risk

## 🔧 Configuration

### Environment Variables
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Customization
- **Add drugs:** Edit `data/drug_lookup.json`
- **Modify prompts:** Edit `llm/gemini_fallback.py`
- **Update ML data:** Edit `ml_model/predict.py`
- **Change UI:** Modify `app.py`

## 🧪 Testing

- Test with known interactions (Lipitor + grapefruit)
- Test with unknown combinations (Paracetamol + papaya)
- Test error handling (invalid drug names)
- Test UI responsiveness

## 🤝 Contributing

- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Submit a pull request

## 📄 License

This project is for educational and informational purposes only. It is not intended to provide medical advice or replace professional healthcare consultation.

## 🙏 Acknowledgments

- **MedlinePlus**: Official drug information source
- **RxNorm**: Drug name standardization
- **Google Gemini**: AI analysis capabilities
- **Streamlit**: Web application framework
- **BeautifulSoup**: Web scraping library

---

