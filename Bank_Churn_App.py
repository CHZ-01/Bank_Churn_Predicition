import streamlit as st
import pandas as pd
import numpy as np
import time
import pickle

# Load Pickle
with open("Bank_Churn_Loads.pkl","rb") as f:
    dit = pickle.load(f)

# Header
st.set_page_config(page_title="Churn Prediction",page_icon=r"images\Churn Predict.png",layout="wide")

# CSS
with open(r"css\style.css") as css:
    st.markdown(f"<style>{css.read()}</style>",unsafe_allow_html=True)

st.title("Bank Churn Prediction")

# Page Select Session
if "select" not in st.session_state:
    st.session_state.select = "Home Page"

# Image Slideshow
def image_slideshow():
    image_paths = ["images/image1.jpg","images/image2.jpg","images/image3.jpg","images/image4.jpg","images/image5.jpg"]

    if "index" not in st.session_state:
        st.session_state.index = 0
        st.session_state.update_time = time.time()

    if time.time() - st.session_state.update_time > 2:
        st.session_state.index = (st.session_state.index + 1) % len(image_paths)
        st.session_state.update_time = time.time()
        
    b1,img = st.columns([0.2,2])
    img.image(image_paths[st.session_state.index],use_container_width=True)

# Page Class
class Pages:

    # Home
    def home_page(self):    

        intro.title("Welcome")  
        intro.write("to the Bank Churn Prediction App! Curious if your customers are likely to leave? Our intelligent prediction system analyzes key factors like transaction history, account activity, and customer behavior to assess churn risk instantly!")  
        intro.write("✔ Identify high-risk customers early")  
        intro.write("✔ Take proactive steps to retain them")  
        intro.write("✔ Improve customer satisfaction and loyalty")
        
        b1,btn,b2 = st.columns([1,5,1],vertical_alignment="top")
        # Start Button
        start = btn.button("Get Started",key="start")

        if start:
            st.session_state.select = "First Page"
            st.rerun()

    # First Page
    def first_page(self): 

        st.session_state.Gender = intro.selectbox("Gender:",["Male","Female"],None)

        st.session_state.Age = intro.number_input("Age:",18,80,None)

        st.session_state.Education = intro.selectbox("Education:",["High School","Diploma","Bachelor's","Master's"],None)

        st.session_state.Marriage = intro.selectbox("Marital Status:",["Single","Married","Divorced"],None)

        b1,btn1,btn2,err,b2 = st.columns([1.6,1.5,1.5,3.2,3.4],vertical_alignment="top")
        
        # Back Button
        first_back = btn1.button("Back",key="first_back") 
        # Next Button
        first_next = btn2.button("Next",key="first_next") 

        if first_next:
            if st.session_state.Gender == None or st.session_state.Age == None or st.session_state.Education == None or st.session_state.Marriage == None:
                err.error("Fill All the Fields!")
            else:
                st.session_state.select = "Second Page"
                st.rerun()
        elif first_back:
            st.session_state.select = "Home Page"
            st.rerun()
    
    # Second Page
    def second_page(self): 

        st.session_state.Dependents = intro.number_input("Dependents:",0,5,None)

        st.session_state.Income = intro.number_input("Income:",5000,100000,None)

        st.session_state.Tenure = intro.number_input("Tenure:",1,30,None) 

        st.session_state.Communication = intro.selectbox("Communication Preference:",["Email","Phone"],None)

        b1,btn1,btn2,err,b2 = st.columns([1.6,1.5,1.5,3.2,3.4],vertical_alignment="top")
        
        # Back Button
        second_back = btn1.button("Back",key="second_back") 
        # Next Button
        second_next = btn2.button("Next",key="second_next")

        if second_next:
            if st.session_state.Dependents == None or st.session_state.Income == None or st.session_state.Tenure == None or st.session_state.Communication == None:
                err.error("Fill All the Fields!")
            else:
                st.session_state.select = "Third Page"
                st.rerun()
        elif second_back:
            st.session_state.select = "First Page"
            st.rerun()

    # Third Page
    def third_page(self):

        st.session_state.Credit_Score = intro.number_input("Credit Score:",300,900,None)

        st.session_state.Credit_Length = intro.number_input("Credit History Length:",1,30,None)

        st.session_state.Outstanding_Loans = intro.number_input("Outstanding_Loans:",1000,50000,None)

        st.session_state.Balance = intro.number_input("Balance:",1,250000,None)

        b1,btn1,btn2,err,b2 = st.columns([1.7,1.5,1.7,3.3,3.4],vertical_alignment="top")
        
        # Back Button
        third_back = btn1.button("Back",key="third_back") 
        # Final Submit
        check = btn2.button("Check",key="check")

        if check:
            if st.session_state.Credit_Score == None or st.session_state.Credit_Length == None or st.session_state.Outstanding_Loans == None or st.session_state.Balance == None:
                err.error("Fill All the Fields!")
            else:
                st.session_state.select = "Last Page"
                st.rerun()
        elif third_back:
            st.session_state.select = "Second Page"
            st.rerun()

    # Last Page / Output Page
    def last_page(self):

        intro.title("Churn Status")

        Gender = dit["Gender"].transform([st.session_state.Gender])[0]
        Education = dit["Education"].transform([[st.session_state.Education]])[0,0]
        Marriage = dit["Marriage"].transform([[st.session_state.Marriage]])[0,0]
        Communication = dit["Communicate"].transform([st.session_state.Communication])[0]

        lst = [Gender,st.session_state.Age,Education,Marriage,st.session_state.Dependents,st.session_state.Income,st.session_state.Tenure,Communication,st.session_state.Credit_Score,st.session_state.Credit_Length,st.session_state.Outstanding_Loans,st.session_state.Balance]
            
        arr = np.hstack((lst)).reshape(1,-1)
        
        cols = ['Gender','Age','Education','Marital_Status','Dependents','Income','Tenure','Communication_Preference','Credit_Score','Credit_History_Length','Outstanding_Loans','Balance']

        df = pd.DataFrame(arr,columns=cols)

        scaled = dit["Scaler"].transform(df)

        predict = dit["Model"].predict(scaled)

        if predict == 0:
            intro.subheader("Sorry,")  
            intro.write("This customer is at risk of churning! Based on our analysis, their engagement and transaction patterns indicate a high likelihood of leaving.")  
            intro.write("Take action now to retain them and improve customer satisfaction!")
        else:
            intro.subheader("Great News!")  
            intro.write("This customer is engaged and showing strong retention! Our analysis confirms their continued loyalty and positive interactions.")  
            intro.write("Keep up the great service to maintain their satisfaction and long-term relationship!")

        b1,btn,b2 = st.columns([1,5,1],vertical_alignment="top")
        
        # Return Home Button
        home = btn.button("Home",key="home")

        if home:
            st.session_state.select = "Home Page"
            st.rerun()

# Class Object
page = Pages()

# Main Container
main_container = st.container(height=500,border=True)

with main_container:
    
    # Side Columns
    col1,col2 = st.columns([0.9,1])
    
    # Side Containers
    container1 = col1.container()
    container2 = col2.container()

    # Image Slideshow
    with container1: 
        image_slideshow()

   # Page Load
    with container2:
        b1,intro,b2 = st.columns([1,5,1],vertical_alignment="top")
        if st.session_state.select == "Home Page":
            page.home_page()
        elif st.session_state.select == "First Page":
            page.first_page()
        elif st.session_state.select == "Second Page":
            page.second_page()
        elif st.session_state.select == "Third Page":    
            page.third_page()
        elif st.session_state.select == "Last Page":
            page.last_page()