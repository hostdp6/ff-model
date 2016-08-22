#! /usr/bin/python2.7

import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from settings import *

def authorize():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'keys.json', scope
    )
    return gspread.authorize(credentials)

def get_workbook(name):

    gc = authorize()
    return gc.open(name)

def score(player):
    score = {}
    for key in player:
        if key not in SCORING:
            continue
        for attr in player[key]:
            if attr not in SCORING[key]:
                continue
            for val in player[key][attr]:
                if val[0] not in score:
                    score[val[0]] = 0.0
                try:
                    score[val[0]] += (float(val[1]) * SCORING[key][attr])
                except ValueError:
                    score[val[0]] += (
                        float(str(val[1]).replace(',','')) * SCORING[key][attr]
                    )

    return score

def get_stats(workbook):

    players = dict()
    for key in SCORING:
        try:
            worksheet = workbook.worksheet(key)
        except:
            print "couldn't find worksheet {}".format(key)
            continue
        data = worksheet.get_all_records(empty2zero=True)
        for row in data:
            if row['PLAYER'] not in players:
                players[row['PLAYER']] = dict()
            if key not in players[row['PLAYER']]:
                players[row['PLAYER']][key] = dict()
            for attr in row:
                if attr in ('YEAR','PLAYER'):
                    continue
                if attr not in players[row['PLAYER']][key]:
                    players[row['PLAYER']][key][attr] = []
                players[row['PLAYER']][key][attr].append(
                    (row['YEAR'], row[attr])
                )

    return players

def calc_scores(players):

    for player in players:
        players[player]['SCORES'] = score(players[player])
    return players

def project_prev(player):

    if 'SCORES' not in player:
        return 0
    total_weight = sum([YEARS_WEIGHT[weight] for weight in YEARS_WEIGHT])
    total_score = 0
    for year in player['SCORES']:
        if str(year) not in YEARS_WEIGHT:
            continue
        total_score += YEARS_WEIGHT[str(year)] * player['SCORES'][year]
    return total_score/total_weight

def project_futr(player):

    try:
        return player['SCORES'][int(PROJ_YEAR)]
    except KeyError:
        return 0

def calc_projections(players):

    for player in players:
        players[player]['PROJECTION'] = dict()
        players[player]['PROJECTION']['PREV'] = project_prev(players[player])
        players[player]['PROJECTION']['FUTR'] = project_futr(players[player])
    return players

def write_projections(workbook, players):

    worksheet = workbook.worksheet(PROJECTION_SHEET)
    worksheet.resize(1,3)
    worksheet.acell('a1').value = 'PLAYER'
    worksheet.acell('ab1').value = 'PROJECTION'
    for player in players:
        print "writing projection for {} ({}, {})".format(
            player,
            players[player]['PROJECTION']['PREV'],
            players[player]['PROJECTION']['FUTR']
        )
        worksheet.append_row((
            player,
            players[player]['PROJECTION']['PREV'],
            players[player]['PROJECTION']['FUTR']
        ))

def main():

    wbk = get_workbook(STATS_BOOK)
    player_stats = calc_scores(get_stats(wbk))
    player_stats = calc_projections(player_stats)

    write_projections(wbk, player_stats)

if __name__ == "__main__":
    main()
