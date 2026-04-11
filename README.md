# Mumbai Travel Decision-Making Survey Bot 🌍

A professional, conversational Streamlit web application designed to collect and structure research survey responses regarding the travel decision-making patterns of Mumbai residents. 

## Features
- **Conversational UI**: Questions are presented one at a time for a low-friction, mobile-friendly user experience.
- **Dynamic Asset Loading**: Displays beautiful, random photorealistic landmarks of Mumbai (Gateway of India, Marine Drive, CST, Sea Link) at the top of every question.
- **Smart Screening**: Automatically screens out participants who do not meet the criteria (e.g., non-residents of Mumbai or those who haven't traveled recently).
- **Automated Data Processing**: All responses are appended seamlessly into a structured `survey_responses.csv` file, making it perfectly prepped for Exploratory Data Analysis (EDA).

## Prerequisites

Make sure you have Python 3.8+ installed. 

Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

## How to Run

Launch the Streamlit app locally by executing the following command in your terminal:
```bash
streamlit run mumbai_travel_survey_bot.py
```

The application will automatically open in your default web browser at `http://localhost:8502`.

## Data Management
As participants complete the survey, their data is locally logged into `survey_responses.csv`. 

> **Privacy Note:** `survey_responses.csv` is explicitly added to the `.gitignore` to prevent you from accidentally uploading live participant data to public repositories. If you wish to share the dataset, ensure you manually scrub any PII before distributing it.
