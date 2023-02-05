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
year = 2022
round = 1
homeTeam = 'raiders'
awayTeam = 'sharks'
site = f'https://www.nrl.com/draw/nrl-premiership/{year}/round-{round}/{homeTeam}-v-{awayTeam}/'
driver.get(site)
time.sleep(3)

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
