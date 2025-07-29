import pandas as pd 
import numpy as np 
import pickle as pk 
import streamlit as st
import io

# App Title and Description
st.title("AutoValuatorPro")
st.write("A smart car price prediction app powered by Machine Learning.")

# Load model and data
model = pk.load(open('model.pkl','rb'))
cars_data = pd.read_csv('Cardetails.csv')

# Extract brand from full car name
def get_brand_name(car_name):
    car_name = car_name.split(' ')[0]
    return car_name.strip()

cars_data['brand'] = cars_data['name'].apply(get_brand_name)

# Form UI Inputs
st.header('CarValuePro: Intelligent Price Prediction System')
brand = st.selectbox('Select Car Brand', sorted(cars_data['brand'].unique()))
year = st.slider('Car Manufactured Year', 1994, 2024, 2020)
km_driven = st.slider('No of kms Driven', 11, 200000, 30000)
fuel = st.selectbox('Fuel type', sorted(cars_data['fuel'].unique()))
seller_type = st.selectbox('Seller type', sorted(cars_data['seller_type'].unique()))
transmission = st.selectbox('Transmission type', sorted(cars_data['transmission'].unique()))
owner = st.selectbox('Owner type', sorted(cars_data['owner'].unique()))
mileage = st.slider('Car Mileage (km/l)', 10, 40, 18)
engine = st.slider('Engine Capacity (CC)', 700, 5000, 1500)
max_power = st.slider('Max Power (bhp)', 0, 200, 85)
seats = st.slider('No of Seats', 4, 10, 5)

# Optional: Show car image (example)
car_images = {
    "Honda": "images/honda.jpg",
    "Toyota": "images/toyota.jpg",
    "Ford": "images/ford.jpg"
}
if brand in car_images:
    st.image(car_images[brand], width=300, caption=f"{brand} sample image")

# Prediction Button
if st.button("Predict"):
    # Create input data
    input_data_model = pd.DataFrame(
        [[brand, year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, seats]],
        columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner',
                 'mileage', 'engine', 'max_power', 'seats']
    )

    # Encoding categorical variables
    input_data_model['owner'].replace(['First Owner', 'Second Owner', 'Third Owner',
                                       'Fourth & Above Owner', 'Test Drive Car'],
                                      [1, 2, 3, 4, 5], inplace=True)
    input_data_model['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
    input_data_model['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'],
                                            [1, 2, 3], inplace=True)
    input_data_model['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)
    input_data_model['name'].replace(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
                                      'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
                                      'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
                                      'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
                                      'Ambassador', 'Ashok', 'Isuzu', 'Opel'],
                                     list(range(1, 32)), inplace=True)

    # Predict price
    car_price = model.predict(input_data_model)

    # Display price
    st.success(f"Estimated Car Price: ₹ {int(car_price[0]):,}")

    # Show input summary
    st.subheader("Input Summary")
    st.json(input_data_model.to_dict(orient='records')[0])

    # Track history using session_state
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(int(car_price[0]))

    st.subheader("Previous Predictions")
    st.write(st.session_state.history)

    # CSV download
    buffer = io.StringIO()
    input_data_model['Predicted Price'] = int(car_price[0])
    input_data_model.to_csv(buffer, index=False)
    st.download_button("Download Prediction as CSV", buffer.getvalue(), "prediction.csv", "text/csv")

