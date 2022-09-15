import streamlit as st
import snowflake.connector as cnx
import pandas as pd

st.title('BET ON FIFA WORLD CUP 2022!')

st.info('Bets are accepted now. Scroll down to submit your bets.')

st.header('Starting on NOVEMBER 20 2022 in QATAR!')

htp1 = "https://storage.googleapis.com/fifa2022-betting-app-images/fifa-world-cup-2022-groups.jpeg"
st.image(htp1, caption='Groups of FIFA World Cup 2022 | Source: sportco.io')

st.write('1 Submit your bets.')
st.write('2 Watch how you perform.')
st.write('3 Compete with others.')

st.text('The rules are:')
st.text('5 points for the correct World Cup Winner!')

# Give fixtures for a given round
def get_fixtures(round):
    with my_cnx.cursor() as my_cur:
        fixtures = my_cur.execute("select * from fifa_world_cup_2022 \
            where league_round = '" + round + "';").fetch_pandas_all()
        return fixtures

# Listing all fixtures of the current round depending on current date
if st.button('First Round Bets'):
    my_cnx = cnx.connect(**st.secrets["snowflake"])
    fixtures = get_fixtures('Group Stage - 1').reset_index()
    st.dataframe(fixtures)
    my_cnx.close()
    # container for round 1 games
    with st.container():
        date, home_team, colon, away_team, user_bet = st.columns(5)
        for index, row in fixtures.iterrows():
            with date:
                st.write(row['FIXTURE_DATE'][0:9])
            with home_team:
                st.markdown('<p align="center">'+row['TEAMS_HOME_NAME']+'</p>'\
                    , unsafe_allow_html=True)
            with colon:
                st.write(':')
            with away_team:
                st.write(row['TEAMS_AWAY_NAME'])
            with user_bet:
                st.write('User Bet')


st.subheader('Brought to you by Claudy Consulting.')

htp2 = "https://storage.googleapis.com/fifa2022-betting-app-images/Claudy_Logo_PRIME_neg_RGB.png"
st.image(htp2, width=100)

