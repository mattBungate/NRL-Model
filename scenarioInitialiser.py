
from cmath import nan
import pandas as pd
import numpy as np
import math
import copy
import matplotlib.pyplot as plt

from sqlalchemy import true

df = pd.read_csv('nrlOddsSheet.csv')


array = df.to_numpy()

all_odds = []
total_odds = []
line_odds = []

headings = True
only_one = 0
games_with_line = 0
total_games = 0
games_with_total = 0

oddsByYear = []
yearOdds = []
oddsByRound = []
roundOdds = []
prevYear = 9
prevDay = 0
prevMonth = None

lastYearOdds = []

rightOrder = []
for i in range(len(array)):
    rightOrder.append(array[-i])

for game in rightOrder:
    if headings == True:
        headings = False
        continue

    if type(game[7]) == str:
        continue

    date = game[0].split('-')

    day = int(date[0])
    year = int(date[2])
    
    #if year == 22:
    #    print(game[0])
    
    #continue

    game_info = []
    game_info.append(game[0])
    game_info.append(game[2])
    game_info.append(game[3])
    game_info.append(float(game[5]))
    game_info.append(float(game[6]))
    game_info.append(float(game[9]))
    game_info.append(float(game[10]))
    game_info.append(float(game[11]))
    
    if year != prevYear:
        oddsByRound.append(roundOdds)
        oddsByYear.append(oddsByRound)
        roundOdds = [game_info]
        oddsByRound = [roundOdds]
        prevDay = day
        prevMonth = date[1]
        prevYear = year
        continue
    if date[1] != prevMonth:
        if day != 1 or prevDay < 30:
            oddsByRound.append(roundOdds)
            roundOdds = [game_info]
            prevDay = day
            prevMonth = date[1]
        else:
            roundOdds.append(game_info)
            prevDay = day
            prevMonth = date[1]
    else:
        if day-prevDay > 1:
            oddsByRound.append(roundOdds)
            roundOdds = [game_info]
            prevDay = day
        else:
            roundOdds.append(game_info)
            prevDay = day
  
    """
    game_info = []
    game_info.append(game[2])
    game_info.append(game[3])
    game_info.append(game[5])
    game_info.append(game[6])
    game_info.append(game[9])
    game_info.append(game[10])
    game_info.append(game[11])
    all_odds.append(game_info)
    total_games += 1

    if type(game[40]) == str:
        game_info_copy_total = copy.deepcopy(game_info)
        game_info_copy_total.append(game[40])
        game_info_copy_total.append(game[44])
        game_info_copy_total.append(game[48])
        total_odds.append(game_info_copy_total)
        games_with_total += 1


    if type(game[21]) == str:
        games_with_line += 1
        game_info_copy = copy.deepcopy(game_info_copy_total)
        game_info_copy.append(game[24])
        game_info_copy.append(game[32])
        game_info_copy.append(game[28])
        game_info_copy.append(game[36])
        line_odds.append(game_info_copy)
"""
oddsByRound.append(roundOdds)
oddsByYear.append(oddsByRound)

#print(f"Number years: {len(oddsByYear)}")
#print(f"Number Rounds in last year: {len(oddsByYear[-1])}")
#print(f"Number games in first round of last year: {len(oddsByYear[-1][0])}")


#for i, round in enumerate(oddsByYear[-1]):
#    print(f"Round {i+1}: {round}")

#print(oddsByYear[0])
profits = []
yearly_bets_placed = []
for year in oddsByYear:
    yearProfit = 0
    bets_placed = 0
    
    for round in year:
        for game in round:
            
            if game[5] > game[7]:
                if game[4] > game[3]:
                    yearProfit += game[5]
                    bets_placed += 1
                else:
                    yearProfit -= 1
                    bets_placed += 1
            else:
                if game[3] > game[4]:
                    yearProfit += game[7]
                    bets_placed += 1
                else:
                    yearProfit -= 1
                    bets_placed += 1
    profits.append(yearProfit)
    yearly_bets_placed.append(bets_placed)

bet_size = 250

total_game_profits = []
each_round_profits = []
total_round_profits = []
total_year_profits = []
total_games_not_even = []
total_worst_week = []

for year in oddsByYear:
    year_profits = 0
    games_not_even = 0
    round_total_profits = []
    round_profits_arr = []
    game_profits = []
    

    for i, round in enumerate(year):
        round_profits = 0
        for game in round:
            if math.isnan(game[5]) or math.isnan(game[7]):
                continue
            if game[5] > game[7]:
                if game[3] > game[4]:
                    year_profits += bet_size*game[5]
                    round_profits += bet_size*game[5]
                else:
                    year_profits -= bet_size
                    round_profits -= bet_size
            else:
                if game[4] > game[3]:
                    year_profits += bet_size*game[7]
                    round_profits += bet_size*game[7]
                else:
                    year_profits -= bet_size
                    round_profits -= bet_size
            game_profits.append(year_profits)
            if year_profits < 0:
                games_not_even += 1
        round_total_profits.append(year_profits)
        round_profits_arr.append(round_profits)
        #print(f"Round {i+1}: {round_profits}")

    each_round_profits.append(round_profits_arr)

    total_games_not_even.append(games_not_even)
    total_game_profits.append(game_profits)
    total_round_profits.append(round_total_profits)
    total_year_profits.append(year_profits)

for year in each_round_profits:
    total_worst_week.append(min(year))


                

fig, (ax1, ax2) = plt.subplots(1,2)
fig.suptitle("2022 NRL regular season bet on every underdog")
i = 0
for game_profit, round_profit in zip(total_game_profits, total_round_profits):
    ax1.plot(range(len(game_profit)), game_profit, label = f"{i+2009}")
    ax2.plot(range(len(round_profit)), round_profit, label = f"{i+2009}")
    i += 1
ax1.legend()
ax2.legend()

year = 2009
for not_even, profit, worstWeek in zip(total_games_not_even, total_year_profits, total_worst_week):
    #print(f"Year: {year}\nProfit: {profit}\nGames not even: {not_even}\nWorst week: {worstWeek}\n")
    year += 1

#plt.show()
