import csv
import os
from aggregate import get_recent_form
matches = {}
seasons = ['13-14', '14-15', '15-16', '16-17']


def read_files():
    path = os.getcwd()
    #Reactions is a csv with intermediate output for debugging. Uncomment if you want to see it
    # output_file = open(path + '/processed/reactions.csv', 'w')
    magnitudes = [0.1, 0.1, 0.15, 0.20, 0.40]

    # output_file.write('Season, Home, Away, HG, AG, Result, Before: P[Home], Before: P[Draw], Before: P[Away], Before: Sum, After: P[Home], After: P[Draw], After: P[Away], After: Sum\n')

    for season in seasons:
        season_file = open(path + '/processed/' + season + '_processed.csv', 'r')
        csv_reader = csv.reader(season_file)
        row_num = 1
        matches[season] = {}
        for row in csv_reader:
            if row_num > 1:
                home = str(row[1].strip())
                away = str(row[2].strip())
                home_goals = int(row[3])
                away_goals = int(row[4])
                result = (row[5]).strip()

                p = {}
                p['home'] = float(row[6])
                p['draw'] = float(row[7])
                p['away'] = float(row[8])
                if home not in matches[season]:
                    matches[season][home] = {}

                goal_diff = [abs(home_goals - away_goals)]
                if goal_diff[0] > 4:
                    goal_diff[0] = 4
                # output_file.write(season + ', ' + home + ', ' + away + ', ' + str(home_goals) + ', ' + str(away_goals) + ', ' + result + ', ' + str(p['home']) + ', ' + str(p['draw']) + ', ' + str(p['away']) + ', ' + str(p['home'] + p['draw'] + p['away']) + ', ')
                alter_probabilities(p, result, goal_diff, magnitudes)
                matches[season][home][away] = [p['home'], p['draw'], p['away']]
                # output_file.write(str(p['home']) + ', ' + str(p['draw']) + ', ' + str(p['away']) + ', ' + str(p['home'] + p['draw'] + p['away']) + '\n')
            row_num += 1
    # output_file.close()
    return


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
    return

def get_prob(home, away):
    HOME = 0
    DRAW = 1
    AWAY = 2
    # CONSTANTS CAN CHANGE. DETERMINED THROUGH TESTING
    HOME_WEIGHTING = .90
    AWAY_WEIGHTING = .10
    RECENCY_WEIGHTING = .40
    weighting = [.1, .2, .3, .4]

    home_sum_probs = 0.0
    draw_sum_probs = 0.0
    away_sum_probs = 0.0
    sum_weighting = 0
    for index in range(0, len(seasons)):
        curr_season = seasons[index]
        if home in matches[curr_season] and away in matches[curr_season][home]:
            sum_weighting += weighting[index]
            home_sum_probs += (weighting[index] * (HOME_WEIGHTING * matches[curr_season][home][away][HOME] + AWAY_WEIGHTING * matches[curr_season][away][home][HOME]))
            draw_sum_probs += (weighting[index] * (HOME_WEIGHTING * matches[curr_season][home][away][DRAW] + AWAY_WEIGHTING * matches[curr_season][away][home][DRAW]))
            away_sum_probs += (weighting[index] * (HOME_WEIGHTING * matches[curr_season][home][away][AWAY] + AWAY_WEIGHTING * matches[curr_season][away][home][AWAY]))
    if sum_weighting == 0:
        return 0, 0, 0


    home_probs = float((home_sum_probs / sum_weighting))
    draw_probs = float((draw_sum_probs / sum_weighting))
    away_probs = float((away_sum_probs / sum_weighting))

    #Get data for recent form if it exists
    try: 
        home_recent, away_recent = get_recent_form(home, away)
        home_recent = float(home_recent)
        away_recent = float(away_recent)
    except Exception as e: #if 5 games haven't happened already then just return without counting for them
        return home_probs, draw_probs, away_probs

    #Change recency weighting if the team has had very poor form and does well or has very poor form and does poorly
    if (home_probs < RECENCY_WEIGHTING and home_recent <= -2) or (away_probs < RECENCY_WEIGHTING and away_recent <= -2):
        RECENCY_WEIGHTING = .1

    if (home_probs < RECENCY_WEIGHTING and home_recent >= 2) or (away_probs < RECENCY_WEIGHTING and away_recent >= 2): 
        RECENCY_WEIGHTING = .5

    #Incorporate recent form into odds
    home_probs += (home_recent / 5) * RECENCY_WEIGHTING
    away_probs += (away_recent / 5) * RECENCY_WEIGHTING


    #make sure between 1 and 0    
    home_probs = min(1, home_probs)
    away_probs = min(1, away_probs)

    home_probs = max(0, home_probs)
    home_probs = max(0, home_probs)

    sum_all = home_probs + draw_probs + away_probs

    return home_probs / sum_all, draw_probs / sum_all, away_probs / sum_all

