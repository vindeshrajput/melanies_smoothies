# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests


st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)


# Write directly to the app
# option = st.selectbox (
# 'How would you like to be contacted?',
#     ('Email','Home Phone','Mobile Phone'))
# st.write('You selected:', option)

# option = st.selectbox (
# 'What is your favorite fruit?',
#     ('Banana','Strawberries','Peaches'))
# st.write('Your favorite fruit is:', option)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ',name_on_order)

# Get the current credentials
cnx = st.connection("snowflake")

session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients'
    , my_dataframe
    , max_selections = 5
)



if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)


    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit_Order')
    # st.write(my_insert_stmt)
    # st.stop()
    if time_to_insert:
       session.sql(my_insert_stmt).collect()
	   
       st.success('Your Smoothie is ordered, ' + name_on_order +'!', icon="✅")
     


















# Use an interactive slider to get user input
# hifives_val = st.slider(
#     "Number of high-fives in Q3",
#     min_value=0,
#     max_value=90,
#     value=60,
#     help="Use this to enter the number of high-fives you gave in Q3",
# )

# #  Create an example dataframe
# #  Note: this is just some dummy data, but you can easily connect to your Snowflake data
# #  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
# created_dataframe = session.create_dataframe(
#     [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
#     schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
# )

# # Execute the query and convert it into a Pandas dataframe
# queried_data = created_dataframe.to_pandas()

# # Create a simple bar chart
# # See docs.streamlit.io for more types of charts
# st.subheader("Number of high-fives")
# st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

# st.subheader("Underlying data")
# st.dataframe(queried_data, use_container_width=True)
