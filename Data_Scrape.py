import requests
import pandas as pd
from difflib import get_close_matches
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import *
from twilio.twiml.messaging_response import MessagingResponse

## SMS for only the 2020-21 season

season_id = '2020-21'
per_mode = 'Totals'
app = Flask("NBA_Datascrape")

player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season_id+'&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='.format(season_id)

headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

response = requests.get(url=player_info_url, headers=headers).json()
player_info = response['resultSets'][0]['rowSet']

column_headers = [
    'player_id', 'player_name', 'player_firstname', 'team_id', 'team_abv', 'player_age', 'player_gamesplayed',
    'player_gameswon', 'player_gameslost', 'unknown1', 'player_minutesplayed', 'player_FGmade', 'player_FGattemps',
    'player_FG%', 'player_3PM', 'player_3PA', 'player_3P%', 'player_FTM', 'player_FTA', 'player_FT%', 'player_OREB',
    'player_DREB', 'player_REB', 'player_Assists', 'player_TOV', 'player_STL', 'player_BLK', 'unkown2', 'player_PF',
    'unkown3', 'player_PPG', 'player_+/-', 'player_FP', 'player_DD2', 'player_TD3', 'unknown4', 'unknown5', 'unknown6',
    'unknown7', 'unknown8', 'unknown9', 'unknown10', 'unknown11', 'unknown12', 'unknown13', 'unknown14', 'unknown15',
    'unknown16', 'unknown17', 'unknown18', 'unknown19', 'unknown20', 'unknown21', 'unknown22', 'unknown23', 'unknown24',
    'unknown25', 'unknown26', 'unknown27', 'unknown28', 'unknown29', 'unknown30', 'unknown31', 'unknown32', 'unknown33',
    'unknown34',
]
def NotValidPlayer():
    print("")
    print("Player not valid")

def terminate():
    print("terminate")

@app.route("/sms", methods=["POST", "GET"])
def sms():
    nba_df = pd.DataFrame(player_info, columns = column_headers) # nba dataframe
    nba_df['player_namelower'] = nba_df['player_name'].str.lower() # lowercase column
    dataset = nba_df 
    index = dataset.index # Range of indexes
    input_player = request.values.get('Body', '').lower() 
    resp = MessagingResponse()
    msg = resp.message()
    r = "" 
    closest_playerslist = get_close_matches(input_player, nba_df['player_namelower'].values) # Find closest match
    if len(closest_playerslist) == 0: # User enters player that is not recognized, nor there is a close approximation of
            # NotValidPlayer()
            # email = "nbaplayersms@gmail.com"
            # pas = "Seattle17!"
            # sms_gateway = '4256150363@tmomail.net'

            # smtp = "smtp.gmail.com" 
            # port = 587
            # This will start our email server
            # server = smtplib.SMTP(smtp,port)
            # Starting the server
            # server.starttls()
            # Now we need to login
            # server.login(email,pas)

            # msg = MIMEMultipart()
            # msg['From'] = email
            # sg['To'] = sms_gateway
            # Make sure you add a new line in the subject
            # msg['Subject'] = "NBA Stats per game\n"
            # body = "\nPlayer Not Validid"
            # print("body: " + body)
            # msg.attach(MIMEText(str(body), 'plain'))

            # sms = msg.as_string()

            # server.sendmail(email,sms_gateway,sms)
        r += "Invalid Player"
        msg.body(r)
        return str(resp)
    input_player = closest_playerslist[0]
    condition = dataset["player_namelower"] == input_player
    point = index[condition]
    player = dataset["player_name"][point[0]]
        #age = dataset["player_age"][point[0]]
    assists = dataset["player_Assists"][point[0]]
    rebounds = dataset["player_REB"][point[0]]
    points = dataset["player_PPG"][point[0]]
    steals = dataset["player_STL"][point[0]]
    blocks = dataset["player_BLK"][point[0]]
    turnovers = dataset["player_TOV"][point[0]]
    FT = dataset["player_FT%"][point[0]]
    Three = dataset["player_3P%"][point[0]]
    FG = dataset["player_FG%"][point[0]]
        # print(" ")
        # print("player name: " + str(player))
        # print("age: " + str(age))
        # print("points: " + str(points))
        # print("assists: " + str(assists))
        # print("rebounds: " + str(rebounds))
        # print("steals: " + str(steals))
        # print("blocks: " + str(blocks))
        # print("turnovers: " + str(turnovers))
        # print("field goal %: " + str(float("{:.1f}".format(FG * 100))) + "%")
        # print("three point %: " + str(float("{:.1f}".format(Three * 100))) + "%")
        # print("free throw %: " + str(float("{:.1f}".format(FT * 100))) + "%")

        # email = "nbaplayersms@gmail.com"
        # pas = "Seattle17!"
        # sms_gateway = '4256150363@tmomail.net'

        # smtp = "smtp.gmail.com" 
        # port = 587
        # This will start our email server
        # server = smtplib.SMTP(smtp,port)
        # Starting the server
        # server.starttls()
        # Now we need to login
        # server.login(email,pas)

        # msg = MIMEMultipart()
        # msg['From'] = email
        # msg['To'] = sms_gateway
        # Make sure you add a new line in the subject
        # msg['Subject'] = "NBA Stats per Game\n"

    r += "NBA Player Stats: " + "\n" + "\nName: "+ str(player) + "\nPoints: " + str(points) + "\nAssists: " + str(assists) + "\nRebounds: " + str(rebounds) + "\nSteals: " + str(steals) + "\nBlocks: " + str(blocks) + "\nTurnovers: " + str(turnovers) + "\nField Goal %: " + str(float("{:.1f}".format(FG * 100))) + "%" + "\nThree Point %: " + str(float("{:.1f}".format(Three * 100))) + "%" + "\nFree Throw %: " + str(float("{:.1f}".format(FT * 100))) + "%" 
    #print(r)
    msg.body(r)

    return str(resp)
        # msg.attach(MIMEText(str(body), 'plain'))

        # sms = msg.as_string()

        # server.sendmail(email,sms_gateway,sms)  

app.run()
# Handle abbreviations, nicknames
# Prompt for career stats, user just enters player
# Prompt for season stats, user enters player and year
# Upgrade twilio, remove header "Sent from your Twilio trial account"
# Figure out how to make this work for other phone numbers (Hopefully upgrading Twilio will work)
# Put application on another server for production deployment

