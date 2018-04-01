import csv
import os
path = os.getcwd()

def main():
    seasons = ['13-14', '14-15', '16-17', '17-18']
    matches = {}
    magnitudes = [0.1, 0.1, 0.15, 0.20, 0.40]

    output_file = open('reactions.csv', 'w')
    output_file.write('Season, Home, Away, HG, AG, Result, Before: P[Home], Before: P[Draw], Before: P[Away], Before: Sum, After: P[Home], After: P[Draw], After: P[Away], After: Sum\n')

    for season in seasons:
        season_file = open(path + '/processed/' + season + '_processed.csv')
        csv_reader = csv.reader(season_file)
        row_num = 1
        matches[season] = {}
        for row in csv_reader:
            if row_num > 1:
                p = {}
                p['home'] = 0.0
                p['draw'] = 0.0
                p['away'] = 0.0
                home = row[1]
                away = row[2]
                home_goals = int(row[3])
                away_goals = int(row[4])
                result = row[5]
                p['home'] = float(row[6])
                p['draw'] = float(row[7])
                p['away'] = float(row[8])
                matches[season][home] = {}
                goal_diff = [abs(home_goals - away_goals)]
                if goal_diff[0] > 4:
                    goal_diff[0] = 4
                output_file.write(season + ', ' + home + ', ' + away + ', ' + str(home_goals) + ', ' + str(away_goals) + ', ' + result + ', ' + str(p['home']) + ', ' + str(p['draw']) + ', ' + str(p['away']) + ', ' + str(p['home'] + p['draw'] + p['away']) + ', ')
                p = alter_probabilities(p, result, goal_diff, magnitudes)
                matches[season][home][away] = [p['home'], p['draw'], p['away']]
                output_file.write(str(p['home']) + ', ' + str(p['draw']) + ', ' + str(p['away']) + ', ' + str(p['home'] + p['draw'] + p['away']) + '\n')
            row_num += 1


def alter_probabilities(p, result, goal_diff, magnitudes):
    win_diff = 1 - p['home']
    draw_diff = 1 - p['draw']
    away_diff = 1 - p['away']
    coefficient = magnitudes[goal_diff[0]]
    if p['home'] <= 0.2:
        if result == 'H' or result == 'D':
            home_increase = coefficient * win_diff
            p['home'] += home_increase
            draw_increase = (0.7 * coefficient * draw_diff)
            p['draw'] += draw_increase
            p['away'] = p['away'] - home_increase - draw_increase
    elif p['home'] <= 0.4:
        if result == 'H':
            home_increase = coefficient * win_diff
            p['home'] += home_increase
            draw_increase = (0.7 * coefficient * draw_diff)
            p['draw'] += draw_increase
            p['away'] = p['away'] - home_increase - draw_increase
        elif result == 'A':
            away_increase = coefficient * away_diff
            p['away'] += away_increase
            p['home'] -= away_increase
    else:
        if result == 'H' and p['home'] <= 0.6:
            home_increase = coefficient * win_diff
            p['home'] += home_increase
            p['away'] -= home_increase
        elif result == 'D' or result == 'A':
            draw_increase = coefficient * draw_diff
            p['draw'] += draw_increase
            away_increase = 0.7 * coefficient * draw_diff
            p['away'] += away_increase
            p['home'] = p['home'] - draw_increase - away_increase
    return p

main()