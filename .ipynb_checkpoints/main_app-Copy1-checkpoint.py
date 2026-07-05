import streamlit as st
from PIL import Image
import pandas as pd


from datetime import datetime
import weather_utils as utils  # Import the helper logic

#from weather_utils import display_all
#import weather_utils as utils


icon_image = Image.open("weather_icon.png")

st.set_page_config(
    page_title="🌦️ Weather Observation App",
    page_icon=icon_image,
    layout="wide"
)

# 
st.title("🌦️ Weather Observation App")

# Navigation menu in the sidebar
navigation = st.sidebar.radio(
    "Select an Option:",
    [
        "1. 📝 Record Weather observation",
        "2. 📊 View weather statistics",
        "3. 🔍 Search observations by date",
        "4. 📋 View all observations"
    ]
)

# App logic based on selection
if navigation == "1. 📝 Record Weather observation":
    st.header("📝 Record New Observation")
    # This section for adding new Weather Observation
    #st.title("📝 Record New Weather Observation")

    # Save when submit button is clicked
    with st.form("weather_form", clear_on_submit=True):
        date_input = st.date_input("Select Date", value=datetime.today())
        date_str = date_input.strftime("%m-%d-%Y") # Formats to MM-DD-YYYY
    
        temp = st.number_input("Temperature (°C)", min_value=40.0, max_value=60.0, step=0.1)
        condition = st.selectbox("Condition", ["Sunny", "Cloudy", "Rainy", "Dusty"])
        humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=50)
        wind = st.number_input("Wind Speed (km/h)", min_value=0, max_value=150, step=1)
    
        submit_button = st.form_submit_button("Save Observation")

    if submit_button:
        # Call utility function to write to CSV file
        utils.add_observation(date_str, temp, condition, humidity, wind)
        st.success(f"Successfully recorded weather for {date_str}!")

    

elif navigation == "2. 📊 View weather statistics":
    st.header("📊 Weather Statistics")
    # This section for viewing Weather stats
    # A seperate function to be called

elif navigation == "3. 🔍 Search observations by date":
    st.header("🔍 Search Observations")
    # This section for searching observations by date
    # A seperate function to be called

elif navigation == "4. 📋 View all observations":
    st.header("📋 All Observations")
    # This section for viewing all observations
    # A seperate function to be called
    #st.write("Heluuuuuuuuuuuu")
    utils.display_all()
    #display_all()
    