import streamlit as st
import pandas as pd
import os
import datetime
import random
import glob
import uuid
import base64
import gspread

st.set_page_config(
    page_title="Mumbaikars Travel Survey",
    page_icon="✈️",
    layout="centered"
)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "survey_responses.csv")

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def get_gspread_client():
    try:
        credentials = dict(st.secrets["gcp_service_account"])
        client = gspread.service_account_from_dict(credentials)
        return client
    except Exception as e:
        return None

# ── CSS ────────────────────────────────────────────────────────────────────────
def apply_custom_css():
    bg_path = os.path.join(BASE_DIR, "assets", "ai_bg.png")
    bg_b64 = get_base64_image(bg_path)

    if bg_b64:
        st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                background-image: linear-gradient(rgba(5,11,20,0.82), rgba(5,11,20,0.92)),
                                  url("data:image/png;base64,{bg_b64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            [data-testid="stHeader"] {{
                background: transparent;
            }}
            .stApp {{
                background-color: transparent !important;
            }}
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        [data-testid="stAppViewContainer"] {
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
        }

        /* ── Cards ─────────────────────────── */
        .main-card {
            background: rgba(11, 22, 44, 0.88);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 2.5rem;
            border-radius: 18px;
            box-shadow: 0 0 35px rgba(59,130,246,0.12), 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(96,165,250,0.12);
            margin-top: 1rem;
            margin-bottom: 2rem;
        }

        /* ── Welcome badge ─────────────────── */
        .welcome-badge {
            display: inline-block;
            background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(234,179,8,0.15));
            border: 1px solid rgba(96,165,250,0.3);
            border-radius: 50px;
            padding: 6px 18px;
            font-size: 0.82rem;
            font-weight: 600;
            color: #93c5fd !important;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        /* ── Trust signal ──────────────────── */
        .trust-signal {
            font-size: 0.95rem;
            color: #cbd5e1 !important;
            border-left: 3px solid #3b82f6;
            margin: 20px 0 30px 0;
            background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(234,179,8,0.04));
            padding: 16px 20px;
            border-radius: 0 12px 12px 0;
        }
        .trust-signal strong { color: #e2e8f0 !important; }

        /* ── Stat row ──────────────────────── */
        .stat-row {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 1.5rem 0;
            flex-wrap: wrap;
        }
        .stat-item {
            text-align: center;
            padding: 12px 18px;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.06);
            min-width: 100px;
        }
        .stat-item .stat-icon { font-size: 1.4rem; display: block; margin-bottom: 4px; }
        .stat-item .stat-label { font-size: 0.78rem; color: #94a3b8 !important; font-weight: 500; }

        /* ── Progress ──────────────────────── */
        .progress-text {
            font-size: 0.9rem;
            color: #60a5fa !important;
            font-weight: 600;
            margin-bottom: 8px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        /* ── Section header ────────────────── */
        .section-label {
            display: inline-block;
            background: rgba(59,130,246,0.15);
            border: 1px solid rgba(59,130,246,0.25);
            border-radius: 8px;
            padding: 4px 14px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #93c5fd !important;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        /* ── Typography ────────────────────── */
        h1 {
            font-weight: 800;
            font-size: 2.4rem;
            background: linear-gradient(135deg, #60a5fa, #fbbf24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
            line-height: 1.2;
        }
        h2 { color: #e2e8f0 !important; font-weight: 700; }
        h3 { color: #e2e8f0 !important; font-weight: 600; margin-top: 1.2rem; margin-bottom: 0.6rem; }
        .secondary-text { color: #94a3b8 !important; font-size: 1.02rem; line-height: 1.7; }
        p, span, div.stMarkdown { color: #cbd5e1 !important; }

        /* ── Hero image ────────────────────── */
        .hero-img-container img {
            border-radius: 14px;
            box-shadow: 0 6px 25px rgba(0,0,0,0.5);
            margin-bottom: 10px;
        }

        /* ── Radio buttons ─────────────────── */
        div[role="radiogroup"] > label {
            background: rgba(18,33,59,0.9);
            padding: 13px 18px;
            border-radius: 10px;
            margin-bottom: 6px;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
            font-size: 0.93rem;
        }
        div[role="radiogroup"] > label:hover {
            background: rgba(26,47,82,0.95);
            border-color: rgba(96,165,250,0.5);
            transform: translateX(4px);
            box-shadow: 0 0 12px rgba(59,130,246,0.08);
        }
        [data-testid="stRadio"] > div { gap: 0.35rem; }

        /* ── Buttons ───────────────────────── */
        .stButton > button, .stFormSubmitButton > button {
            font-weight: 600;
            letter-spacing: 0.5px;
            padding: 0.6rem 1.5rem;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        /* ── Progress bar ──────────────────── */
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #3b82f6, #fbbf24);
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)


# ── Section definitions (grouping the original questions) ──────────────────────
SECTIONS = [
    {
        "title": "Screening",
        "icon": "🔍",
        "description": "First, let's check if you're eligible for this survey.",
        "questions": [
            {"id": "q1", "text": "Are you a legal resident of Mumbai City?", "type": "radio", "options": ["Yes", "No"], "screener": True},
            {"id": "q2", "text": "Have you travelled outside Mumbai and stayed at a destination for at least 24 consecutive hours in the last 12 months?", "type": "radio", "options": ["Yes", "No"], "screener": True},
        ]
    },
    {
        "title": "Demographics",
        "icon": "👤",
        "description": "Tell us a bit about yourself.",
        "questions": [
            {"id": "q3", "text": "What is your age group?", "type": "radio", "options": ["18-24 years", "25-34 years", "35-44 years", "45-54 years", "55-64 years", "65 years and above"]},
            {"id": "q4", "text": "What is your gender?", "type": "radio", "options": ["Male", "Female", "Prefer not to say"]},
            {"id": "q5", "text": "What is your highest level of education completed?", "type": "radio", "options": ["Below SSC (10th)", "SSC / HSC (10th-12th)", "Undergraduate (Bachelor's Degree)", "Postgraduate (Master's Degree)", "Doctoral / Professional Degree (PhD, MBA, CA, etc.)"]},
            {"id": "q6", "text": "What is your current occupation?", "type": "radio", "options": ["Student", "Private Employee", "Government Employee", "Self-employed / Business Owner", "Homemaker", "Retired", "Unemployed / Between Jobs"]},
            {"id": "q7", "text": "What is your approximate total monthly household income?", "type": "radio", "options": ["Below ₹ 25,000", "₹ 25,001 - ₹ 50,000", "₹ 50,001 - ₹ 1,00,000", "₹ 1,00,001 - ₹ 2,00,000", "Above ₹ 2,00,000", "Prefer not to disclose"]},
            {"id": "q8", "text": "What is your current marital / household status?", "type": "radio", "options": ["Single", "Married without children", "Married with children", "In a relationship (not married)", "Divorced"]},
        ]
    },
    {
        "title": "Recent Trip Details",
        "icon": "🗺️",
        "description": "Think about your most recent trip outside Mumbai.",
        "questions": [
            {"id": "q9", "text": "Which type of destination did you visit on your most recent trip?", "type": "radio", "options": ["Hill Station / Mountain", "Coastal / Beach", "Cultural / Heritage", "Religious / Pilgrimage", "Nature / Wildlife / Eco-tourism", "International", "Other"]},
            {"id": "q10", "text": "Who did you travel with on this trip?", "type": "radio", "options": ["Alone (Solo travel)", "With spouse", "With family", "With friends", "With colleagues / office group", "Organised tour group"]},
            {"id": "q11", "text": "What was your approximate total budget for that trip (per person, all expenses)?", "type": "radio", "options": ["Below ₹ 5,000", "₹ 5,001 - ₹ 15,000", "₹ 15,001 - ₹ 30,000", "₹ 30,001 - ₹ 50,000", "Above ₹ 50,000"]},
            {"id": "q12", "text": "How many leisure trips (24+ hours away) have you taken in the past 12 months?", "type": "radio", "options": ["1", "2-3", "4-5", "More than 5"]},
            {"id": "q13", "text": "What was your PRIMARY source of information when choosing this destination?", "type": "radio", "options": ["Word of mouth (family / friends)", "Social media (Instagram, YouTube, Reels, etc.)", "Travel websites / blogs / OTAs (MakeMyTrip, TripAdvisor, etc.)", "Personal prior experience", "Travel agent / tour operator", "TV or print media", "Online search engine (Google)"]},
        ]
    },
    {
        "title": "Push Motivation – Escape & Relaxation",
        "icon": "🌴",
        "description": "Rate how strongly you agree with each statement.",
        "questions": [
            {"id": "q14_1", "text": "Travelling helps me escape from the stress and pressure of daily work and city life.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q14_2", "text": "I travel to rest, relax, and recharge my mind and body.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q14_3", "text": "Getting away from Mumbai's crowds and noise is an important reason I travel.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q14_4", "text": "Travel allows me to temporarily forget my responsibilities and worries.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
        ]
    },
    {
        "title": "Push Motivation – Adventure & Excitement",
        "icon": "🏔️",
        "description": "Rate how strongly you agree with each statement.",
        "questions": [
            {"id": "q15_1", "text": "I am motivated to travel because I enjoy exciting and thrilling experiences.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q15_2", "text": "I seek destinations that offer adventure activities (trekking, water sports, etc.).", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q15_3", "text": "The possibility of experiencing something new and risky excites me about travel.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q15_4", "text": "Trying new and adrenaline-filled activities is an important part of my travel.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
        ]
    },
    {
        "title": "Push Motivation – Family & Bonding",
        "icon": "👨‍👩‍👧‍👦",
        "description": "Rate how strongly you agree with each statement.",
        "questions": [
            {"id": "q16_1", "text": "Spending quality time with my family is a primary reason I travel.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q16_2", "text": "I travel to strengthen relationships with my family members / loved ones.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q16_3", "text": "Travelling as a family / with close ones makes the experience more meaningful.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q16_4", "text": "Traveling allows me to create lasting memories with my family.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
        ]
    },
    {
        "title": "Push Motivation – Culture & Knowledge",
        "icon": "📚",
        "description": "Rate how strongly you agree with each statement.",
        "questions": [
            {"id": "q17_1", "text": "I travel to learn about and experience new cultures, traditions, and ways of life.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q17_2", "text": "Meeting and interacting with people from different backgrounds motivates me to travel.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q17_3", "text": "Travel broadens my perspective on the world and different societies.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q17_4", "text": "I am interested in visiting places that offer historical, cultural, or educational experiences.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
        ]
    },
    {
        "title": "Push Motivation – Social Status",
        "icon": "📸",
        "description": "Rate how strongly you agree with each statement.",
        "questions": [
            {"id": "q18_1", "text": "Travelling to popular or exotic destinations improves my status among peers.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q18_2", "text": "I enjoy sharing my travel experiences on social media to inspire others.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q18_3", "text": "Visiting well-known destinations makes me feel accomplished and distinguished.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q18_4", "text": "Travelling to unique or exclusive destinations enhances my personal image.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
        ]
    },
    {
        "title": "Pull Motivation – Safety & Enjoyment",
        "icon": "🛡️",
        "description": "Rate how strongly you agree with each statement.",
        "questions": [
            {"id": "q19_1", "text": "I prefer travelling to destinations where I feel personally safe and secure.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q19_2", "text": "The enjoyment and fun aspect of a trip is a major driver of my travel decision.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q19_3", "text": "I am more likely to travel if I know the destination is safe for travellers like me.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q19_4", "text": "I prefer destinations that offer both safety and enjoyable recreational activities.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
        ]
    },
    {
        "title": "Pull Motivation – Nature & Environment",
        "icon": "🌿",
        "description": "Rate how important each factor is for you.",
        "questions": [
            {"id": "q20_1", "text": "Beautiful natural landscapes attract me to a destination.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q20_2", "text": "Pleasant climate and weather conditions at the destination are important to me.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q20_3", "text": "Clean, unpolluted environments significantly influence my destination choice.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q20_4", "text": "A clean, well-maintained destination environment is important in my travel choice.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
        ]
    },
    {
        "title": "Pull Motivation – Affordability",
        "icon": "💰",
        "description": "Rate how important each factor is for you.",
        "questions": [
            {"id": "q21_1", "text": "Affordable accommodation and food options are a major factor in choosing a destination.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q21_2", "text": "Overall value for money is a critical consideration in my destination decision.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q21_3", "text": "I compare the cost of travel to different destinations before making a final choice.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q21_4", "text": "Availability of budget-friendly transport to the destination influences my choice.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
        ]
    },
    {
        "title": "Pull Motivation – Culture & Events",
        "icon": "🎭",
        "description": "Rate how important each factor is for you.",
        "questions": [
            {"id": "q22_1", "text": "Local festivals, fairs, and cultural events attract me to a destination.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q22_2", "text": "The availability of cultural and arts experiences (museums, folk performances, etc.) is important.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q22_3", "text": "I prefer destinations that offer authentic local experiences and traditions.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
        ]
    },
    {
        "title": "Pull Motivation – Nightlife, Food & Shopping",
        "icon": "🍜",
        "description": "Rate how important each factor is for you.",
        "questions": [
            {"id": "q23_1", "text": "A vibrant nightlife, entertainment options, and social scene attract me to a destination.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q23_2", "text": "Local food, street food, and regional cuisine are an important part of my travel motivation.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q23_3", "text": "The variety of restaurants, cafes, and dining experiences at a destination matters to me.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q23_4", "text": "Availability of good shopping facilities (local markets, malls, souvenirs) attracts me.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q23_5", "text": "Hygienic conditions (food, water, sanitation) at a destination influence my choice.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
        ]
    },
    {
        "title": "Pull Motivation – Safety & Stability",
        "icon": "🏥",
        "description": "Rate how important each factor is for you.",
        "questions": [
            {"id": "q24_1", "text": "Low crime rates and perceived personal safety strongly influence my destination choice.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q24_2", "text": "Political stability and absence of civil unrest at a destination affects my travel decision.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q24_3", "text": "Availability of medical facilities and emergency services at a destination is important.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
        ]
    },
    {
        "title": "Pull Motivation – Heritage Sites",
        "icon": "🏛️",
        "description": "Rate how important each factor is for you.",
        "questions": [
            {"id": "q25_1", "text": "The presence of well-known historical monuments and heritage sites attracts me to a destination.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q25_2", "text": "UNESCO World Heritage Sites or protected monuments are significant draws for me.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q25_3", "text": "I prefer destinations with a rich, documented cultural and historical legacy.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
        ]
    },
    {
        "title": "Destination Image – Infrastructure",
        "icon": "🏨",
        "description": "Rate how important each factor is for you.",
        "questions": [
            {"id": "q26_1", "text": "Good quality and reliable accommodation (hotels, homestays, resorts) is important to my choice.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q26_2", "text": "Efficient and comfortable transport options (flights, trains, roads) within the destination matter.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q26_3", "text": "Friendly and helpful local people and tourism staff positively influence my destination choice.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
            {"id": "q26_4", "text": "Availability of tourist facilities (guided tours, information centres, maps) is important.", "type": "radio", "options": ["Not at all important", "Slightly important", "Moderately important", "Important", "Very important"]},
        ]
    },
    {
        "title": "Destination Image – Quality Ratings",
        "icon": "⭐",
        "description": "Rate the quality of each aspect for the destination type you last visited.",
        "questions": [
            {"id": "q27_1", "text": "Quality and variety of accommodation options available.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_2", "text": "Quality of local food, restaurants, and dining options.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_3", "text": "Ease and comfort of transport to and within the destination.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_4", "text": "Quality of tourism infrastructure (signage, visitor centres, guides, facilities).", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_5", "text": "Natural beauty, scenery, and outdoor appeal.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_6", "text": "Cleanliness and environmental quality.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_7", "text": "Climate and weather suitability for travel.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_8", "text": "Richness of cultural attractions, monuments, and heritage.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_9", "text": "Local festivals, fairs, and cultural events.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_10", "text": "Friendliness and hospitality of local residents.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_11", "text": "Perceived personal safety and security for travellers.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_12", "text": "Uniqueness and novelty of experiences available.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
            {"id": "q27_13", "text": "Value for money compared to other destination types.", "type": "radio", "options": ["Very Poor", "Poor", "Average", "Good", "Excellent"]},
        ]
    },
    {
        "title": "Social Media & Word of Mouth",
        "icon": "📱",
        "description": "Rate how strongly you agree with each statement.",
        "questions": [
            {"id": "q28_1", "text": "Social media content (Instagram, YouTube, Reels, travel influencers) influences my destination choice.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q28_2", "text": "I often discover new travel destinations through social media posts and travel vlogs.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q28_3", "text": "I regularly check photos, reviews, and ratings on social media before choosing a destination.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q28_4", "text": "Positive social media coverage of a destination makes me significantly more likely to visit it.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q29_1", "text": "Recommendations from family and close friends strongly influence my destination choice.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"id": "q29_2", "text": "If my social circle visits and recommends a destination, I am more likely to visit it.", "type": "radio", "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
        ]
    },
]

# Flatten all questions for CSV schema
ALL_QUESTIONS = [q for sec in SECTIONS for q in sec["questions"]]
TOTAL_QUESTIONS = len(ALL_QUESTIONS)

# ── Save Logic (unchanged from original) ──────────────────────────────────────
def save_response():
    """Save the current survey response to the CSV file (upsert)."""
    data = dict(st.session_state.responses)
    data["Session_ID"] = st.session_state.session_id

    if data.get("q1") == "No" or data.get("q2") == "No":
        data["Completed"] = False
        data["Screened_Out"] = True
    elif st.session_state.completed:
        data["Completed"] = True
        data["Screened_Out"] = False
    else:
        data["Completed"] = False
        data["Screened_Out"] = False

    data["Timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format_col(q_id):
        return "Q." + q_id[1:] if q_id.startswith("q") else q_id

    all_cols = ["Session_ID"] + [format_col(q["id"]) for q in ALL_QUESTIONS] + ["Completed", "Screened_Out", "Timestamp"]

    row = {"Session_ID": data.get("Session_ID", "")}
    for q in ALL_QUESTIONS:
        row[format_col(q["id"])] = data.get(q["id"], "")
    row["Completed"] = data.get("Completed", "")
    row["Screened_Out"] = data.get("Screened_Out", "")
    row["Timestamp"] = data.get("Timestamp", "")

    df_new = pd.DataFrame([row], columns=all_cols)

    try:
        if os.path.exists(CSV_FILE):
            try:
                df_existing = pd.read_csv(CSV_FILE, encoding="utf-8-sig")
            except Exception:
                df_existing = pd.DataFrame(columns=all_cols)
            for col in all_cols:
                if col not in df_existing.columns:
                    df_existing[col] = ""
            df_existing = df_existing.reindex(columns=all_cols, fill_value="")
            if st.session_state.session_id in df_existing["Session_ID"].values:
                df_existing.loc[df_existing["Session_ID"] == st.session_state.session_id, all_cols] = df_new.iloc[0].values
            else:
                df_existing = pd.concat([df_existing, df_new], ignore_index=True)
            df_existing.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        else:
            df_new.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
            
        # ── Google Sheets Integration ──
        gc = get_gspread_client()
        if gc:
            try:
                sh = gc.open_by_key("11WXKYFOLQLC7iNHXwOJFjKZoyRP7Mky2JGscRO8BtMM")
                worksheet = sh.sheet1
                
                # Check if headers exist
                existing_data = worksheet.get_all_values()
                if not existing_data:
                    worksheet.append_row(all_cols)
                    existing_data = [all_cols]
                
                headers = existing_data[0]
                # Reorder to match sheet headers
                ordered_values = [str(row.get(h, "")) for h in headers]
                
                # Upsert logic (find by Session_ID)
                session_index = -1
                if "Session_ID" in headers:
                    sid_idx = headers.index("Session_ID")
                    for i, r in enumerate(existing_data):
                        if i > 0 and len(r) > sid_idx and str(r[sid_idx]) == str(st.session_state.session_id):
                            session_index = i + 1 # 1-based index in sheets
                            break
                
                from gspread.utils import rowcol_to_a1
                if session_index > 0: # Update existing
                    # Using A1 notation for the exact row range
                    cell_range = f"{rowcol_to_a1(session_index, 1)}:{rowcol_to_a1(session_index, len(headers))}"
                    worksheet.update(cell_range, [ordered_values])
                else: # Append new
                    worksheet.append_row(ordered_values)
            except Exception as e:
                # Don't throw error to user if just Google Sheets fails, but log it
                st.error(f"⚠️ Google Sheets Sync Failed (CSV saved): {str(e)}")
                
    except Exception as e:
        st.error(f"⚠️ Failed to save response: {e}")


# ── Main App ───────────────────────────────────────────────────────────────────
def main():
    apply_custom_css()

    # ── Session init ───────────────────────────────────────────────────────────
    if "current_section_idx" not in st.session_state:
        st.session_state.current_section_idx = 0
        st.session_state.responses = {}
        st.session_state.completed = False
        st.session_state.screened_out = False
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.survey_started = False

    # ── Completed ──────────────────────────────────────────────────────────────
    if st.session_state.completed:
        st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("<h1>Thank You! 🙏</h1>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:1.15rem; color:#f1f5f9 !important;'>Your responses have been successfully recorded.</p>", unsafe_allow_html=True)
        st.markdown("<p class='secondary-text'>Thank you for contributing to our research on Mumbaikars' travel motivations and destination preferences. Your honest answers will help shape the future of tourism studies at the University of Mumbai.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Submit Another Response"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── Screened out ───────────────────────────────────────────────────────────
    if st.session_state.screened_out:
        st.markdown('<div class="main-card" style="text-align:center;">', unsafe_allow_html=True)
        st.info("Thank you for your time, but you do not meet the criteria for this survey.")
        if st.button("Start Over"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── End check ──────────────────────────────────────────────────────────────
    if st.session_state.current_section_idx >= len(SECTIONS):
        st.session_state.completed = True
        save_response()
        st.rerun()
        return

    # ══════════════════════════════════════════════════════════════════════════
    #   WELCOME / LANDING SCREEN
    # ══════════════════════════════════════════════════════════════════════════
    if not st.session_state.survey_started:
        # ── Title card ─────────────────────────────────────────────────────────
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;"><span class="welcome-badge">📝 Academic Research</span></div>', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>Mumbaikars Travel Survey</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8 !important; font-size:1rem;'>Understanding travel motivations & destination preferences of Mumbai residents</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Hero image ─────────────────────────────────────────────────────────
        hero_path = os.path.join(BASE_DIR, "assets", "mumbai_hero.png")
        if os.path.exists(hero_path):
            st.markdown('<div class="hero-img-container">', unsafe_allow_html=True)
            st.image(hero_path, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Info card ──────────────────────────────────────────────────────────
        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        st.markdown("""
        <div class="trust-signal">
            <strong>We are students from the Department of Statistics, University of Mumbai.</strong><br><br>
            We are conducting academic research on the travel motivations and destination preferences of 
            Mumbai residents. All responses are <strong>completely anonymous</strong> and will be used 
            <strong>solely for academic purposes</strong>.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:center; margin-top:0.5rem;'>What makes you pack your bags and leave the city?</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p class='secondary-text' style='text-align:center; max-width:88%; margin:0 auto;'>
        Is it the call of the mountains, the pull of a beach sunset, or simply the need to escape Mumbai's pace? 
        Help us understand the real reasons Mumbaikars travel — and the experiences that matter most to you.
        </p>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="stat-row">
            <div class="stat-item">
                <span class="stat-icon">⏱️</span>
                <span class="stat-label">5–7 Minutes</span>
            </div>
            <div class="stat-item">
                <span class="stat-icon">📋</span>
                <span class="stat-label">18 Sections</span>
            </div>
            <div class="stat-item">
                <span class="stat-icon">🔒</span>
                <span class="stat-label">100% Anonymous</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Start Survey →", use_container_width=True, type="primary"):
                st.session_state.survey_started = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ══════════════════════════════════════════════════════════════════════════
    #   SURVEY WIZARD
    # ══════════════════════════════════════════════════════════════════════════
    total_sections = len(SECTIONS)
    idx = st.session_state.current_section_idx
    progress = (idx + 1) / total_sections

    st.markdown(f"<div class='progress-text'>Section {idx + 1} of {total_sections}</div>", unsafe_allow_html=True)
    st.progress(progress)

    sec = SECTIONS[idx]

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"<span class='section-label'>{sec['icon']}  {sec['title']}</span>", unsafe_allow_html=True)
    st.markdown(f"<p class='secondary-text'>{sec['description']}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.04); margin:1rem 0;'>", unsafe_allow_html=True)

    with st.form(key=f"form_sec_{idx}", border=False):
        temp = {}
        all_answered = True

        for q in sec["questions"]:
            st.markdown(f"**{q['text']}**")
            prev = st.session_state.responses.get(q["id"])
            def_idx = q["options"].index(prev) if prev in q["options"] else None

            choice = st.radio(
                "Select:", options=q["options"],
                index=def_idx, label_visibility="collapsed",
                key=f"w_{q['id']}"
            )
            temp[q["id"]] = choice
            if choice is None:
                all_answered = False
            st.markdown("<br>", unsafe_allow_html=True)

        # Navigation
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if idx > 0:
                if st.form_submit_button("← Back", use_container_width=True):
                    for k, v in temp.items():
                        if v is not None:
                            st.session_state.responses[k] = v
                    st.session_state.current_section_idx -= 1
                    save_response()
                    st.rerun()
        with c3:
            label = "Finish & Submit" if idx == total_sections - 1 else "Next →"
            if st.form_submit_button(label, type="primary", use_container_width=True):
                if not all_answered:
                    st.error("⚠️ Please answer all questions in this section.")
                else:
                    for k, v in temp.items():
                        st.session_state.responses[k] = v
                    save_response()
                    # Screening check (section 0)
                    if idx == 0:
                        if temp.get("q1") == "No" or temp.get("q2") == "No":
                            st.session_state.screened_out = True
                            st.rerun()
                            return
                    st.session_state.current_section_idx += 1
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
