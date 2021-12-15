import requests
import sys
import pandas as pd
from difflib import get_close_matches
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import *
from twilio.twiml.messaging_response import MessagingResponse
import gc

# A template to work only for career and season stats SMS

app = Flask("NBA_SMS")

def ColumnHeaders():
    column_headers = [
        'player_id', 'PLAYER', 'player_firstname', 'team_id', 'team_abv', 'player_age', 'GP',
        'player_gameswon', 'player_gameslost', 'unknown1', 'player_minutesplayed', 'player_FGmade', 'player_FGattemps',
        'FG_PCT', 'player_3PM', 'player_3PA', 'FG3_PCT', 'player_FTM', 'player_FTA', 'FT_PCT', 'player_OREB',
        'player_DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'unkown2', 'player_PF',
        'unkown3', 'PTS', 'player_+/-', 'player_FP', 'player_DD2', 'player_TD3', 'unknown4', 'unknown5', 'unknown6',
        'unknown7', 'unknown8', 'unknown9', 'unknown10', 'unknown11', 'unknown12', 'unknown13', 'unknown14', 'unknown15',
        'unknown16', 'unknown17', 'unknown18', 'unknown19', 'unknown20', 'unknown21', 'unknown22', 'unknown23', 'unknown24',
        'unknown25', 'unknown26', 'unknown27', 'unknown28', 'unknown29', 'unknown30', 'unknown31', 'unknown32', 'unknown33',
        'unknown34',
    ]
    return column_headers

def ColumnHeaders2():
    column_headers = [
        'player_id', 'RANK', 'PLAYER', 'TEAM', 'GP', 'MIN', 'FGM',
        'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM',
        'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK',
        'TOV', 'PTS', 'EFF', 
    ]
    return column_headers


def Headers():
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
    return headers

def DataSet(season_id):
    player_info_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season='+season_id+'&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='.format(season_id)
    headers  = Headers()
    response = requests.get(url=player_info_url, headers=headers).json()
    player_info = response['resultSets'][0]['rowSet']
    column_headers = ColumnHeaders()
    nba_df = pd.DataFrame(player_info, columns = column_headers) 
    nba_df['player_namelower'] = nba_df['PLAYER'].str.lower()
    nba_df['Year'] = season_id
    return nba_df 

def DataSet2(season_id):
    player_info_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=' + season_id +'&SeasonType=Regular+Season&StatCategory=PTS'
    headers = Headers()
    response = requests.get(url=player_info_url, headers = headers).json()
    player_info = response['resultSet']['rowSet']
    column_headers = ColumnHeaders2()
    nba_df = pd.DataFrame(player_info, columns = column_headers)
    nba_df['player_namelower'] = nba_df['PLAYER'].str.lower()
    nba_df['Year'] = season_id
    return nba_df

def Add(dataset, games, player, assists, rebounds, points, steals, blocks, turnovers, FT, Three, FG, year, playeridarr):
    gamesarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), 'GP'].values
    #print("gamesarr: " + str(gamesarr))
    games += gamesarr[0]
    gamesseason = (float)(gamesarr[0]) 
    player = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), 'PLAYER'].values
    assistsarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), 'AST'].values
    assists += ((float)(assistsarr[0]) * gamesseason)
    reboundsarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), "REB"].values
    rebounds += ((float)(reboundsarr[0]) * gamesseason)
    pointsarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), "PTS"].values
    points += ((float)(pointsarr[0]) * gamesseason)
    stealsarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), "STL"].values
    steals += ((float)(stealsarr[0]) * gamesseason)
    blocksarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), "BLK"].values
    blocks += ((float)(blocksarr[0]) * gamesseason)
    turnoversarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), "TOV"].values
    turnovers += ((float)(turnoversarr[0]) * gamesseason)
    FTarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), "FT_PCT"].values
    FT += ((float)(FTarr[0]) * gamesseason)
    Threearr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), "FG3_PCT"].values
    Three += ((float)(Threearr[0]) * gamesseason)
    FGarr = dataset.loc[(dataset["Year"] == year) & (dataset["player_id"] == playeridarr), "FG_PCT"].values
    FG += ((float)(FGarr[0]) * gamesseason)
    return games, player, assists, rebounds, points, steals, blocks, turnovers, FT, Three, FG

def Year(input_playerarr):
    if ((input_playerarr[len(input_playerarr) - 1][0:4]).isdigit()):
        return input_playerarr[len(input_playerarr) - 1][0:4]
    elif (input_playerarr[len(input_playerarr) - 2][0:4]).isdigit():
        return input_playerarr[len(input_playerarr) - 2][0:4]
    else:
        return "None"
    

