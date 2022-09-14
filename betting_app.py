import streamlit as st
import snowflake.connector as cnx
import pandas as pd

st.title('BET ON FIFA WORLD CUP 2022!')

st.header('Bets are accepted now. Scroll down to submit your bets.')

st.text('1 Submit your bets.')
st.text('2 Watch how you perform.')
st.text('3 Compete with others.')

st.text('Starting on NOVEMBER 20 2022 in QATAR!')

htp1 = "https://storage.googleapis.com/fifa2022-betting-app-images/fifa-world-cup-2022-groups.jpeg"
st.image(htp1, caption='Groups of FIFA World Cup 2022 | Source: sportco.io')

# Give fixtures for a given round
def get_fixtures(round):
    with my_cnx.cursor() as my_cur:
        group_stage_1 = my_cur.execute("select * from fifa_world_cup_2022 \
            where league_round = '" + round + "';")
        return my_cur.fetchall(), my_cur.description

# Listing all fixtures of the current round depending on current date
if st.button('First Round Bets'):
    my_cnx = cnx.connect(**st.secrets["snowflake"])
    fixtures, columns = get_fixtures('Group Stage - 1')
    first_round_fixtures = pd.DataFrame(fixtures, columns=columns)
    st.dataframe(fixtures)
    my_cnx.close()
    # container for round 1 games
    # with st.container():
    #     date, home_team, colon, away_team, user_bet = st.columns(5, "medium")
    #     for f in fixtures:
    #         with date:
    #             st.subheader()


st.subheader('Brought to you by Claudy Consulting.')

htp2 = "https://storage.googleapis.com/fifa2022-betting-app-images/Claudy_Logo_PRIME_neg_RGB.png"
st.image(htp2, width=100)

