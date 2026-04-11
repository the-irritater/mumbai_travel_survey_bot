import streamlit as st
import pandas as pd
import os
import datetime
import random
import glob

st.set_page_config(
    page_title="Mumbaikars Travel Survey Chatbot",
    page_icon="🌍",
    layout="centered"
)

def apply_custom_css():
    st.markdown("""
        <style>
            .stApp {
                background-color: #0e1117;
            }
            .chat-user {
                background-color: #1e2130;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 10px;
            }
            .chat-bot {
                background-color: #262730;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 10px;
            }
            [data-testid="stRadio"] > div {
                gap: 0.5rem;
            }
        </style>
    """, unsafe_allow_html=True)

# Ensure the CSV is saved in the same directory as the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "survey_responses.csv")

QUESTIONS = [
    {"id": "q1", "text": "Are you a legal resident of Mumbai City?", "type": "radio", "options": ["Yes", "No"], "screener": True},
    {"id": "q2", "text": "Have you travelled outside Mumbai and stayed at a destination for at least 24 consecutive hours in the last 12 months?", "type": "radio", "options": ["Yes", "No"], "screener": True},

    {"id": "q3", "text": "What is your age group?", "type": "radio", "options": ["18-24 years", "25-34 years", "35-44 years", "45-54 years", "55-64 years", "65 years and above"]},
    {"id": "q4", "text": "What is your gender?", "type": "radio", "options": ["Male", "Female", "Prefer not to say"]},
    {"id": "q5", "text": "What is your highest level of education completed?", "type": "radio", "options": ["Below SSC (10th)", "SSC / HSC (10th-12th)", "Undergraduate (Bachelor's Degree)", "Postgraduate (Master's Degree)", "Doctoral / Professional Degree (PhD, MBA, CA, etc.)"]},
    {"id": "q6", "text": "What is your current occupation?", "type": "radio", "options": ["Student", "Private Employee", "Government Employee", "Self-employed / Business Owner", "Homemaker", "Retired", "Unemployed / Between Jobs"]},
    {"id": "q7", "text": "What is your approximate total monthly household income?", "type": "radio", "options": ["Below ₹ 25,000", "₹ 25,001 - ₹ 50,000", "₹ 50,001 - ₹ 1,00,000", "₹ 1,00,001 - ₹ 2,00,000", "Above ₹ 2,00,000", "Prefer not to disclose"]},
    {"id": "q8", "text": "What is your current marital / household status?", "type": "radio", "options": ["Single", "Married without children", "Married with children", "In a relationship (not married)", "Divorced"]},
    {"id": "q9", "text": "Which type of destination did you visit on your most recent trip?", "type": "radio", "options": ["Hill Station / Mountain", "Coastal / Beach", "Cultural / Heritage", "Religious / Pilgrimage", "Nature / Wildlife / Eco-tourism", "International", "Other"]},
    {"id": "q10", "text": "Who did you travel with on this trip?", "type": "radio", "options": ["Alone (Solo travel)", "With spouse", "With family", "With friends", "With colleagues / office group", "Organised tour group"]},
    {"id": "q11", "text": "What was your approximate total budget for that trip (per person, all expenses)?", "type": "radio", "options": ["Below ₹ 5,000", "₹ 5,001 - ₹ 15,000", "₹ 15,001 - ₹ 30,000", "₹ 30,001 - ₹ 50,000", "Above ₹ 50,000"]},
    {"id": "q12", "text": "How many leisure trips (24+ hours away) have you taken in the past 12 months?", "type": "radio", "options": ["1", "2-3", "4-5", "More than 5"]},
    {"id": "q13", "text": "What was your PRIMARY source of information when choosing this destination?", "type": "radio", "options": ["Word of mouth (family / friends)", "Social media (Instagram, YouTube, Reels, etc.)", "Travel websites / blogs / OTAs (MakeMyTrip, TripAdvisor, etc.)", "Personal prior experience", "Travel agent / tour operator", "TV or print media", "Online search engine (Google)"]},

    {"id": "q14_1", "text": "**Push Motivation**: Please rate - *Travelling helps me escape from the stress and pressure of daily work and city life.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q14_2", "text": "**Push Motivation**: Please rate - *I travel to rest, relax, and recharge my mind and body.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q14_3", "text": "**Push Motivation**: Please rate - *Getting away from Mumbai's crowds and noise is an important reason I travel.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q14_4", "text": "**Push Motivation**: Please rate - *Travel allows me to temporarily forget my responsibilities and worries.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    {"id": "q15_1", "text": "**Push Motivation**: Please rate - *I am motivated to travel because I enjoy exciting and thrilling experiences.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q15_2", "text": "**Push Motivation**: Please rate - *I seek destinations that offer adventure activities (trekking, water sports, etc.).*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q15_3", "text": "**Push Motivation**: Please rate - *The possibility of experiencing something new and risky excites me about travel.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q15_4", "text": "**Push Motivation**: Please rate - *Trying new and adrenaline-filled activities is an important part of my travel.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    {"id": "q16_1", "text": "**Push Motivation**: Please rate - *Spending quality time with my family is a primary reason I travel.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q16_2", "text": "**Push Motivation**: Please rate - *I travel to strengthen relationships with my family members / loved ones.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q16_3", "text": "**Push Motivation**: Please rate - *Travelling as a family / with close ones makes the experience more meaningful.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q16_4", "text": "**Push Motivation**: Please rate - *Traveling allows me to create lasting memories with my family.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},

    {"id": "q17_1", "text": "**Push Motivation**: Please rate - *I travel to learn about and experience new cultures, traditions, and ways of life.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q17_2", "text": "**Push Motivation**: Please rate - *Meeting and interacting with people from different backgrounds motivates me to travel.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q17_3", "text": "**Push Motivation**: Please rate - *Travel broadens my perspective on the world and different societies.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q17_4", "text": "**Push Motivation**: Please rate - *I am interested in visiting places that offer historical, cultural, or educational experiences.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},

    {"id": "q18_1", "text": "**Push Motivation**: Please rate - *Travelling to popular or exotic destinations improves my status among peers.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q18_2", "text": "**Push Motivation**: Please rate - *I enjoy sharing my travel experiences on social media to inspire others.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q18_3", "text": "**Push Motivation**: Please rate - *Visiting well-known destinations makes me feel accomplished and distinguished.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q18_4", "text": "**Push Motivation**: Please rate - *Travelling to unique or exclusive destinations enhances my personal image.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},

    {"id": "q19_1", "text": "**Pull Motivation**: Please rate - *I prefer travelling to destinations where I feel personally safe and secure.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q19_2", "text": "**Pull Motivation**: Please rate - *The enjoyment and fun aspect of a trip is a major driver of my travel decision.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q19_3", "text": "**Pull Motivation**: Please rate - *I am more likely to travel if I know the destination is safe for travellers like me.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q19_4", "text": "**Pull Motivation**: Please rate - *I prefer destinations that offer both safety and enjoyable recreational activities.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},

    {"id": "q20_1", "text": "**Pull Motivation**: Rate importance - *Beautiful natural landscapes attract me to a destination.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q20_2", "text": "**Pull Motivation**: Rate importance - *Pleasant climate and weather conditions at the destination are important to me.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q20_3", "text": "**Pull Motivation**: Rate importance - *Clean, unpolluted environments significantly influence my destination choice.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q20_4", "text": "**Pull Motivation**: Rate importance - *A clean, well-maintained destination environment is important in my travel choice.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},

    {"id": "q21_1", "text": "**Pull Motivation**: Rate importance - *Affordable accommodation and food options are a major factor in choosing a destination.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q21_2", "text": "**Pull Motivation**: Rate importance - *Overall value for money is a critical consideration in my destination decision.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q21_3", "text": "**Pull Motivation**: Rate importance - *I compare the cost of travel to different destinations before making a final choice.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q21_4", "text": "**Pull Motivation**: Rate importance - *Availability of budget-friendly transport to the destination influences my choice.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},

    {"id": "q22_1", "text": "**Pull Motivation**: Rate importance - *Local festivals, fairs, and cultural events attract me to a destination.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q22_2", "text": "**Pull Motivation**: Rate importance - *The availability of cultural and arts experiences (museums, folk performances, etc.) is important.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q22_3", "text": "**Pull Motivation**: Rate importance - *I prefer destinations that offer authentic local experiences and traditions.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},

    {"id": "q23_1", "text": "**Pull Motivation**: Rate importance - *A vibrant nightlife, entertainment options, and social scene attract me to a destination.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q23_2", "text": "**Pull Motivation**: Rate importance - *Local food, street food, and regional cuisine are an important part of my travel motivation.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q23_3", "text": "**Pull Motivation**: Rate importance - *The variety of restaurants, cafes, and dining experiences at a destination matters to me.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q23_4", "text": "**Pull Motivation**: Rate importance - *Availability of good shopping facilities (local markets, malls, souvenirs) attracts me.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q23_5", "text": "**Pull Motivation**: Rate importance - *Hygienic conditions (food, water, sanitation) at a destination influence my choice.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},

    {"id": "q24_1", "text": "**Pull Motivation**: Rate importance - *Low crime rates and perceived personal safety strongly influence my destination choice.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q24_2", "text": "**Pull Motivation**: Rate importance - *Political stability and absence of civil unrest at a destination affects my travel decision.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q24_3", "text": "**Pull Motivation**: Rate importance - *Availability of medical facilities and emergency services at a destination is important.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},

    {"id": "q25_1", "text": "**Pull Motivation**: Rate importance - *The presence of well-known historical monuments and heritage sites attracts me to a destination.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q25_2", "text": "**Pull Motivation**: Rate importance - *UNESCO World Heritage Sites or protected monuments are significant draws for me.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q25_3", "text": "**Pull Motivation**: Rate importance - *I prefer destinations with a rich, documented cultural and historical legacy.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},

    {"id": "q26_1", "text": "**Destination Image**: Rate importance - *Good quality and reliable accommodation (hotels, homestays, resorts) is important to my choice.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q26_2", "text": "**Destination Image**: Rate importance - *Efficient and comfortable transport options (flights, trains, roads) within the destination matter.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q26_3", "text": "**Destination Image**: Rate importance - *Friendly and helpful local people and tourism staff positively influence my destination choice.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
    {"id": "q26_4", "text": "**Destination Image**: Rate importance - *Availability of tourist facilities (guided tours, information centres, maps) is important.*", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},

    {"id": "q27_1", "text": "**Destination Image**: Rate quality - *Quality and variety of accommodation options available at this type of destination.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_2", "text": "**Destination Image**: Rate quality - *Quality of local food, restaurants, and dining options.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_3", "text": "**Destination Image**: Rate quality - *Ease and comfort of transport to and within this type of destination.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_4", "text": "**Destination Image**: Rate quality - *Quality of tourism infrastructure (signage, visitor centres, guides, facilities).*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_5", "text": "**Destination Image**: Rate quality - *Natural beauty, scenery, and outdoor appeal of this destination type.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_6", "text": "**Destination Image**: Rate quality - *Cleanliness and environmental quality at this destination type.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_7", "text": "**Destination Image**: Rate quality - *Climate and weather suitability for travel.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_8", "text": "**Destination Image**: Rate quality - *Richness of cultural attractions, monuments, and heritage.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_9", "text": "**Destination Image**: Rate quality - *Local festivals, fairs, and cultural events.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_10", "text": "**Destination Image**: Rate quality - *Friendliness and hospitality of local residents.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_11", "text": "**Destination Image**: Rate quality - *Perceived personal safety and security for travellers.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_12", "text": "**Destination Image**: Rate quality - *Uniqueness and novelty of experiences available.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
    {"id": "q27_13", "text": "**Destination Image**: Rate quality - *Value for money compared to other destination types.*", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},

    {"id": "q28_1", "text": "**Social Media**: Please rate - *Social media content (Instagram, YouTube, Reels, travel influencers) influences my destination choice.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q28_2", "text": "**Social Media**: Please rate - *I often discover new travel destinations through social media posts and travel vlogs.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q28_3", "text": "**Social Media**: Please rate - *I regularly check photos, reviews, and ratings on social media before choosing a destination.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q28_4", "text": "**Social Media**: Please rate - *Positive social media coverage of a destination makes me significantly more likely to visit it.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},

    {"id": "q29_1", "text": "**Social Media**: Please rate - *Recommendations from family and close friends strongly influence my destination choice.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": "q29_2", "text": "**Social Media**: Please rate - *If my social circle visits and recommends a destination, I am more likely to visit it.*", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]}
]

def save_response():
    data = st.session_state.responses
    
    # Check screenout condition
    if data.get("q1") == "No" or data.get("q2") == "No":
        data["Completed"] = False
        data["Screened_Out"] = True
    else:
        data["Completed"] = True
        data["Screened_Out"] = False
        
    data["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    all_columns = [q["id"] for q in QUESTIONS] + ["Completed", "Screened_Out", "Timestamp"]
    row = {col: data.get(col, "") for col in all_columns}
    
    df = pd.DataFrame([row], columns=all_columns)
    
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)
    print(f"DEBUG: Saved response to {CSV_FILE}")

def main():
    apply_custom_css()
    
    st.title("Mumbaikars Travel Survey ✈️")
    st.markdown("Thank you for participating! Please answer the questions below.")
    
    # Initialize session state
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
        st.session_state.responses = {}
        st.session_state.chat_history = []
        st.session_state.completed = False
        st.session_state.screened_out = False

    # Display Chat History
    for msg in st.session_state.chat_history:
        if msg["role"] == "bot":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])

    # If survey is ended (completed or screened out)
    if st.session_state.completed:
        st.success("You have successfully completed the survey. Your responses have been recorded.")
        
        # Show a preview of the saved data to the user
        if os.path.exists(CSV_FILE):
            st.markdown("### Your Recorded Response:")
            df_full = pd.read_csv(CSV_FILE)
            st.dataframe(df_full.tail(1)) # Show the last row added
            
        if st.button("Start Over"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return
        
    if st.session_state.screened_out:
        st.info("Thank you for your time, but you do not meet the criteria for this survey. You have completed your task.")
        if st.button("Start Over"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return

    # Check if we reached the end
    if st.session_state.current_index >= len(QUESTIONS):
        print(f"DEBUG: Reached end of questions. Index: {st.session_state.current_index}")
        save_response()
        st.session_state.completed = True
        st.rerun()
        return

    # Display Current Question
    current_q = QUESTIONS[st.session_state.current_index]
    
    # Randomly pick an image from assets
    assets = glob.glob(os.path.join("assets", "*.png"))
    current_image = random.choice(assets) if assets else None
    
    with st.chat_message("assistant", avatar="🤖"):
        if current_image:
            st.image(current_image, use_container_width=True)
            
        st.markdown(f"**Question {st.session_state.current_index + 1} of {len(QUESTIONS)}**")
        st.markdown(current_q["text"])
        
        user_choice = st.radio(
            "Select an option:", 
            options=current_q["options"], 
            key=current_q["id"],
            index=None
        )
        
        if user_choice is not None:
            # Save answer
            st.session_state.responses[current_q["id"]] = user_choice
            
            # Append to history
            st.session_state.chat_history.append({"role": "bot", "content": current_q["text"]})
            st.session_state.chat_history.append({"role": "user", "content": user_choice})
            
            # Check Screening constraints
            if current_q.get("screener") and user_choice == "No":
                save_response()
                st.session_state.screened_out = True
                st.rerun()
            else:
                st.session_state.current_index += 1
                st.rerun()


if __name__ == "__main__":
    main()
