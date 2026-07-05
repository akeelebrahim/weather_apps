import streamlit as st
from PIL import Image
import pandas as pd
import os
from datetime import datetime
import weather_utils as utils  # Import the helper logic

# Project root = one level up from this src/ folder (used to locate assets)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# -------------------------------------------------------------- Aditional part to change the BG image
# https://medium.com/@hriskikesh.yadav332/setting-cool-background-image-in-streamlit-app-cab8c8ee2a8f
page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://cdn.wallpapersafari.com/88/75/cLUQqJ.jpg");
  #background-image: url("https://images8.alphacoders.com/126/thumb-1920-1263205.jpg");
  background-size: cover;
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_element, unsafe_allow_html=True)
# -------------------------------------------------------------- Aditional part to change the BG image

icon_image = Image.open(os.path.join(BASE_DIR, "assets", "weather_icon.png"))

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
        "4. 📋 View all observations",
        "🚀 Mandatory Stretch Goals"
    ]
)

# App logic based on selection
if navigation == "🏠 Welcome":
   st.markdown("""
    ### Welcome to my Weather Dashboard! 👋
    ## Select an option from the sidebar menu on the left to get started:
    
    *   #### Record Weather: Input daily temperatures, humidity, conditions, and wind speed[Option: 1].
    *   #### View Statistics: Analyze current trends, maximums, minimums, and averages[Option: 2].
    *   #### Search observations: Look up specific weather conditions recorded by date[Option: 3].
    *   #### View All: Display the historical climate observation database logs[Option: 4].
            
    #### ***Thank you***
    """)
#-------------------------------------------------------------------------Menu option 1
elif navigation == "1. 📝 Record Weather observation":
    st.header("📝 Record New Observation")

    with st.form("weather_form", clear_on_submit=True):
        date_input = st.date_input("Select Date", value=datetime.today())
        date_str = date_input.strftime("%m-%d-%Y") # Formats to MM-DD-YYYY
        
        temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, step=0.1)
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
#=========================================================================Mandatory Stretch Goals

elif navigation == "🚀 Mandatory Stretch Goals":
    st.header("🚀 Advanced Analytics (Mandatory Stretch Goals)")
#-------------------------- to large the fonts, it was very small
# https://docs.streamlit.io/develop/api-reference/text/st.markdown
    st.markdown("""
    <style>
    button[data-baseweb="tab"] p {
        font-size: 20px !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)
#--------------------------
    
    # Create sub-tabs to house each of the 5 required goals
    tab1, tab2, tab3, tab4_5 = st.tabs([
        "📊 Text Graph Trends", 
        "📅 Month/Season Filter", 
        "🔮 Weather Prediction", 
        "🏆 Climate Records & YoY"
    ])
    
    # ---------------------------------------------------------
    # STRETCH GOAL 1: TEXT-BASED TEMPERATURE GRAPH
    # ---------------------------------------------------------
    with tab1:
        st.subheader("Text-Based Temperature Trends")
        st.write("A clean text visual tracking our most recent historical logs:")
        # Display as a code block so fonts align perfectly into a chart
        graph_output = utils.generate_text_graph(limit=12)
        st.code(graph_output)
        
    # ---------------------------------------------------------
    # STRETCH GOAL 2: FILTER OBSERVATIONS
    # ---------------------------------------------------------
    with tab2:
        st.subheader("Filter Observations by Timeframe")
        filter_type = st.radio("Choose filtering mode:", ["Month", "Season"])
        
        if filter_type == "Month":
            months_dict = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12"}
            month_select = st.selectbox("Select Month", list(months_dict.keys()))
            filtered_results = utils.filter_by_timeframe("Month", months_dict[month_select])
        else:
            season_select = st.selectbox("Select Season", ["Winter (Dec-Feb)", "Summer (Jun-Sep)", "Spring/Autumn (Transitional)"])
            filtered_results = utils.filter_by_timeframe("Season", season_select)
            
        st.dataframe(filtered_results, use_container_width=True)

    # ---------------------------------------------------------
    # STRETCH GOAL 3: HISTORICAL CLIMATE PREDICTIONS
    # ---------------------------------------------------------
    with tab3:
        st.subheader("Predictive Analytics Engine")
        st.write("Calculates tomorrow's likely outlook based on long-term historical records.")
        
        target_dt = st.date_input("Select a target calendar date to simulate:")
        month_code = target_dt.strftime("%m")
        
        prediction = utils.predict_tomorrow(month_code)
        if prediction:
            p_col1, p_col2, p_col3 = st.columns(3)
            p_col1.metric("Predicted Temp", f"{prediction['expected_temp']:.1f} °C")
            p_col2.metric("Predicted Humidity", f"{int(prediction['expected_humidity'])} %")
            p_col3.info(f"Likely Sky Condition: **{prediction['likely_condition']}**")

    # ---------------------------------------------------------
    # STRETCH GOALS 4 & 5: YOY COMPARISONS & ALL-TIME RECORDS
    # ---------------------------------------------------------
    with tab4_5:
        climate_metrics = utils.get_climate_records()
        
        if climate_metrics is not None:
            st.subheader("📊 Year-over-Year Climate Comparison (Goal 4)")
            st.write("Historical baseline comparison matrix grouped by calendar year:")
            # --- RENDER AS A CLEAN STREAMLIT INTERACTIVE TABLE ---
            st.dataframe(
                climate_metrics['yoy_table'].style.format({
                    'Average_Temperature': '{:.1f} °C',
                    'Maximum_Temperature': '{:.1f} °C',
                    'Minimum_Temperature': '{:.1f} °C'
                }),
                use_container_width=True
            )
            st.markdown("---")

            st.subheader("🏆 Historic Record Breakers (Goal 5)")
            r_col1, r_col2 = st.columns(2)
            r_col1.metric("All-Time Highest Temp", f"{climate_metrics['highest_temp']} °C", f"On {climate_metrics['highest_date']}")
            r_col2.metric("All-Time Lowest Temp", f"{climate_metrics['lowest_temp']} °C", f"On {climate_metrics['lowest_date']}")
            
            st.markdown("---")
# -----------------------------------------------------
        else:
            st.warning("No historical entries found to process calculations.")
#=========================================================================Mandatory Stretch Goals
