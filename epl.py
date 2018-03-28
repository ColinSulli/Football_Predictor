import csv
import os
path = os.getcwd()

p_home = -1
p_draw = -1
p_away = -1

def main():
    seasons = [14, 15, 16, 17]
    season = seasons[2]
    season_file = open(path + '/Processed Data/EPL 2016-17.csv')
    csv_reader = csv.reader(season_file)

    matches = {}
    row_num = 1
    magnitudes = [0.1, 0.1, 0.15, 0.20, 0.40]

    for row in csv_reader:
        if row_num > 1:
            home = row[1]
            away = row[2]
            home_goals = row[3]
            away_goals = row[4]
            result = row[5]
            p_home = row[6]
            p_draw = row[7]
            p_away = row[8]
            goal_diff = [abs(home_goals - away_goals)]
            if goal_diff[0] > 4:
                goal_diff[0] = 4
            matches[home] = {}
            matches[home][away] = {}
            if p_home <= 0.2:
                if result == 'H':
                    difference = (1 - p_home)
                    coefficient = magnitudes[goal_diff[0]]
                    p_home += coefficient * difference
                    p_draw = p_draw - (0.70 * coefficient * difference)
                    p_away = p_away - (0.30 * coefficient * difference)
                elif result == 'D':

                elif result == 'A':

        row_num += 1


main()