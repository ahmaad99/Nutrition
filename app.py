import streamlit as st
import pandas as pd
from datetime import datetime

# Load your nutrition dataset
# Assuming the CSV file is named 'nutrition_data.csv' and located in the same directory
df = pd.read_csv('data.csv')

# Set the 'Food' column as the index
df.set_index('Food', inplace=True)

# Initialize session state for accumulating daily nutrition totals
if 'cal' not in st.session_state:
    st.session_state.cal = 0
    st.session_state.prot = 0
    st.session_state.fat = 0
    st.session_state.fiber = 0
    st.session_state.food_count = 0

# Function to reset the daily totals


def reset_totals():
    st.session_state.cal = 0
    st.session_state.prot = 0
    st.session_state.fat = 0
    st.session_state.fiber = 0
    st.session_state.food_count = 0


# Display title and instructions
st.title('Daily Nutrition Tracker')
st.write('Enter food items and their quantities to track your daily nutrition intake.')

# Input fields for food item and quantity
food = st.text_input('Enter food item name:')
quant = st.number_input('Enter quantity in grams:', min_value=0)

# Button to add food item to the daily total
if st.button('Add Food'):
    if food in df.index and quant > 0:
        nutrition_values = df.loc[food]
        st.session_state.cal += nutrition_values['Calories (kcal)'] * (
            quant / 100)
        st.session_state.prot += nutrition_values['Protein (g)'] * (
            quant / 100)
        st.session_state.fat += nutrition_values['Fat (g)'] * (quant / 100)
        st.session_state.fiber += nutrition_values['Fiber (g)'] * (quant / 100)
        st.session_state.food_count += 1
        st.success(f"Added {quant}g of {food}")
    else:
        st.error("Please enter a valid food item and quantity.")

# Button to reset the daily totals
if st.button('Reset Totals'):
    reset_totals()
    st.success("Daily totals have been reset.")

# Display the date and daily totals
st.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
st.write(f"Total Foods Added: {st.session_state.food_count}")
st.write(f"Total Calories: {st.session_state.cal:.2f} kcal")
st.write(f"Total Protein: {st.session_state.prot:.2f} g")
st.write(f"Total Fat: {st.session_state.fat:.2f} g")
st.write(f"Total Fiber: {st.session_state.fiber:.2f} g")
