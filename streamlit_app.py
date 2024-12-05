# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits your want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie will be", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:  
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    
    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients, name_on_order)
                values ('{ingredients_string}', '{name_on_order}')"""
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        # Fix the st.success syntax - it uses format method instead of comma separation
        st.success(f'Congrats {name_on_order}! Your Smoothie is ordered! ✅')

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
