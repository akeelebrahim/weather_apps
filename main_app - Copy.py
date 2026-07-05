import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import weather_utils as utils  # Import the helper logic


page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://cdn.wallpapersafari.com/88/75/cLUQqJ.jpg");
  background-size: cover;
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_element, unsafe_allow_html=True)





icon_image = Image.open("weather_icon.png")

st.set_page_config(
    page_title="🌦️ Weather Observation App",
    page_icon=icon_image,
    layout="wide"
)

st.title("🌦️ Weather Observation App")

# Navigation menu in the sidebar (Added Home/Welcome as the default option)
navigation = st.sidebar.radio(
    "Select an Option:",
    [
        "🏠 Welcome",
        "1. 📝 Record Weather observation",
        "2. 📊 View weather statistics",
        "3. 🔍 Search observations by date",
        "4. 📋 View all observations"
    ]
)

# App logic based on selection
if navigation == "🏠 Welcome":
    st.markdown("""
    ### Welcome to my Weather Dashboard! 👋
    Select an option from the sidebar menu on the left to get started:
    
    *   **Record Weather:** Input daily temperatures, humidity, conditions, and wind speed[Option: 1].
    *   **View Statistics:** Analyze current trends, maximums, minimums, and averages[Option: 2].
    *   **Search observations:** Look up specific weather conditions recorded by date[Option: 3].
    *   **View All:** Display the historical climate observation database logs[Option: 4].\n
        ***Thank you***
    """)
#-------------------------------------------------------------------------Menu option 1
elif navigation == "1. 📝 Record Weather observation":
    st.header("📝 Record New Observation")

    with st.form("weather_form", clear_on_submit=True):
        date_input = st.date_input("Select Date", value=datetime.today())
        date_str = date_input.strftime("%m-%d-%Y") # Formats to MM-DD-YYYY
        
        temp = st.number_input("Temperature (°C)", min_value=38.0, max_value=60.0, step=0.1)
        condition = st.selectbox("Condition", ["Sunny", "Cloudy", "Rainy", "Dusty"])
        humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=50)
        wind = st.number_input("Wind Speed (km/h)", min_value=0, max_value=150, step=1)
    
        submit_button = st.form_submit_button("Save Observation")

    if submit_button:
        utils.add_observation(date_str, temp, condition, humidity, wind)
        st.success(f"Successfully recorded weather for {date_str}!")
#-------------------------------------------------------------------------Menu option 2
elif navigation == "2. 📊 View weather statistics":
    st.header("📊 Weather Statistics")

    stats = utils.get_weather_stats()
    
    if stats is None:
        st.warning("No weather data found yet! Try adding an observation first.")
    else:
        # Create 3 clean columns side-by-side for a dashboard feel
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Average Temperature", value=f"{stats['avg_temp']:.1f} °C")
        with col2:
            st.metric(label="Highest Temperature (Max)", value=f"{stats['max_temp']:.1f} °C")
        with col3:
            st.metric(label="Lowest Temperature (Min)", value=f"{stats['min_temp']:.1f} °C")
            
        # Add a visual separator before showing the categorical mode
        st.markdown("---")
        st.subheader("☁️ Dominant Weather Trend")
        st.info(f"The most commonly recorded weather condition in our logs is: **{stats['common_condition']}**")

#-------------------------------------------------------------------------Menu option 3
elif navigation == "3. 🔍 Search observations by date":
    st.header("🔍 Search Observations")

    # 1. Let the user select a date visually using a date picker calendar
    search_date = st.date_input("Select a date to look up:")
    
    # 2. Format the selected date to match our CSV string format (MM-DD-YYYY)
    search_date_str = search_date.strftime("%m-%d-%Y")
    
    # 3. Call our utility function when the user wants to fetch data
    results = utils.search_by_date(search_date_str)
    
    # 4. Check if we found anything and display it clearly
    if not results.empty:
        st.success(f"Found observation data for {search_date_str}:")
        # Display the result as a clean, styled table instead of raw code
        st.dataframe(results, use_container_width=True)
    else:
        st.info(f"No records found for {search_date_str}. Try checking another date!")

#-------------------------------------------------------------------------Menu option 4
elif navigation == "4. 📋 View all observations":
    st.header("📋 All Observations")
    utils.display_all()