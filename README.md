# Mumbai Travel Survey Bot

Automated conversational survey bot designed to capture commuting patterns, preferred travel modes, peak-hour bottlenecks, and transit satisfaction across Mumbai suburban transport networks.

## Application Architecture

Streamlit conversational interface guiding users through structured demographic, mode selection, frequency, and route satisfaction questions:
- **Suburban Rail**: Central, Western, and Harbour line commuting metrics.
- **Metro & Monorail**: Urban rapid transit adoption patterns.
- **Road Transit**: BEST Bus, auto-rickshaw, ride-share, and private vehicle travel.

## Core Features & Data Flow

| Feature Module | Method / Logic | Output Metric |
|---|---|---|
| Survey Flow Engine | Stateful session tracking in Streamlit | Structured survey response row |
| Questionnaire Parser | Text-based prompt sequence parsing | Standardized question flow |
| Response Logger | Automated CSV persistence | `survey_responses.csv` data log |

## Project Structure

```
mumbai_travel_survey_bot/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── survey_bot_preview.png
├── mumbai_travel_survey_bot.py
├── questionnaire.txt
├── research_questionnaire.pdf
├── survey_responses.csv
├── requirements.txt
└── README.md
```

## How to Run

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Launch Streamlit Application
```bash
streamlit run mumbai_travel_survey_bot.py
```

## Author

Sanman Kadam  
MSc Statistics | Data Analyst
