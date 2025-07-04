# import pandas as pd 
# import numpy as np 
# import pickle as pk 
# import streamlit as st

# model = pk.load(open('model.pkl','rb'))

# st.header('Car Price Prediction ML Model')

# cars_data = pd.read_csv('Cardetails.csv')

# def get_brand_name(car_name):
#     car_name = car_name.split(' ')[0]
#     return car_name.strip()
# cars_data['name'] = cars_data['name'].apply(get_brand_name)

# name = st.selectbox('Select Car Brand', cars_data['name'].unique())
# year = st.slider('Car Manufactured Year', 1994,2024)
# km_driven = st.slider('No of kms Driven', 11,200000)
# fuel = st.selectbox('Fuel type', cars_data['fuel'].unique())
# seller_type = st.selectbox('Seller  type', cars_data['seller_type'].unique())
# transmission = st.selectbox('Transmission type', cars_data['transmission'].unique())
# owner = st.selectbox('Seller  type', cars_data['owner'].unique())
# mileage = st.slider('Car Mileage', 10,40)
# engine = st.slider('Engine CC', 700,5000)
# max_power = st.slider('Max Power', 0,200)
# seats = st.slider('No of Seats', 5,10)


# if st.button("Predict"):
#     input_data_model = pd.DataFrame(
#     [[name,year,km_driven,fuel,seller_type,transmission,owner,mileage,engine,max_power,seats]],
#     columns=['name','year','km_driven','fuel','seller_type','transmission','owner','mileage','engine','max_power','seats'])
    
#     input_data_model['owner'].replace(['First Owner', 'Second Owner', 'Third Owner',
#        'Fourth & Above Owner', 'Test Drive Car'],
#                            [1,2,3,4,5], inplace=True)
#     input_data_model['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'],[1,2,3,4], inplace=True)
#     input_data_model['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'],[1,2,3], inplace=True)
#     input_data_model['transmission'].replace(['Manual', 'Automatic'],[1,2], inplace=True)
#     input_data_model['name'].replace(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
#        'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
#        'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
#        'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
#        'Ambassador', 'Ashok', 'Isuzu', 'Opel'],
#                           [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
#                           ,inplace=True)

#     car_price = model.predict(input_data_model)

#     st.markdown('Car Price is going to be '+ str(car_price[0]))

    


import pandas as pd
import numpy as np
import pickle as pk
import streamlit as st

# Load the trained model
model = pk.load(open('model.pkl','rb'))

st.header('Car Price Prediction ML Model')

# Load the car dataset
cars_data = pd.read_csv('Cardetails.csv')

# Extract brand names
def get_brand_name(car_name):
    return car_name.split(' ')[0].strip()

cars_data['name'] = cars_data['name'].apply(get_brand_name)

# Mapping dictionaries
name_mapping = {
    'Maruti': 1, 'Skoda': 2, 'Honda':3, 'Hyundai':4, 'Toyota':5, 'Ford':6, 'Renault':7,
    'Mahindra':8, 'Tata':9, 'Chevrolet':10, 'Datsun':11, 'Jeep':12, 'Mercedes-Benz':13,
    'Mitsubishi':14, 'Audi':15, 'Volkswagen':16, 'BMW':17, 'Nissan':18, 'Lexus':19,
    'Jaguar':20, 'Land':21, 'MG':22, 'Volvo':23, 'Daewoo':24, 'Kia':25, 'Fiat':26,
    'Force':27, 'Ambassador':28, 'Ashok':29, 'Isuzu':30, 'Opel':31
}

fuel_mapping = {'Diesel':1, 'Petrol':2, 'LPG':3, 'CNG':4}
seller_mapping = {'Individual':1, 'Dealer':2, 'Trustmark Dealer':3}
transmission_mapping = {'Manual':1, 'Automatic':2}
owner_mapping = {'First Owner':1, 'Second Owner':2, 'Third Owner':3, 'Fourth & Above Owner':4, 'Test Drive Car':5}

# Streamlit widgets
name = st.selectbox('Select Car Brand', sorted(cars_data['name'].unique()))
year = st.slider('Car Manufactured Year', 1994,2024,2015)
km_driven = st.slider('No of kms Driven', 11,200000,50000)
fuel = st.selectbox('Fuel type', cars_data['fuel'].unique())
seller_type = st.selectbox('Seller type', cars_data['seller_type'].unique())
transmission = st.selectbox('Transmission type', cars_data['transmission'].unique())
owner = st.selectbox('Owner type', cars_data['owner'].unique())
mileage = st.slider('Car Mileage (kmpl)', 10,40,20)
engine = st.slider('Engine CC', 700,5000,1200)
max_power = st.slider('Max Power', 0,200,80)
seats = st.slider('No of Seats', 5,10,5)

if st.button("Predict"):
    # Map categorical variables to numbers
    name_num = name_mapping.get(name, -1)  # if not found, set -1
    fuel_num = fuel_mapping.get(fuel, -1)
    seller_num = seller_mapping.get(seller_type, -1)
    transmission_num = transmission_mapping.get(transmission, -1)
    owner_num = owner_mapping.get(owner, -1)
    
    # Check for unknown categories
    if -1 in [name_num, fuel_num, seller_num, transmission_num, owner_num]:
        st.error("Invalid category selection. Please check input values.")
    else:
        # Create input DataFrame
        input_data_model = pd.DataFrame(
            [[name_num, year, km_driven, fuel_num, seller_num, transmission_num,
              owner_num, mileage, engine, max_power, seats]],
            columns=['name','year','km_driven','fuel','seller_type',
                     'transmission','owner','mileage','engine','max_power','seats']
        )

        # Predict
        car_price = model.predict(input_data_model)

        st.markdown(f"### Predicted Car Price: ₹ {car_price[0]:,.2f}")
