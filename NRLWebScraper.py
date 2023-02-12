from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv 

import headings as HEAD

PATH = 'C:\Program Files (x86)\chromedriver.exe'
ser = Service(PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

dataFile = open('gameData.csv', 'w')
writer = csv.writer(dataFile)
writer.writerow(HEAD.headings)

def timeDealer(time):
    time_split = time.split(':')
    return float(time_split[0]) + float(time_split[1])/60

def removeComma(num):
    if len(num) < 4:
        return num
    num_split = num.split(',')
    return int(num_split[0])*1000 + int(num_split[1])

def parseText(gameInfoRaw):
    scoreHeader = gameInfoRaw[2].split('\n')
    summarySection = gameInfoRaw[3].split('\n')
    #for i, val in enumerate(summarySection):
    #    print(i, val)
    #xxxxx
    statsSection = gameInfoRaw[4].split('\n')
    #for i, val in enumerate(statsSection):
    #    print(i, val)
    #xxxxxx
    gameInfo = [gameInfoRaw[0], gameInfoRaw[1], scoreHeader[2], scoreHeader[7]]
    for line, content in enumerate(scoreHeader):
        if content == 'Scored':
            gameInfo.append(scoreHeader[line+1])
    
    for line, content in enumerate(summarySection):
        if content == 'TRIES':
            gameInfo.append(summarySection[line - 1])
            gameInfo.append(summarySection[line + 1])
        if content == 'CONVERSIONS':
            gameInfo.append(summarySection[line - 1][0])
            if len(summarySection[line - 1]) > 1:
                gameInfo.append(summarySection[line - 1][2])
            gameInfo.append(summarySection[line + 1][0])
            if len(summarySection[line+1]) > 1:
                gameInfo.append(summarySection[line + 1][2])
        
        if content == "PENALTY GOALS":
            gameInfo.append(summarySection[line - 1][0])
            if len(summarySection[line - 1]) > 1:
                gameInfo.append(summarySection[line - 1][2])
            else:
                gameInfo.append(0)
            gameInfo.append(summarySection[line + 1][0])
            if len(summarySection[line + 1]) > 1:
                gameInfo.append(summarySection[line + 1][2])
        
        if content == "1 POINT FIELD GOALS":
            while len(gameInfo) < 16:
                gameInfo.append(0)
            gameInfo.append(summarySection[line - 1][0])
            if len(summarySection[line - 1]) > 1:
                gameInfo.append(summarySection[line - 1][2])
            else:
                gameInfo.append(0)
            gameInfo.append(summarySection[line + 1][0])
            if len(summarySection[line + 1]) > 1:
                gameInfo.append(summarySection[line + 1][2])
        
        if content == '2 POINT FIELD GOALS':
            while len(gameInfo) < 20:
                gameInfo.append(0)
            gameInfo.append(summarySection[line - 1][0])
            if len(summarySection[line - 1]) > 1:
                gameInfo.append(summarySection[line - 1][2])
            else:
                gameInfo.append(0)
            gameInfo.append(summarySection[line + 1][0])
            if len(summarySection[line + 1]) > 1:
                gameInfo.append(summarySection[line + 1][2])
        
        if content == 'SIN BINS':
            while len(gameInfo) < 24:
                gameInfo.append(0)
            gameInfo.append(summarySection[line - 1])
            gameInfo.append(summarySection[line + 1])
        
        if content == 'SENT OFF':
            while len(gameInfo) < 26:
                gameInfo.append(0)
            gameInfo.append(summarySection[line - 1])
            gameInfo.append(summarySection[line + 1])
        
        if content == 'HALF TIME':
            while len(gameInfo) != 28:
                gameInfo.append(0)
            gameInfo.append(summarySection[line - 1])
            gameInfo.append(summarySection[line + 1])

    for line, content in enumerate(statsSection):
        if 'Possession %' in content:
            while len(gameInfo) < 30:
                gameInfo.append(0)
            posLine = statsSection[line + 1].strip()
            for i, char in enumerate(posLine):
                if char == '%':
                    gameInfo.append(float(posLine[i-2:i]))
            continue
        if 'Time In Possession' in content:
            while len(gameInfo) < 32:
                gameInfo.append(0)
            gameInfo.append(timeDealer(statsSection[line + 1]))
            gameInfo.append(timeDealer(statsSection[line + 3]))
            continue
        if 'Completion Rate' in content:
            while len(gameInfo) < 34:
                gameInfo.append(0)
            for i, char in enumerate(content):
                if char == '%':
                    gameInfo.append(content[i-2:i])
            for i, char in enumerate(content):
                if char == '/':
                    gameInfo.append(content[i-2:i])
            continue
        if 'All Runs' in content:
            while len(gameInfo) < 38:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'All Run Metres' in content:
            while len(gameInfo) < 40:
                gameInfo.append(0)
            gameInfo.append(removeComma(statsSection[line + 1].strip()))
            gameInfo.append(removeComma(statsSection[line + 3].strip()))
            continue
        if 'Post Contact Metres' in content:
            while len(gameInfo) < 42:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Line Breaks' in content:
            while len(gameInfo) < 44:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Tackle Breaks' in content:
            while len(gameInfo) < 46:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Average Set Distance' in content:
            while len(gameInfo) < 48:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Kick Return Metres' in content:
            while len(gameInfo) < 50:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Offloads' in content:
            while len(gameInfo) < 52:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Receipts' in content:
            while len(gameInfo) < 54:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Total Passes' in content:
            while len(gameInfo) < 56:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Dummy Passes' in content:
            while len(gameInfo) < 58:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Kicks' in content:
            while len(gameInfo) < 60:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Kicking Metres' in content:
            while len(gameInfo) < 62:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Forced Drop Outs' in content:
            while len(gameInfo) < 64:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Kick Defusal' in content:
            while len(gameInfo) < 66:
                gameInfo.append(0)
            for i, char in enumerate(content):
                if char == '%':
                    gameInfo.append(content[i-2:i])
        if '40/20' in content:
            while len(gameInfo) < 68:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Bombs' in content:
            while len(gameInfo) < 70:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
        if 'Grubbers' in content:
            while len(gameInfo) < 72:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Effective Tackle' in content:
            while len(gameInfo) < 74:
                gameInfo.append(0)
            for i, char in enumerate(content):
                if char == '%':
                    if content[i-2] != 'e':
                        gameInfo.append(content[i-4:i])
        if 'Tackles Made' in content:
            while len(gameInfo) < 76:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
        if 'Missed Tackles' in content:
            while len(gameInfo) < 78:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Intercepts' in content:
            while len(gameInfo) < 80:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Ineffective Tackles' in content:
            while len(gameInfo) < 82:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Errors' in content:
            while len(gameInfo) < 84:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
        if 'Penalties Conceeded' in content:
            while len(gameInfo) < 86:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Ruck Infringements' in content: 
            while len(gameInfo) < 88:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Inside 10' in content: 
            while len(gameInfo) < 90:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'On Reports' in content:
            while len(gameInfo) < 92:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())
            continue
        if 'Interchanges' in content:
            while len(gameInfo) < 94:
                gameInfo.append(0)
            gameInfo.append(statsSection[line + 2].strip())
            gameInfo.append(statsSection[line + 4].strip())
        if 'Head Injury Assessment' in content: #HIA's
            while len(gameInfo) < 96:
                    gameInfo.append(0)
            gameInfo.append(statsSection[line + 1].strip())
            gameInfo.append(statsSection[line + 3].strip())

    while len(gameInfo) < 98:
        gameInfo.append(0)

    #for heading, val in zip(HEAD.headings, gameInfo):
    #    print(heading, val)
    #xxxxxxx
    return gameInfo


