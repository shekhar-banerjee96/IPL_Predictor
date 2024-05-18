import streamlit as st
import pandas as pd
import pickle
import base64

def image_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
image_local('background.jpg') 

# Declaring the teams
teams = ['Royal Challengers Bangalore', 'Mumbai Indians', 'Kings XI Punjab', 'Kolkata Knight Riders',
       'Sunrisers Hyderabad', 'Rajasthan Royals', 'Chennai Super Kings',
       'Delhi Capitals']

# decarling the venues

cities = ['Chandigarh', 'Chennai', 'Bangalore', 'Mumbai', 'Dharamsala',
       'Hyderabad', 'Cuttack', 'Jaipur', 'Raipur', 'Delhi', 'Nagpur',
       'Kolkata', 'Indore', 'Centurion', 'Ahmedabad', 'Abu Dhabi',
       'East London', 'Durban', 'Pune', 'Visakhapatnam', 'Mohali',
       'Johannesburg', 'Cape Town', 'Bengaluru', 'Sharjah',
       'Port Elizabeth', 'Kimberley', 'Ranchi', 'Bloemfontein']

pipe = pickle.load(open('pipe.pkl', 'rb'))

with st.container():

    st.title("IPL Win Predictor")

    col1, col2 = st.columns(2)

    with col1:
        battingteam = st.selectbox('Select the Batting Team', sorted(teams))

    with col2:
        bowlingteam = st.selectbox('Select the Bowling Team', sorted(teams))




    city = st.selectbox('Select the city where the match is being played', sorted(cities))

    target = st.number_input('Target',format='%d',value = 0) 

    col3, col4, col5 = st.columns(3)

    with col3:
        score = st.number_input('Score',format='%d',value = 0)

    with col4:
        overs = st.number_input('Overs Completed',format='%d',value = 0)

    with col5:
        wickets = st.number_input('Wickets Fallen',format='%d',value = 0)

    if st.button("Predict Probability"):
        if battingteam == bowlingteam :
            st.header("Unfortunately , Teams don't play with each other.")
        else :    
            runs_left = target - score
            balls_left = 120 - (overs*6)
            wickets = 10 - wickets
            currentrunrate = score/overs if overs > 0 else 0
            requiredrunrate = (runs_left*6)/balls_left

            input_df = pd.DataFrame({'batting_team':[battingteam], 'bowling_team':[bowlingteam],
                                    'city':[city], 'runs_left':[runs_left],
                                    'balls_left':[balls_left],'wickets':[wickets],
                                    'total_runs_x':[target],'current_run_rate':[currentrunrate],
                                    'req_run_rate':[requiredrunrate]})
            result = pipe.predict_proba(input_df)
            lossprob = result[0][0]
            winprob = result[0][1]

            st.header(battingteam+" - "+str(round(winprob*100))+"%")
            st.header(bowlingteam+" - "+str(round(lossprob*100))+"%")
