import streamlit as st
import time
from core import check_interaction
from rxnorm import get_generic_name_quick
import logging




# Page configuration
st.set_page_config(
    page_title="💊 Drug - Food Interaction Checker",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# Function to toggle theme
def toggle_theme():
    st.session_state.theme = "Dark" if st.session_state.theme == "Light" else "Light"

# Top bar: Title + theme icon
col_left, col_right = st.columns([9, 1])
with col_left:
    st.markdown(
        '<h1 class="main-header" >💊 Drug–Food Interaction Checker</h1>',
        unsafe_allow_html=True
    )
with col_right:
    # Theme toggle icon button
    st.button(
        "🌙" if st.session_state.theme == "Light" else "☀️",
        on_click=toggle_theme
    )

# Apply CSS based on theme
if st.session_state.theme == "Dark":
    with open("styles/dark.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Fix Streamlit header gap background
    st.markdown("""
        <style>
        header.stAppHeader {
            background: #000000 !important;   /* or match your dark background */
        }
        .st-emotion-cache-1ffuo7c {
            background: #000000 !important;   /* override white background */
        }
        </style>
    """, unsafe_allow_html=True)

else:
    with open("styles/light.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Configure logging
# Apply CSS based on theme
if st.session_state.theme == "Dark":
    with open("styles/dark.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # Make placeholder text white in dark mode
    st.markdown("""
        <style>
        ::placeholder {
            color: #ffffff !important;
            opacity: 1 !important;
        }
        input, textarea {
            color: #ffffff !important;
            background-color: #333333 !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    with open("styles/light.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        ::placeholder {
            color: #666666 !important;
            opacity: 1 !important;
        }
        input, textarea {
            color: #000000 !important;
            background-color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.25rem;
        color: #666;
        text-align: center;
        margin-top: -0.5rem;
        margin-bottom: 0.5rem;}
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    

    /* Optional: Reduce padding between components */
    .element-container {
        margin-top: -0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)


logging.basicConfig(level=logging.INFO)
def main():
    # Header
    #st.markdown('<h1 class="main-header">💊 Drug–Food Interaction Checker</h1>', unsafe_allow_html=True)
    st.markdown(
    '<p class="sub-header" style="text-align: center; width: 100%; margin-top: 0; margin-bottom: 0.5rem;">AI-powered assistant to identify potential interactions between medications and foods</p>',
    unsafe_allow_html=True
)

    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About This Tool")
        st.markdown("""
        This application helps you check for potential interactions between medications and foods using:
        
        🔬 **Official Sources**: MedlinePlus.gov
        🤖 **AI Analysis**: Google Gemini AI
        🧠 **ML Predictions**: Based on known interactions
        
        **⚠️ Important Disclaimer:**
        This tool provides general information only and should not replace professional medical advice. Always consult your healthcare provider or pharmacist.
        """)
        
        st.header("📋 How It Works")
        st.markdown("""
        1. **Enter** your medication name (brand or generic)
        2. **Enter** the food item you're concerned about
        3. **Click** "Check Interaction" to get results
        4. **Review** the analysis and recommendations
        """)
        
        st.header("🔍 Example Searches")
        st.markdown("""
        **Drugs:**
        - Lipitor, Warfarin, Tylenol
        - Atorvastatin, Coumadin, Acetaminophen
        
        **Foods:**
        - Grapefruit, Spinach, Dairy
        - Alcohol, Bananas, Aged Cheese
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💊 Medication")
        drug = st.text_input(
            "Enter medication name",
            placeholder="e.g., Lipitor, Warfarin, Tylenol",
            help="Enter the brand name or generic name of your medication"
        )
        
        if drug:
            # Show standardized name
            generic_name = get_generic_name_quick(drug)
            if generic_name.lower() != drug.lower():
                st.info(f"📝 Standardized to: **{generic_name}**")
    
    with col2:
        st.subheader("🍎 Food Item")
        food = st.text_input(
            "Enter food or beverage",
            placeholder="e.g., grapefruit, spinach, dairy",
            help="Enter the food or beverage you want to check"
        )
    
    # Check button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        check_button = st.button(
            "🔍 Check Interaction",
            type="primary",
            use_container_width=True
        )
    
    # Process the interaction check
    if check_button:
        if drug and food:
            with st.spinner("🔍 Analyzing interaction..."):
                # Add a small delay to show the spinner
                time.sleep(0.5)
                
                try:
                    source, response, generic_drug = check_interaction(drug, food)
                    
                    # Display results based on source
                    if source == "official":
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("✅ **Official Information Found**")
                        st.markdown(response)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    elif source == "ai":
                        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                        st.warning("🤖 **AI-Generated Analysis**")
                        st.markdown(response)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    elif source == "ml":
                        st.markdown('<div class="info-box">', unsafe_allow_html=True)
                        st.info("🧠 **Machine Learning Prediction**")
                        st.markdown(response)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    elif source == "error":
                        st.markdown('<div class="error-box">', unsafe_allow_html=True)
                        st.error("❌ **Error Occurred**")
                        st.markdown(response)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Show additional information
                    if source != "error":
                        st.markdown("---")
                        st.subheader("📊 Analysis Summary")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Drug", generic_drug.title())
                        with col2:
                            st.metric("Food", food.title())
                        with col3:
                            source_icon = {
                                "official": "🔬",
                                "ai": "🤖", 
                                "ml": "🧠"
                            }.get(source, "❓")
                            st.metric("Source", f"{source_icon} {source.title()}")
                        
                        # Additional recommendations
                        st.markdown("---")
                        st.subheader("💡 General Recommendations")
                        st.markdown("""
                        - **Always consult** your healthcare provider or pharmacist
                        - **Read** medication labels and patient information
                        - **Be consistent** with your diet when taking medications
                        - **Monitor** for any unusual symptoms
                        - **Report** any concerns to your doctor immediately
                        """)
                        
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
                    st.info("Please try again or contact support if the problem persists.")
                    
        else:
            st.error("❌ Please enter both medication and food names.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>💊 Drug–Food Interaction Checker | Powered by MedlinePlus, Gemini AI, and ML</p>
        <p>⚠️ This tool is for informational purposes only. Always consult healthcare professionals.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()