years = list(range(2013, 2023))

allRawInfo = []

for year in years:
    print(f"\nYear: {year}")
    yearRawInfo = []
    round = 1
    num_rounds = 10
    while round <= num_rounds:
        print(f"Round: {round}")
        roundRawInfo = []
        site = f'https://www.nrl.com/draw/?competition=111&round={round}&season={year}'
        driver.get(site)
         

        if round == 1:
            num_rounds = len(driver.find_elements(By.CLASS_NAME, 'filter-dropdown-item--round'))

        classesFound = driver.find_elements(By.CLASS_NAME, 'l-grid')
        matchButtonCentres = []
        for classFound in classesFound:
            if classFound.text[:5] == 'Match':
                matchButtonCentres.append(classFound)

        for i in range(len(matchButtonCentres)):
            gameInfoRaw = [year, round]

            link = driver.find_element(By.XPATH, f'//*[@id="draw-content"]/section[{i+1}]/ul/li/div/div[1]/a')
            link.click()
            time.sleep(2)
            gameInfoRaw.append(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div').text)
            gameInfoRaw.append(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]').text)
            htmlText = driver.page_source 
            soup = BeautifulSoup(htmlText, 'html.parser')
            classes = soup.find_all('div')
            for element in classes:
                if element.text[:5] == 'Stats':
                    gameInfoRaw.append(element.text)
            roundRawInfo.append(gameInfoRaw)
            gameInfoProcessed = parseText(gameInfoRaw)
            writer.writerow(gameInfoProcessed)
            
            driver.back()
            time.sleep(2)
        round += 1
        yearRawInfo.append(roundRawInfo)
    allRawInfo.append(yearRawInfo)

print("Years:", len(allRawInfo))
roundsInYear = []
for year in allRawInfo:
    roundsInYear.append(len(year))

for year, rounds in zip(years, roundsInYear):
    print(f"{year}: {rounds}")

print("Rounds:", roundsInYear)

writer.close()
xxxxxxxxxx

#statsSplit = stats.text.split('\n')
#for i, stat in enumerate(statsSplit):
#    print(i, stat)
