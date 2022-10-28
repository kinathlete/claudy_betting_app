import streamlit as st
import snowflake.connector as cnx
import streamlit_authenticator as stauth
from datetime import datetime

st.title('MAKE YOUR PREDICTIONS FOR FIFA WORLD CUP 2022!')

st.info('Predictions are accepted now. Scroll down to submit start.')

st.header('Starting 20 NOVEMBER 2022 in QATAR!')

htp1 = "https://storage.googleapis.com/fifa2022-betting-app-images/fifa_world_cup_2022_groups.jpeg"
st.image(htp1, caption='Groups of FIFA World Cup 2022 | Source: sportco.io')

round_one_start = datetime.strptime("20/11/2022", "%d/%m/%Y")
round_two_start = datetime.strptime("25/11/2022", "%d/%m/%Y")
round_three_start = datetime.strptime("29/11/2022", "%d/%m/%Y")
round_of_sixteen = datetime.strptime("03/12/2022", "%d/%m/%Y")
quarter_finals = datetime.strptime("09/12/2022", "%d/%m/%Y")
semi_finals = datetime.strptime("13/12/2022", "%d/%m/%Y")
third_place_playoff = datetime.strptime("17/12/2022", "%d/%m/%Y")
final = datetime.strptime("18/12/2022", "%d/%m/%Y")
present = datetime.now()

# Assigning selected round globally based on date
if present.date() < round_one_start.date():
    selected_round = 'Group Stage - 1'
elif present.date() < round_two_start.date():
    selected_round = 'Group Stage - 2'
elif present.date() < round_three_start.date():
    selected_round = 'Group Stage - 3'
elif present.date() < round_of_sixteen.date():
    selected_round = 'Round of Sixteen'
elif present.date() < quarter_finals.date():
    selected_round = 'Quarter Finals'
elif present.date() < semi_finals.date():
    selected_round = 'Semi Finals'
elif present.date() < third_place_playoff.date():
    selected_round = 'Third Place Playoffs'
elif present.date() < final.date():
    selected_round = 'Final'

# Initialise Snowflake connection
def init_cnx():
    return cnx.connect(
    **st.secrets["snowflake"], client_session_keep_alive=True
    )

# Load all users
def get_users():
    with my_cnx.cursor() as my_cur:
        users = my_cur.execute(f"select * \
            from users;").fetch_pandas_all()
        return users

# Get user id
def get_user_id(username):
    with my_cnx.cursor() as my_cur:
        user_id = my_cur.execute(f"select id \
            from users \
                where username = '{username}';").fetchone()
        return user_id[0]

# Check if user has made predictions
def has_predictions(user_id):
    with my_cnx.cursor() as my_cur:
        has_predictions = my_cur.execute(f"select count(*) \
            from user_predictions_results \
                where user_id = {user_id};").fetchone()
        return has_predictions[0]

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

def get_predictions(user_id):
    with my_cnx.cursor() as my_cur:
        user_predictions = my_cur.execute(f"select FIXTURE_DATE, TEAM_GROUP, TEAMS_HOME_NAME \
            , TEAMS_AWAY_NAME, HOME_GOALS, AWAY_GOALS \
                from user_predictions_results a \
                    inner join fifa_world_cup_2022 b \
                        on b.fixture_id = a.fixture_id \
                            inner join groups c \
                                on c.team = b.teams_home_name \
                                    where user_id = {user_id} \
                                        order by a.fixture_date asc;").fetch_pandas_all()

        return user_predictions

def write_predictions(predictions, user_id):
    with my_cnx.cursor() as my_cur:
        for i in predictions[f'{username}']:
            home_preds = predictions[f'{username}'][i]['home_goals']
            away_preds = predictions[f'{username}'][i]['away_goals']
            my_cur.execute(f"insert into user_predictions_results \
                (user_id, fixture_id, home_goals, away_goals) \
                    values ({user_id}, {i}, {home_preds}, {away_preds});")

    return True

# Instantiate Snowflake connection
my_cnx = init_cnx()

# authentication
users = get_users()
names = users["EMAIL"].values.tolist()
usernames = users["USERNAME"].values.tolist()
passwords = users["PASSWORD"].values.tolist()
hashed_passwords = stauth.Hasher(passwords).generate()
credentials = {"usernames":{}}
for un, name, pw in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})
authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login','main')

if authentication_status:
    st.subheader(f"Welcome {username}!")
    user_id = get_user_id(username)
    fixtures = get_fixtures(selected_round)
    if has_predictions(user_id) <= len(fixtures.index):
        with st.form('user_predictions', clear_on_submit=True):
            # load fixtures
            predictions = {}
            prediction = {}
            for index, row in fixtures.iterrows():
                fixture_id = row['FIXTURE_ID']
                date = row['FIXTURE_DATE'][0:10]
                group = "GROUP " + row['TEAM_GROUP']
                home_team = row['TEAMS_HOME_NAME']
                away_team = row['TEAMS_AWAY_NAME']
                prediction[f'{fixture_id}'] = {}
                # user prediction
                st.write(f"{date} | {group} -- {home_team} : {away_team}")
                home, away = st.columns(2)
                with home:
                    prediction[f'{fixture_id}']['home_goals'] = st.number_input(f"{home_team}", min_value=0, max_value=13)
                with away:
                    prediction[f'{fixture_id}']['away_goals'] = st.number_input(f"{away_team}", min_value=0, max_value=13)
                predictions[f'{username}'] = prediction


            submitted = st.form_submit_button("Submit")
            
            if submitted:
                if write_predictions(predictions, user_id):
                    st.write("Thank you for submitting!")
    
    else:
        st.subheader("Your Predictions")
        for index, row in get_predictions(user_id).iterrows():
            date = row['FIXTURE_DATE'][0:10]
            group = "GROUP " + row['TEAM_GROUP']
            home_team = row['TEAMS_HOME_NAME']
            away_team = row['TEAMS_AWAY_NAME']
            home_prediction = row['HOME_GOALS']
            away_prediction = row['AWAY_GOALS']
            # user prediction
            match_details, user_prediction = st.columns(2)
            with match_details:
                st.write(f"{date} | {group} -- {home_team} : {away_team}")
            with user_prediction:
                st.write(str(home_prediction) + " : " + str(away_prediction))

    authenticator.logout("Logout","main")

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

st.subheader('Brought to you by Claudy Consulting.')

htp2 = "https://storage.googleapis.com/fifa2022-betting-app-images/Claudy_Logo_PRIME_neg_RGB.png"
st.image(htp2, width=100)