def evaluate():
    path = os.getcwd()
    input_file = open(path + '/rawinput/17-18.csv', 'r')
    csv_reader = csv.reader(input_file)

    if os.path.exists("final") and os.path.isdir("final"):
        shutil.rmtree("final")
    os.system('mkdir ' + "final")

    output_file = open(path + '/final/output.csv', 'w')
    header = 'home, away, result, us, B365, BW, IW, LB, PS, WH, VC\n'
    output_file.write(header)

    our_score = 0.0
    B365_score = 0.0
    BW_score = 0.0
    IW_score = 0.0
    LB_score = 0.0
    PS_score = 0.0
    WH_score = 0.0
    VC_score = 0.0

    row_num = 1
    for row in csv_reader:
        if row_num > 1:
            home = str(row[2]).strip()
            away = str(row[3]).strip()
            result = (row[6]).strip()

            our_h, our_d, our_a = get_prob(home, away)
            if our_h > 0 and our_d > 0 and our_a > 0:
                our_diff = appraise(our_score, our_h, our_d, our_a, result) - our_score
                our_score = appraise(our_score, our_h, our_d, our_a, result)

                b365_base = float(row[23]) + float(row[24]) + float(row[25])
                b365_diff = appraise(B365_score, float(row[25])/b365_base, float(row[24])/b365_base, float(row[23])/b365_base, result) - B365_score
                B365_score = appraise(B365_score, float(row[25])/b365_base, float(row[24])/b365_base, float(row[23])/b365_base, result)

                bw_base = float(row[26]) + float(row[27]) + float(row[28])
                bw_diff = appraise(BW_score, float(row[28])/bw_base, float(row[27])/bw_base, float(row[26])/bw_base, result) - BW_score
                BW_score = appraise(BW_score, float(row[28])/bw_base, float(row[27])/bw_base, float(row[26])/bw_base, result)

                iw_base = float(row[29]) + float(row[30]) + float(row[31])
                iw_diff = appraise(IW_score, float(row[31])/iw_base, float(row[30])/iw_base, float(row[29])/iw_base, result) - IW_score
                IW_score = appraise(IW_score, float(row[31])/iw_base, float(row[30])/iw_base, float(row[29])/iw_base, result)

                lb_base = float(row[32]) + float(row[33]) + float(row[34])
                lb_diff = appraise(LB_score, float(row[34])/lb_base, float(row[33])/lb_base, float(row[32])/lb_base, result) - LB_score
                LB_score = appraise(LB_score, float(row[34])/lb_base, float(row[33])/lb_base, float(row[32])/lb_base, result)

                ps_base = float(row[35]) + float(row[36]) + float(row[37])
                ps_diff = appraise(PS_score, float(row[37])/ps_base, float(row[36])/ps_base, float(row[35])/ps_base, result) - PS_score
                PS_score = appraise(PS_score, float(row[37])/ps_base, float(row[36])/ps_base, float(row[35])/ps_base, result)

                wh_base = float(row[38]) + float(row[39]) + float(row[40])
                wh_diff = appraise(WH_score, float(row[40])/wh_base, float(row[39])/wh_base, float(row[38])/wh_base, result) - WH_score
                WH_score = appraise(WH_score, float(row[40])/wh_base, float(row[39])/wh_base, float(row[38])/wh_base, result)

                vc_base = float(row[41]) + float(row[42]) + float(row[43])
                vc_diff = appraise(VC_score, float(row[43])/vc_base, float(row[42])/vc_base, float(row[41])/vc_base, result) - VC_score
                VC_score = appraise(VC_score, float(row[43])/vc_base, float(row[42])/vc_base, float(row[41])/vc_base, result)

                line = home + ', ' + away + ',' + result + ', ' + str(our_diff) + ', ' + str(b365_diff) + ', ' + str(bw_diff) + ', ' + str(iw_diff) + ', ' + str(lb_diff) + ', ' + str(ps_diff) + ', ' +str(wh_diff) + ', ' +str(vc_diff) + '\n'

                output_file.write(line)
        row_num += 1
    input_file.close()
    output_file.close()
    return


def appraise(score, home, draw, away, result):
    max_prob = max(home, draw, away)

    if (max_prob == home):
        if (result == 'H'):
            score += home
        elif (result == 'D'):
            score -= (home - draw)
        else:
            score -= (home - away)

    elif (max_prob == draw):
        if (result == 'H'):
            score -= (draw - home)
        elif (result == 'D'):
            score += draw
        else:
            score -= (draw - away)

    elif (max_prob == away):
        if (result == 'H'):
            score -= (away - home)
        elif (result == 'D'):
            score -= (away - draw)
        else:
            score += away
    return score


def main():
    read_files()
    evaluate()


main()