import streamlit as st
import snowflake.connector as cnx
import pandas as pd

st.title('PREDICT ON FIFA WORLD CUP 2022!')

st.info('Predictions are accepted now. Scroll down to submit your predictions.')

st.header('Starting 20 NOVEMBER 2022 in QATAR!')

htp1 = "https://storage.googleapis.com/fifa2022-betting-app-images/fifa-world-cup-2022-groups.jpeg"
st.image(htp1, caption='Groups of FIFA World Cup 2022 | Source: sportco.io')

# st.write('1 Submit your bets.')
# st.write('2 Watch how you perform.')
# st.write('3 Compete with others.')

# st.text('The rules are:')
# st.text('5 points for the correct World Cup Winner!')

# Provide a username
username = st.text_input('Your Username', max_chars=20)
email = st.text_input('Your Email', max_chars=100)

# Create user in Snowflake
def create_user(username, email):
    with my_cnx.cursor() as my_cur:
        # check if user exists already, if not create user
        existing_user_id = my_cur.execute(f"select id from users \
            where email = '{email}';")
        if existing_user_id:
            user_id = existing_user_id
        else:
            my_cur.execute(f"insert into users (username, email)\
                values ('{username}','{email}');")
            user_id = my_cur.execute(f"select id from users\
                where username = '{username}'\
                    and email = '{email}';")
        return user_id

# Give fixtures for a given round
def get_fixtures(round):
    with my_cnx.cursor() as my_cur:
        fixtures = my_cur.execute(f"select * \
                from fifa_world_cup_2022 a \
                        inner join groups b \
                            on b.team = a.teams_home_name \
                                where a.league_round = '{round}' \
                                    order by a.fixture_date asc;").fetch_pandas_all()
        return fixtures

# Insert prediction
def insert_prediction(user_id, fixture_id, p_home, p_away):
    with my_cnx.cursor() as my_cur:

        new_entry = ''
        existing_prediction = my_cur.execute(f"select id from user_predictions_results\
            where user_id = {user_id} and fixture_id = {fixture_id};")
        if existing_prediction:
            my_cur.execute(f"update user_predictions_results\
                set home_goals = {p_home} and away_goals = {p_away}\
                    where user_id = {user_id} and fixture_id = {fixture_id} ;")
        else:
            my_cur.execute(f"insert into user_predictions_results \
                values ('{user_id}', '{fixture_id}', '{p_home}', '{p_away}');")
        # check if prediction exists in db now
        new_entry = my_cur.execute(f"select id from user_predictions_results\
            where user_id = {user_id} and fixture_id = {fixture_id};")
        return new_entry

# Listing all fixtures of the current round depending on current date
if st.button('Make New Predictions'):
    my_cnx = cnx.connect(**st.secrets["snowflake"])
    user_id = create_user(username, email)
    fixtures = get_fixtures('Group Stage - 1')
    # st.dataframe(fixtures)
    # container for round 1 games
    with st.container():
        predictions = []
        for index, row in fixtures.iterrows():
            fixture_id = row['FIXTURE_ID']
            date = row['FIXTURE_DATE'][0:10]
            group = "GROUP " + row['group']
            home_team = row['TEAMS_HOME_NAME']
            away_team = row['TEAMS_AWAY_NAME']
            # user prediction
            st.write(f"{date} | {group} -- {home_team} : {away_team}")
            home, away = st.columns(2)
            with home:
                home_goals = st.number_input(f"{home_team}", min_value=0, max_value=13)
            with away:
                away_goals = st.number_input(f"{away_team}", min_value=0, max_value=13)
            prediction = {'fixture_id': fixture_id, 'home': home_goals, 'away': away_goals}
            predictions.append(prediction)
        if st.button('Submit'):
            with my_cnx.cursor() as my_cur:
                for p in predictions:
                    p_home = prediction['home']
                    p_away = prediction['away']
                    p_fix_id = prediction['fixture_id']
                    p_entry = insert_prediction(user_id, fixture_id, p_home, p_away)
    
    my_cnx.close()

# Checking user bets
if st.button('Show my Predictions'):
    st.write('Your bets are going to be displayed here if there are any.')


st.subheader('Brought to you by Claudy Consulting.')

htp2 = "https://storage.googleapis.com/fifa2022-betting-app-images/Claudy_Logo_PRIME_neg_RGB.png"
st.image(htp2, width=100)

