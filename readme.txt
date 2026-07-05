# Weather Tracker App 🌦️

Welcome to my Weather Tracker application! I built this project for my data science course to help weather enthusiasts log local climate data and see trends over time. It is built completely using Python and Streamlit for the front-end interface.

The app is fully localized to handle the unique weather patterns of Bahrain, from the scorching, humid summer days to the cooler rainy winter months.

## Features
* **Welcome Screen:** A clean landing page introducing the dashboard layout.
* **Record Weather:** Lets you enter temperature, humidity, wind speed, and conditions via a simple form.
* **View Statistics:** Instantly calculates the average, max, and minimum temperatures, plus the most common weather type.
* **Search by Date:** Look up specific historical data points by choosing a date from a calendar.
* **View All:** Displays the whole database logs in a clean table view.

## File Structure
* `main_app.py`: Handles all the Streamlit interface, buttons, inputs and page layouts.
* `weather_utils.py`: Contains the logic functions for reading/writing the CSV file and doing the math.
* `weather_observations.csv`: The database file holding all our localized weather observations.

## How to Run It
1. Make sure you have python and the required libraries installed (`pip install streamlit pandas pillow`)
2. Clone this repo to your machine.
3. Open your terminal in the project folder and run:
   ```bash
   streamlit run main_app.py

## Resources:
* Report by Ministry of Transportation and Telecommunications
* Title: METEOROLOGICAL DIRECTORATE CLIMATE SECTION
* Link: https://www.bahrainweather.gov.bh/files/climate/monthly-climate-summary.pdf