@app.route("/sms", methods=["POST", "GET"])
def sms():
    input_player = request.values.get('Body', '').lower() 
    input_playerarr = input_player.split(' ')
    i = len(input_playerarr) - 1
    while (input_playerarr[i] == "" or input_playerarr[i] == ''):
        input_playerarr.pop(i)
        i = i - 1
    year = Year(input_playerarr)
    check = year.isdigit()
    if (check):
        yearstring = str(year) + "-" + str(((int)(year) + 1))[2:4] 
        input_playerarr = input_player.split(' ')
        input_playerarr.pop(len(input_playerarr) - 1)
        input_player = ' '.join(input_playerarr)
        if (1947 < (int)(year) < 1996):
            dataset = DataSet2(yearstring)
            if (len(dataset.loc[(dataset['Year'] == yearstring) & (dataset['player_namelower'] == input_player),'player_id'].values) == 0):
                dataset = pd.read_excel('Missing_Players.xlsx')
                if (len(dataset.loc[(dataset['Year'] == yearstring) & (dataset['player_namelower'] == input_player),'player_id'].values) == 0):
                    resp = MessagingResponse()
                    msg = resp.message()
                    r = "" 
                    r += "Invalid Player"
                    msg.body(r)
                    return str(resp)
        elif (1995 < (int)(year)):
            dataset = DataSet(yearstring)
            if (len(dataset.loc[(dataset['Year'] == yearstring) & (dataset['player_namelower'] == input_player),'player_id'].values) == 0):
                resp = MessagingResponse()
                msg = resp.message()
                r = "" 
                r += "Invalid player"
                msg.body(r)
                return str(resp)
        else:
            resp = MessagingResponse()
            msg = resp.message()
            r = "" 
            r += "Invalid player"
            msg.body(r)
            return str(resp)
        player = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'PLAYER'].values
        points = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'PTS'].values
        games = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'GP'].values
        assists = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'AST'].values
        rebounds = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'REB'].values
        steals = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'STL'].values
        blocks = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'BLK'].values
        turnovers = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'TOV'].values
        FT = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'FT_PCT'].values
        FG = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'FG_PCT'].values
        Three = dataset.loc[(dataset["Year"] == yearstring) & (dataset['player_namelower'] == input_player), 'FG3_PCT'].values
        resp = MessagingResponse()
        msg = resp.message()
        r = "" 
        r += "NBA Player Stats: " + "\n" + "\nYear: " + str(yearstring) + "\nName: "+ str(player[0]) + "\nPoints: " + str(float("{:.1f}".format(points[0]))) + "\nAssists: " + str(float("{:.1f}".format(assists[0]))) + "\nRebounds: " + str(float("{:.1f}".format(rebounds[0]))) + "\nSteals: " + str(float("{:.1f}".format(steals[0]))) + "\nBlocks: " + str(float("{:.1f}".format(blocks[0]))) + "\nTurnovers: " + str(float("{:.1f}".format(turnovers[0]))) + "\nField Goal %: " + str(float("{:.1f}".format(FG[0] * 100))) + "%" + "\nThree Point %: " + str(float("{:.1f}".format(Three[0] * 100))) + "%" + "\nFree Throw %: " + str(float("{:.1f}".format(FT[0] * 100))) + "%" 
        msg.body(r)
        return str(resp)
    elif (0 < len(input_playerarr) < 4):
        input_player = ' '.join(input_playerarr)
        assists = 0
        rebounds = 0
        points = 0
        steals = 0
        blocks = 0
        turnovers = 0
        FT = 0
        Three = 0
        FG = 0
        games = 0
        player = ""
        player_info_url = 'https://stats.nba.com/stats/leagueLeaders?ActiveFlag=No&LeagueID=00&PerMode=PerGame&Scope=S&Season=All+Time&SeasonType=Regular+Season&StatCategory=PTS'
        headers = Headers()
        response = requests.get(url=player_info_url, headers=headers).json()
        player_info = response['resultSet']['rowSet']
        column_headers = [
                'player_id', 'PLAYER', 'GP', 'MIN', 'FGM', 'FGA', 'FG_PCT',
                'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
                'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
                'PTS', 'AST_TOV', 'STL_TOV', 'EFG_PCT', 'TS_PCT', 'GP_RANK', 'MIN_RANK', 'FGM_RANK',
                'FGA_RANK', 'FG_PCT_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK',
                'unknown7', 'unknown8', 'unknown9', 'unknown10', 'unknown11', 'unknown12', 'unknown13', 'unknown14', 'unknown15',
                'unknown16', 'unknown17', 'unknown18',
            ]
        dataset = pd.DataFrame(player_info, columns = column_headers)
        dataset['player_namelower'] = dataset['PLAYER'].str.lower()
        playeridarr = dataset.loc[dataset['player_namelower'] == input_player, 'player_id'].values
        if (len(playeridarr) > 0):
            gamesarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), 'GP'].values
            player = dataset.loc[(dataset["player_id"] == playeridarr[0]), 'PLAYER'].values
            assistsarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), 'AST'].values
            reboundsarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), "REB"].values
            pointsarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), "PTS"].values
            stealsarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), "STL"].values
            blocksarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), "BLK"].values
            turnoversarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), "TOV"].values
            FTarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), "FT_PCT"].values
            Threearr = dataset.loc[(dataset["player_id"] == playeridarr[0]), "FG3_PCT"].values
            FGarr = dataset.loc[(dataset["player_id"] == playeridarr[0]), "FG_PCT"].values
            resp = MessagingResponse()
            msg = resp.message()
            r = "" 
            r += "NBA Player Stats: " + "\n" + "\nName: "+ str(player[0]) + "\nPoints: " + str(float("{:.1f}".format(pointsarr[0]))) + "\nAssists: " + str(float("{:.1f}".format(assistsarr[0]))) + "\nRebounds: " + str(float("{:.1f}".format(reboundsarr[0]))) + "\nSteals: " + str(float("{:.1f}".format(stealsarr[0]))) + "\nBlocks: " + str(float("{:.1f}".format(blocksarr[0]))) + "\nTurnovers: " + str(float("{:.1f}".format(turnoversarr[0]))) + "\nField Goal %: " + str(float("{:.1f}".format(FGarr[0] * 100))) + "%" + "\nThree Point %: " + str(float("{:.1f}".format(Threearr[0] * 100))) + "%" + "\nFree Throw %: " + str(float("{:.1f}".format(FTarr[0] * 100))) + "%" 
            msg.body(r)
            return str(resp)
        elif (len(DataSet('2019-20').loc[(DataSet('2019-20')["player_namelower"] == input_player), 'player_id']) > 0 or len(DataSet('2020-21').loc[(DataSet('2020-21')["player_namelower"] == input_player), 'player_id']) > 0 or len(DataSet('2021-22').loc[(DataSet('2020-21')["player_namelower"] == input_player), 'player_id']) > 0):
            dataset = pd.read_excel('NBAplayer_1996-present.xlsx')
            playeridarr = dataset.loc[dataset['player_namelower'] == input_player, 'player_id'].values
            if (len(playeridarr) > 0):
                playeryear = dataset.loc[dataset['player_id'] == playeridarr[0], 'Year'].values
                for i in playeryear:
                    games, player, assists, rebounds, points, steals, blocks, turnovers, FT, Three, FG = Add(dataset, games, player, assists, rebounds, points, steals, blocks, turnovers, FT, Three, FG, i, playeridarr[0])
            yearsarr = ['2020-21', '2021-22']
            for i in yearsarr:
                dataset = DataSet(i)
                playeridarr = dataset.loc[dataset['player_namelower'] == input_player, 'player_id'].values
                if (len(playeridarr) > 0):
                    games, player, assists, rebounds, points, (steals), (blocks), (turnovers), (FT), (Three), (FG) = Add(dataset, games, player, assists, rebounds, points, steals, blocks, turnovers, FT, Three, FG, i, playeridarr[0])
            resp = MessagingResponse()
            msg = resp.message()
            r = "" 
            r += "NBA Player Stats: " + "\n" + "\nName: "+ str(player[0]) + "\nPoints: " + str(float("{:.1f}".format(points/games))) + "\nAssists: " + str(float("{:.1f}".format(assists/games))) + "\nRebounds: " + str(float("{:.1f}".format(rebounds/games))) + "\nSteals: " + str(float("{:.1f}".format(steals/games))) + "\nBlocks: " + str(float("{:.1f}".format(blocks/games))) + "\nTurnovers: " + str(float("{:.1f}".format(turnovers/games))) + "\nField Goal %: " + str(float("{:.1f}".format((FG/games) * 100))) + "%" + "\nThree Point %: " + str(float("{:.1f}".format((Three/games) * 100))) + "%" + "\nFree Throw %: " + str(float("{:.1f}".format((FT/games) * 100))) + "%" 
            msg.body(r)
            return str(resp)
        else:
            resp = MessagingResponse()
            msg = resp.message()
            r = "" 
            r += "Invalid"
            msg.body(r)
            return str(resp)

app.run()