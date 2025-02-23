import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load Pickle
with open("Bank_Churn_Loads.pkl","rb") as f:
    dit = pickle.load(f)

# Header
# st.set_page_config(page_title="Churn Prediction",page_icon=r"img\Page_Icon.png",layout="wide")

st.title("Bank Churn Prediction")

# def page1():
Gender = st.selectbox("Gender:",["Male","Female"],None)

Age = st.number_input("Age:",18,80,None)

Education = st.selectbox("Education:",["High School","Diploma","Bachelor's","Master's"],None)

Marriage = st.selectbox("Marital Status:",["Single","Married","Divorced"],None)


# def page2():
Dependents = st.number_input("Dependents:",0,5,None)

Income = st.number_input("Income:",5000,100000,None)

Tenure = st.number_input("Tenure:",1,30,None) 

Communication = st.selectbox("Communication Preference:",["Email","Phone"],None)

# def page3():
Credit_Score = st.number_input("Credit Score:",300,900,None)

Credit_Length = st.number_input("Credit History Length:",1,30,None)

Outstanding_Loans = st.number_input("Outstanding_Loans:",1000,50000,None)

Balance = st.number_input("Balance:",1,250000,None)


btn,err,b = st.columns([0.5,0.71,2])


# def page4():
if btn.button("Submit"):    
    try:
        Gender = dit["Gender"].transform([Gender])[0]
        Education = dit["Education"].transform([[Education]])[0,0]
        Marriage = dit["Marriage"].transform([[Marriage]])[0,0]
        Communication = dit["Communicate"].transform([Communication])[0]

        lst = [Gender,Age,Education,Marriage,Dependents,Income,Tenure,Communication,Credit_Score,Credit_Length,Outstanding_Loans,Balance]
            
        arr = np.hstack((lst)).reshape(1,-1)
        
        cols = ['Gender','Age','Education','Marital_Status','Dependents','Income','Tenure','Communication_Preference','Credit_Score','Credit_History_Length','Outstanding_Loans','Balance']

        df = pd.DataFrame(arr,columns=cols)

        scaled = dit["Scaler"].transform(df)

        predict = dit["Model"].predict(scaled)

        if predict == 0:
            val = "Active Customer"
        else:
            val = "Churned Customer"

        st.text_input("Prediction:",value=val,disabled=True)

    except ValueError:
        err.error("Fill All the Fields.")        
