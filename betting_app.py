import streamlit as st

st.title('BET ON FIFA WORLD CUP 2022!')

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])

st.header('6 users have already signed-up.')

st.header('1 Submit your bets.')
st.header('2 Watch how you perform.')
st.header('3 Compete with others.')

st.header('Starting soon!')

htp7 = "https://storage.cloud.google.com/fifa2022-betting-app-images/world-cup-2022-groups.jpeg"
st.image(htp7, caption='Groups of World Cup 2022')




