# Weather Tracker App 🌦️

Welcome to my Weather Tracker application! I built this project for my data science course to help weather enthusiasts log local climate data and see trends over time. It is built completely using Python and Streamlit for the front-end interface.

The app is fully localized to handle the unique weather patterns of Bahrain, from the scorching, humid summer days to the cooler rainy winter months.

## Features
* **Welcome Screen:** A clean landing page introducing the dashboard layout.
* **Record Weather:** Lets you enter temperature, humidity, wind speed, and conditions via a simple form.
* **View Statistics:** Instantly calculates the average, max, and minimum temperatures, plus the most common weather type.
* **Search by Date:** Look up specific historical data points by choosing a date from a calendar.
* **View All:** Displays the whole database logs in a clean table view.

## Stretch Goals - Mandatory
All 5 required stretch goals are implemented under the **🚀 Mandatory Stretch Goals** menu option:
1. **Text Graph Trends:** Displays temperature trends as text-based bar graphs of the most recent logs.
2. **Month/Season Filter:** Filters observations by calendar month or Bahrain seasonal groupings (Summer, Winter, Transitional).
3. **Weather Prediction:** Predicts tomorrow's outlook based on historical records of the selected month.
4. **Year-over-Year Comparison:** Compares yearly averages, maximums, and minimums in a summary table.
5. **Record Breakers:** Tracks and displays the all-time highest and lowest recorded temperatures.

## File Structure
```
├── README.md
├── src/
│   ├── main_app.py             # All the Streamlit interface, buttons, inputs and page layouts
│   └── weather_utils.py        # Logic functions for reading/writing the CSV file and doing the math
├── data/
│   ├── weather_observations.csv    # The database file holding all our localized weather observations
│   └── monthly-climate-summary.csv # Reference climate data from the Meteorological Directorate
├── assets/
│   ├── weather_icon.png        # App page icon
│   └── Weather Radar Wallpaper.jpg
└── docs/
    ├── The Weather Tracker App Slides.pptx  # Presentation slide deck
    └── monthly-climate-summary.pdf          # Source report
```

## How to Run It
1. Make sure you have python and the required libraries installed (`pip install streamlit pandas pillow`)
2. Clone this repo to your machine.
3. Open your terminal in the project folder and run:
   ```bash
   streamlit run src/main_app.py
   ```
## App Video tutorial available in 'Assets' folder
### App live link to test: Best viewed using full screen 90% browser zoom
# https://weatherapps.streamlit.app/
## Presentation
* Slide deck: `docs/The Weather Tracker App Slides.pptx` (included in this repository)
* Repository: https://github.com/akeelebrahim/weather_apps

## Resources:
* Report by Ministry of Transportation and Telecommunications
* Title: METEOROLOGICAL DIRECTORATE CLIMATE SECTION - MONTHLY WEATHER SUMMARY – JUNE 2023
* Link: https://www.bahrainweather.gov.bh/files/climate/monthly-climate-summary.pdf
