# codebasics ML course: codebasics.io, all rights reserverd

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prediction_helper import predict

# Set page configuration
st.set_page_config(
    page_title="Health Insurance Premium Predictor",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .prediction-result {
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo and title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">🏥 Health Insurance Premium Predictor</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;">Estimate your health insurance premium based on personal and health factors</p>', unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2 = st.tabs(["💰 Premium Calculator", "ℹ️ About the Model"])
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Personal Information</h2>', unsafe_allow_html=True)
    
    # Define options with tooltips and descriptions
    categorical_options = {
        'Gender': {
            'options': ['Male', 'Female'],
            'description': 'Your biological gender affects premium calculations based on statistical health risks.'
        },
        'Marital Status': {
            'options': ['Unmarried', 'Married'],
            'description': 'Marital status can influence premium rates due to statistical risk factors.'
        },
        'BMI Category': {
            'options': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
            'description': 'Body Mass Index category is a key health indicator used in premium calculations.'
        },
        'Smoking Status': {
            'options': ['No Smoking', 'Regular', 'Occasional'],
            'description': 'Smoking significantly impacts health risks and insurance premiums.'
        },
        'Employment Status': {
            'options': ['Salaried', 'Self-Employed', 'Freelancer', ''],
            'description': 'Your employment type may affect premium calculations and payment options.'
        },
        'Region': {
            'options': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
            'description': 'Geographic location influences premium rates due to regional healthcare costs.'
        },
        'Medical History': {
            'options': [
                'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
                'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
                'Diabetes & Heart disease'
            ],
            'description': 'Pre-existing conditions are important factors in determining premium rates.'
        },
        'Insurance Plan': {
            'options': ['Bronze', 'Silver', 'Gold'],
            'description': 'Higher tier plans offer better coverage but come with higher premium costs.'
        }
    }
    
    # Personal Information section
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input('Age', min_value=18, step=1, max_value=100, 
                             help='Your current age (between 18-100 years)')        
        gender = st.selectbox('Gender', categorical_options['Gender']['options'],
                             help=categorical_options['Gender']['description'])
        marital_status = st.selectbox('Marital Status', categorical_options['Marital Status']['options'],
                                     help=categorical_options['Marital Status']['description'])
        number_of_dependants = st.number_input('Number of Dependants', min_value=0, step=1, max_value=20,
                                             help='Number of people financially dependent on you')
    
    with col2:
        income_lakhs = st.number_input('Income in Lakhs', step=0.1, min_value=0.0, max_value=200.0, format="%.1f",
                                      help='Your annual income in lakhs (₹100,000s)')
        employment_status = st.selectbox('Employment Status', categorical_options['Employment Status']['options'],
                                        help=categorical_options['Employment Status']['description'])
        region = st.selectbox('Region', categorical_options['Region']['options'],
                            help=categorical_options['Region']['description'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Health Information section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Health Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category']['options'],
                                   help=categorical_options['BMI Category']['description'])
        smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status']['options'],
                                     help=categorical_options['Smoking Status']['description'])
    
    with col2:
        medical_history = st.selectbox('Medical History', categorical_options['Medical History']['options'],
                                      help=categorical_options['Medical History']['description'])
        genetical_risk = st.slider('Genetical Risk', min_value=0, max_value=5, step=1,
                                 help='Genetic risk factor score from 0 (low) to 5 (high)')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Insurance Plan section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Insurance Plan</h2>', unsafe_allow_html=True)
    
    # Display plan options with visual indicators
    plan_col1, plan_col2, plan_col3 = st.columns(3)
    
    selected_plan = None
    
    with plan_col1:
        bronze_selected = st.checkbox('Bronze Plan', help='Basic coverage with lower premiums')
        st.markdown('''
        <div style="padding: 10px; border-radius: 5px; border: 1px solid #CD7F32; text-align: center;">
            <h3 style="color: #CD7F32;">Bronze</h3>
            <p>Basic coverage</p>
            <p>Lower premium</p>
            <p>Higher out-of-pocket costs</p>
        </div>
        ''', unsafe_allow_html=True)
        if bronze_selected:
            selected_plan = 'Bronze'
    
    with plan_col2:
        silver_selected = st.checkbox('Silver Plan', help='Balanced coverage and costs')
        st.markdown('''
        <div style="padding: 10px; border-radius: 5px; border: 1px solid #C0C0C0; text-align: center;">
            <h3 style="color: #808080;">Silver</h3>
            <p>Moderate coverage</p>
            <p>Balanced premium</p>
            <p>Moderate out-of-pocket costs</p>
        </div>
        ''', unsafe_allow_html=True)
        if silver_selected:
            selected_plan = 'Silver'
    
    with plan_col3:
        gold_selected = st.checkbox('Gold Plan', help='Comprehensive coverage with higher premiums')
        st.markdown('''
        <div style="padding: 10px; border-radius: 5px; border: 1px solid #FFD700; text-align: center;">
            <h3 style="color: #DAA520;">Gold</h3>
            <p>Comprehensive coverage</p>
            <p>Higher premium</p>
            <p>Lower out-of-pocket costs</p>
        </div>
        ''', unsafe_allow_html=True)
        if gold_selected:
            selected_plan = 'Gold'
    
    # Default to Bronze if none selected
    if not selected_plan:
        selected_plan = 'Bronze'
        bronze_selected = True
    
    insurance_plan = selected_plan
    st.markdown('</div>', unsafe_allow_html=True)

    # Create a dictionary for input values
    input_dict = {
        'Age': age,
        'Number of Dependants': number_of_dependants,
        'Income in Lakhs': income_lakhs,
        'Genetical Risk': genetical_risk,
        'Insurance Plan': insurance_plan,
        'Employment Status': employment_status,
        'Gender': gender,
        'Marital Status': marital_status,
        'BMI Category': bmi_category,
        'Smoking Status': smoking_status,
        'Region': region,
        'Medical History': medical_history
    }
    
    # Add a calculate button with better styling
    st.markdown('<div style="display: flex; justify-content: center; margin: 20px 0;">', unsafe_allow_html=True)
    calculate_button = st.button('Calculate Premium', use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction section
    if calculate_button:
        with st.spinner('Calculating your premium...'):
            prediction = predict(input_dict)
        
        # Display the prediction with better styling
        st.markdown(f'''
        <div class="prediction-result">
            <p>Your Estimated Annual Premium</p>
            <h2>₹{prediction:,}</h2>
        </div>
        ''', unsafe_allow_html=True)
        
        # Add some context to the prediction
        st.info(f"This estimate is based on the information you provided. Actual premiums may vary based on additional factors and insurance provider policies.")
        
        # Show factors that influenced the premium
        st.markdown('<h3>Key Factors Influencing Your Premium</h3>', unsafe_allow_html=True)
        
        # Create a simple visualization of the factors
        factors = {
            'Age': 'High' if age > 50 else ('Medium' if age > 30 else 'Low'),
            'BMI Category': 'High' if bmi_category in ['Obesity', 'Underweight'] else 'Medium' if bmi_category == 'Overweight' else 'Low',
            'Smoking Status': 'High' if smoking_status == 'Regular' else 'Medium' if smoking_status == 'Occasional' else 'Low',
            'Medical History': 'High' if medical_history != 'No Disease' else 'Low',
            'Insurance Plan': 'High' if insurance_plan == 'Gold' else 'Medium' if insurance_plan == 'Silver' else 'Low'
        }
        
        # Convert to numeric for visualization
        factor_values = {'High': 3, 'Medium': 2, 'Low': 1}
        factor_df = pd.DataFrame({
            'Factor': list(factors.keys()),
            'Impact': [factor_values[v] for v in factors.values()]
        })
        
        # Create a horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 4))
        colors = ['#4CAF50', '#FFC107', '#F44336']
        bars = ax.barh(factor_df['Factor'], factor_df['Impact'], color=[colors[v-1] for v in factor_df['Impact']])
        ax.set_xlim(0, 4)
        ax.set_xticks([1, 2, 3])
        ax.set_xticklabels(['Low', 'Medium', 'High'])
        ax.set_title('Impact of Factors on Your Premium')
        
        # Display the chart
        st.pyplot(fig)

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">About the Premium Prediction Model</h2>', unsafe_allow_html=True)
    st.markdown('''
    This health insurance premium calculator uses machine learning to estimate your annual premium based on various personal and health factors.
    
    ### How It Works
    
    The model analyzes the following key factors to predict your premium:
    
    - **Age**: Older individuals typically have higher premiums due to increased health risks
    - **BMI Category**: Weight relative to height affects health risks and premiums
    - **Smoking Status**: Smokers face significantly higher premiums due to associated health risks
    - **Medical History**: Pre-existing conditions impact premium calculations
    - **Insurance Plan**: Higher tier plans (Gold, Silver) provide better coverage but cost more
    
    ### Data Privacy
    
    All information entered is processed locally and is not stored or shared with third parties.
    
    ### Disclaimer
    
    This calculator provides estimates only. Actual premiums will vary based on insurance provider policies, additional health assessments, and other factors not captured in this model.
    ''')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a sample visualization
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Premium Trends</h2>', unsafe_allow_html=True)
    
    # Create sample data for visualization
    age_range = list(range(20, 71, 10))
    premium_by_age_nonsmoker = [5000, 8000, 12000, 18000, 25000, 35000]
    premium_by_age_smoker = [8000, 13000, 20000, 30000, 42000, 55000]
    
    # Create a line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(age_range, premium_by_age_nonsmoker, marker='o', linewidth=2, label='Non-smoker')
    ax.plot(age_range, premium_by_age_smoker, marker='o', linewidth=2, label='Smoker')
    ax.set_xlabel('Age')
    ax.set_ylabel('Average Annual Premium (₹)')
    ax.set_title('Average Premium by Age and Smoking Status')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    
    # Display the chart
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
# Add a footer
st.markdown('''
<div style="text-align: center; margin-top: 30px; padding: 10px; border-top: 1px solid #e0e0e0;">
    <p>© 2025 Health Insurance Premium Predictor | Developed for codebasics ML course</p>
</div>
''', unsafe_allow_html=True)
