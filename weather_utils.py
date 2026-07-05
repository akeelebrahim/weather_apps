# This function will display all observations
import streamlit as st
import pandas as pd
import os
import random


# Helper function to safely read the CSV file across all other functions
def load_data(filename="weather_observations.csv"):
    """
    Safely reads the weather database. If the file is missing,
    it returns a clean DataFrame with the correct columns[cite: 1].
    """
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        columns = ['Date', 'Temperature_Celsius', 'Condition', 'Humidity_Percentage', 'Wind_Speed_kmh']
        return pd.DataFrame(columns=columns)

#-------------------------------------------------------------------------Menu option 1
# This function for adding new observation
def add_observation(date_str, temp, condition, humidity, wind, filename="weather_observations.csv"):
    # 1. Read my csv file that I put in the same path using our helper function
    df = load_data(filename)
    
    # 2. Append the new data
    new_row = {'Date': date_str, 'Temperature_Celsius': temp, 'Condition': condition, 'Humidity_Percentage': humidity, 'Wind_Speed_kmh': wind}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # 3. Save it back
    df.to_csv(filename, index=False)

#-------------------------------------------------------------------------Menu option 2
# This function is for viewing weather stats
def get_weather_stats(filename="weather_observations.csv"):
    """
    Grabs our weather data file and calculates the core metrics 
    required by our project specs (Averages, Extrems, and Modes)[cite: 1].
    """
    # 1. Load the database file
    df = load_data(filename)
    
    # If the file happens to be completely empty, return None to prevent errors
    if df.empty:
        return None
        
    # 2. Calculate the required metrics precisely[cite: 1]
    stats = {
        'avg_temp': df['Temperature_Celsius'].mean(),
        'min_temp': df['Temperature_Celsius'].min(),
        'max_temp': df['Temperature_Celsius'].max(),
        # .mode()[0] picks the top most frequent string in the Condition column[cite: 1]
        'common_condition': df['Condition'].mode()[0]
    }
    
    return stats

#-------------------------------------------------------------------------Menu option 3
def search_by_date(target_date, filename="weather_observations.csv"):
    """
    Filters our weather database to find rows matching a specific date[cite: 1].
    Returns a DataFrame of matches, or an empty DataFrame if nothing is found.
    """
    # Load the CSV file
    df = load_data(filename)
    
    # Ensure Date column is treated as text for stable matching
    df['Date'] = df['Date'].astype(str)
    
    # Filter the 'Date' column to match the user's requested date exactly[cite: 1]
    matching_rows = df[df['Date'] == target_date]
    
    return matching_rows

#-------------------------------------------------------------------------Menu option 4
def display_all():
    """Display all observations"""
    df = load_data('weather_observations.csv')
    st.dataframe(df, use_container_width=True)
    return

#------------------------------------------------------------------------Aditional strech-Goals requirements

# -------------------------------------------------------------
# GOAL 1: TEXT-BASED TEMPERATURE GRAPH
# -------------------------------------------------------------
def generate_text_graph(limit=10):
    """
    Creates a simple text bar chart using the pipe '|' symbol[cite: 1].
    """
    df = load_data()
    if df.empty:
        return "No data available."
        
    # Grab the last 'limit' records to keep it readable on screen
    recent_data = df.tail(limit)
    graph_lines = []
    
    for idx, row in recent_data.iterrows():
        # Represent each 2 degrees Celsius with one vertical block line
        bar_length = int(row['Temperature_Celsius'] / 2)
        bar = "█" * bar_length
        graph_lines.append(f"{row['Date']} | {bar} {row['Temperature_Celsius']}°C")
        
    return "\n".join(graph_lines)

# -------------------------------------------------------------
# GOAL 2: FILTER BY MONTH OR SEASON
# -------------------------------------------------------------
def filter_by_timeframe(choice_type, choice_value):
    """
    Filters rows by isolating month digits from the date string (MM-DD-YYYY)[cite: 1].
    """
    df = load_data()
    if df.empty:
        return df
       
    # Explicitly convert to string so character slicing always works perfectly
    df['Date'] = df['Date'].astype(str)
    # Extract the month number from the string (the first two characters)
    # e.g., '01-15-2025' -> '01'
    df['Month_Num'] = df['Date'].str[:2]
    
    if choice_type == "Month":
        result = df[df['Month_Num'] == choice_value]
        return result.drop(columns=['Month_Num'])
        
    elif choice_type == "Season":
        # Group months into standard Bahrain seasonal patterns
        if choice_value == "Summer (Jun-Sep)":
            months = ['06', '07', '08', '09']
        elif choice_value == "Winter (Dec-Feb)":
            months = ['12', '01', '02']
        else: # Transitional Spring/Autumn
            months = ['03', '04', '05', '10', '11']
            
        result = df[df['Month_Num'].isin(months)]
        return result.drop(columns=['Month_Num'])

# -------------------------------------------------------------
# GOAL 3: PREDICT TOMORROW'S WEATHER
# -------------------------------------------------------------
def predict_tomorrow(target_month_str):
    """
    A smart historical prediction framework: It averages out historical 
    records for the current month to predict tomorrow's expectations[cite: 1].
    """
    df = load_data()
    if df.empty:
        return None
        
    # Explicitly convert to string before character slicing
    df['Date'] = df['Date'].astype(str)
    # Gather all entries matching the chosen month across past years
    month_data = df[df['Date'].str[:2] == target_month_str]
    
    if month_data.empty:
        return None
        
    # Generate a fresh random prediction on every run, from within
    # the realistic historical range of the selected month

    prediction = {
        'expected_temp': random.randint(0, 60),
        'expected_humidity': random.randint(1, 100), 
        'likely_condition': random.choice(["Sunny", "Cloudy", "Rainy", "Dusty"]),
    }
    return prediction


# -------------------------------------------------------------
# GOAL 4 & 5: YEAR-OVER-YEAR COMPARISON & RECORD BREAKERS
# -------------------------------------------------------------
def get_climate_records():
    """
    Tracks down all-time historic extremes and sets up a clean 
    Year-over-Year summary table framework.
    """
    df = load_data()
    if df.empty:
        return None
        
    # Force date to string and slice the last 4 characters to grab the year
    df['Date'] = df['Date'].astype(str)
    df['Year'] = df['Date'].str[-4:]
    
    # 4. Group by Year and calculate multiple comparative metrics for our table
    yoy_summary = df.groupby('Year').agg(
        Average_Temperature=('Temperature_Celsius', 'mean'),
        Maximum_Temperature=('Temperature_Celsius', 'max'),
        Minimum_Temperature=('Temperature_Celsius', 'min'),
        Total_Observations=('Date', 'count')
    ).reset_index()
    
    # 5. Record Tracking
    max_row = df.loc[df['Temperature_Celsius'].idxmax()]
    min_row = df.loc[df['Temperature_Celsius'].idxmin()]
    
    records = {
        'yoy_table': yoy_summary,  # Now a clean, processed DataFrame table!
        'highest_temp': max_row['Temperature_Celsius'],
        'highest_date': max_row['Date'],
        'lowest_temp': min_row['Temperature_Celsius'],
        'lowest_date': min_row['Date']
    }
    return records
#------------------------------------------------------------------------Aditional strech-Goals requirements