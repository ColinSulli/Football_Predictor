import csv
import os
path = os.getcwd()

def main():
    seasons = ['13-14', '14-15', '16-17', '17-18']
    season_file = open(path + '/processed/14-15_processed.csv')
    csv_reader = csv.reader(season_file)

    matches = {}
    row_num = 1
    magnitudes = [0.1, 0.1, 0.15, 0.20, 0.40]

    for row in csv_reader:
        p = {}
        p['home'] = 0.0
        p['draw'] = 0.0
        p['away'] = 0.0
        if row_num > 1:
            home = row[1]
            away = row[2]
            home_goals = row[3]
            away_goals = row[4]
            result = row[5]
            p['home'] = row[6]
            p['draw'] = row[7]
            p['away'] = row[8]
            matches[home] = {}
            matches[home][away] = {}
            goal_diff = [abs(home_goals - away_goals)]
            if goal_diff[0] > 4:
                goal_diff[0] = 4
            difference = (1 - p['home'])
            coefficient = magnitudes[goal_diff[0]]
            if p['home'] <= 0.2:
                if result == 'H' or result == 'D':
                    p['home'] += coefficient * difference
                    p['draw'] = p['draw'] - (0.70 * coefficient * difference)
                    p['away'] = p['away'] - (0.30 * coefficient * difference)

        row_num += 1

    print matches

main()