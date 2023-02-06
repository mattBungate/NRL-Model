from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv 

PATH = 'C:\Program Files (x86)\chromedriver.exe'
ser = Service(PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

#for round in range(25):    
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
        time.sleep(3)  

        if round == 1:
            num_rounds = len(driver.find_elements(By.CLASS_NAME, 'filter-dropdown-item--round'))

        classesFound = driver.find_elements(By.CLASS_NAME, 'l-grid')
        #print(len(classesFound))
        matchButtonCentres = []
        for classFound in classesFound:
            if classFound.text[:5] == 'Match':
                matchButtonCentres.append(classFound)

        for i in range(len(matchButtonCentres)):
            gameInfoRaw = []

            link = driver.find_element(By.XPATH, f'//*[@id="draw-content"]/section[{i+1}]/ul/li/div/div[1]/a')
            link.click()
            time.sleep(3)
            gameInfoRaw.append(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]'))
            gameInfoRaw.append(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div'))
            htmlText = driver.page_source 
            soup = BeautifulSoup(htmlText, 'html.parser')
            classes = soup.find_all('div')
            for element in classes:
                if element.text[:5] == 'Stats':
                    gameInfoRaw.append(element.text)
            roundRawInfo.append(gameInfoRaw)
            driver.back()
            time.sleep(3)
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


print()
print()
for info in roundInfoRaw:
    print('--------------')
    print(info)

print('--------------')
print(len(roundInfoRaw))
xxxxxxxxxx


# Gather the text from each game into a list
roundInfoRaw = []

for button in matchButtonCentres:
    button.click()
    time.sleep(3)
    htmlText = driver.page_source
    soup = BeautifulSoup(htmlText, 'html.parser')
    classes = soup.find_all('div')
    for element in classes:
        if element.text.split('\n')[0][:5] == 'Stats':
            roundInfoRaw.append(element.text)

    driver.back()
    time.sleep(3)

for info in roundInfoRaw:
    print('--------------')
    print(info)

print('--------------')
print(len(roundInfoRaw))
xxxxxxxxxx

print(len(driver.find_elements(By.LINK_TEXT, 'Team Stats')))
scoreTab = driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div').text.split('\n')
print("Score tab:")
for i, stat in enumerate(scoreTab):
    print(i, stat)
print('------------')

allStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section').text.split('\n')
print("All stats")
for i, stat in enumerate(allStats):
    print(i, stat)
print("-----------")


possComp = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[1]/div').text.split('\n')
print("possComp:")
for i, stat in enumerate(possComp):
    print(i, stat)
print('---------------------')

htmlText = driver.page_source

soup = BeautifulSoup(htmlText, 'html.parser')
classes = soup.find_all('div')
stats = classes[1205]

for element in classes:
    if element.text.split('\n')[0][:5] == 'Stats':
        stats = element.text

print('--------------------')
print(stats)
print('--------------------')
#statsSplit = stats.text.split('\n')
#for i, stat in enumerate(statsSplit):
#    print(i, stat)
