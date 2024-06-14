import streamlit as st
import pandas as pd
from datetime import date

# Load the dataset


@st.cache_data
def load_data():
    return pd.read_csv('data.csv')


df = load_data()

# Initialize session state
if 'food_list' not in st.session_state:
    st.session_state.food_list = []
if 'quantities' not in st.session_state:
    st.session_state.quantities = []
if 'adding_food' not in st.session_state:
    st.session_state.adding_food = False

# Function to add a new food item


def add_food():
    st.session_state.food_list.append("")
    st.session_state.quantities.append(0)
    st.session_state.adding_food = True

# Function to mark adding food as done


def done():
    st.session_state.adding_food = False


# Load or initialize the record CSV
record_file = 'record.csv'
try:
    record_df = pd.read_csv(record_file)
except FileNotFoundError:
    record_df = pd.DataFrame(
        columns=['Date', 'Calories', 'Protein', 'Fat', 'Fiber'])

# Main buttons
st.title("Food and Nutrition Tracker")

if st.button('Add Food'):
    add_food()

if st.button('Done'):
    done()

# If adding food, show input fields
if st.session_state.adding_food:
    for i in range(len(st.session_state.food_list)):
        st.session_state.food_list[i] = st.selectbox(
            f'Food {i + 1}',
            options=df['Food'].tolist(),
            key=f'food_{i}'
        )
        st.session_state.quantities[i] = st.number_input(
            f'Quantity {i + 1}',
            min_value=0,
            key=f'quantity_{i}'
        )

# If done, show the results and save to CSV
if not st.session_state.adding_food and st.session_state.food_list:
    st.write("Current Food List and Quantities:")
    total_protein = total_calories = total_fat = total_fiber = 0

    for food, quantity in zip(st.session_state.food_list, st.session_state.quantities):
        if food:
            st.write(f"{food}: {quantity}")
            food_data = df[df['Food'] == food].iloc[0]
            total_protein += food_data['Protein'] * (quantity/100)
            total_calories += food_data['Calories'] * (quantity/100)
            total_fat += food_data['Fat'] * (quantity/100)
            total_fiber += food_data['Fiber'] * (quantity/100)

    st.write("Total Nutritional Values:")
    st.write(f"Total Protein: {total_protein}g")
    st.write(f"Total Calories: {total_calories} kcal")
    st.write(f"Total Fat: {total_fat}g")
    st.write(f"Total Fiber: {total_fiber}g")

    # Get current date
    today = date.today()
    st.write(f"Date: {today}")

    # Save the results to the CSV file
    new_record = {
        'Date': today,
        'Calories': total_calories,
        'Protein': total_protein,
        'Fat': total_fat,
        'Fiber': total_fiber
    }
     record_df = pd.concat([record_df, new_record], ignore_index=True)
    record_df.to_csv(record_file, index=False)
    st.write("Record saved to CSV.")
