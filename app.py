# Importing the Necessary Libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pickle


# reading the cleaned data
df = pd.read_csv("cleaned_Loan_application_data.csv")


# function to predict whether a client is likely to default on their loan payments
def predict(CNT_FAM_MEMBERS, YEARS_EMPLOYED, ORGANIZATION_TYPE, AMT_ANNUITY, AMT_CREDIT, 
            NAME_INCOME_TYPE, AGE, FLAG_OWN_CAR, AMT_INCOME_TOTAL):

    ORGANIZATION_TYPE = df["ORGANIZATION_TYPEencode"][df["ORGANIZATION_TYPE"] == f"{ORGANIZATION_TYPE}"].unique()[0]
    NAME_INCOME_TYPE = df["NAME_INCOME_TYPEencode"][df["NAME_INCOME_TYPE"] == f"{NAME_INCOME_TYPE}"].unique()[0]
    FLAG_OWN_CAR_encode = {"Yes": 1, "No": 0}
    FLAG_OWN_CAR = FLAG_OWN_CAR_encode[FLAG_OWN_CAR]

    with open("random_forest_model.pkl", "rb") as file:
        model = pickle.load(file)

    prediction = model.predict([[CNT_FAM_MEMBERS, YEARS_EMPLOYED, ORGANIZATION_TYPE, AMT_ANNUITY, AMT_CREDIT, 
                                 NAME_INCOME_TYPE, AGE, FLAG_OWN_CAR, AMT_INCOME_TOTAL]])

    if prediction == 1:
        return 'Default'
    if prediction == 0:
        return 'Not-Default'



# Streamlit Setup
st.set_page_config("Loan Default", layout = "wide")


selected = option_menu(None,
                       options = ["Menu", "Prediction"],
                       icons = ["house"],
                       orientation = "horizontal",
                       styles = {"nav-link": {"font-size": "18px", "text-align": "center", "margin": "1px"},
                                 "icon": {"color": "yellow", "font-size": "20px"},
                                 "nav-link-selected": {"background-color": "#9457eb"}} )


if selected == "Menu":
    
    st.title(''':red[**Financial Risk Detection**]''')

    st.markdown("")

    st.markdown('''* The lending industry faces significant challenges in assessing creditworthiness, particularly for applicants with limited or no credit history. 
                     Loan defaults pose financial risks to lending institutions, making accurate risk assessment crucial.''')
    
    st.markdown('''* This project aims to leverage Exploratory Data Analysis (EDA) and machine learning to conduct risk analysis for loan default prediction 
                     in the context of a consumer finance company. By analyzing historical loan application data, we will identify patterns and factors that 
                     indicate whether a client is likely to default on their loan payments. This analysis will assist the company in minimizing financial losses 
                     while ensuring that creditworthy applicants are not unfairly rejected.''')


if selected == "Prediction":

    with st.form("classification"):

        col1, col2 = st.columns(2)

        with col1:
            st.number_input(":blue[**Age**]", min_value = 0, key = "age")

            st.number_input(":blue[**Client Family Members**]", min_value = 0, key = "cfm")

            st.number_input(":blue[**No of Years Employed**]", min_value = 0, key = "ye")

            st.selectbox(":blue[**Organization Type**]", 
                        options = df["ORGANIZATION_TYPE"].unique(),
                        key = "ot")
            
            st.selectbox(":blue[**Income Type**]", 
                        options = df["NAME_INCOME_TYPE"].unique(),
                        key = "nit")
        

        with col2:

            st.number_input(":blue[**Amt_Annuity**]", min_value = 0.0, key = "aa")

            st.number_input(":blue[**Amt_Credit**]", min_value = 0.0, key = "ac")

            st.number_input(":blue[**Amt_Income_Total**]", min_value = 0.0, key = "ait")

            st.radio(":blue[Flag_Own_Car]", options = ["Yes", "No"], key = "foc")
            

        if st.form_submit_button("**Predict**"):

            pred = predict(st.session_state["cfm"], st.session_state["ye"], st.session_state["ot"], 
                           st.session_state["aa"], st.session_state["ac"], st.session_state["nit"], 
                           st.session_state["age"], st.session_state["foc"], st.session_state["ait"])
            
            st.success(f"**The Client is likely to :green[{pred}] on their Loan Payments.**")

    
# ------------------------------x--------------------------x----------------------------x--------------------------x------------------------------x--------------------------------------------------