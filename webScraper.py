#Web scraper - gathers all data required for this shit

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

years = [2022]

print("\n\nThis is our test:\n\n")

PATH = '/Users/matthewbungate/Desktop/Projects/NRL Model/chromedriver.exe'
ser = Service(r"/Users/matthewbungate/Desktop/Projects/NRL Model/chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

def normalise_name(team_name):
    normalised_name = ''
    for char in team_name:
        if char == ' ':
            normalised_name += '-'
        else:
            normalised_name += char.tolower()
    return normalised_name


for year in years:
    with open(f"Data_{year}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        headings = ["Home Score",
            "Away Score",
            "Home Tries", 
            "Away Tries",
            "Home Conversions Frac",
            "Away Conversion Frac",
            "Home Penalty Goals",
            "Away Penalty Goals",
            "Home half time score",
            "Away half time score",
            "Home possession %", 
            "Away possession %", 
            "Home Time in possession",
            "Away Time in possession", 
            "Home Completion rate (%)",
            "Away Completion rate (%)", 
            "Home Completion rate (frac)",
            "Away completion rate (frac)",
            "Home All runs",
            "Away all runs",
            "Home all run metres",
            "Away all run metres",
            "Home post contact metres",
            "Away post contact metres",
            "Home Line breaks", 
            "Away line breaks",
            "Home tackle breaks",
            "Away tackle breaks",
            "Home avg set distance",
            "Away avg set distance",
            "Home kick return metres",
            "Away kick return metres",
            "Home avg play the ball speed",
            "Away avg play the ball speed",
            "Home offloads",
            "Away offloads", 
            "Home receipts",
            "Away receipts",
            "Home total passes",
            "Away total passes",
            "Home dummy passes", 
            "Away dummy passes",
            "Home kicks",
            "Away kicks",
            "Home kicking metres",
            "Away kicking metres",
            "Home forced drop outs",
            "Away forced drop outs",
            "Home kick defusal",
            "Away kick defusal",
            "Home bombs",
            "Away bombs",
            "Home grubbers",
            "Away grubbers",
            "Home effective tackle (%)", 
            "Away effective tackle (%)", 
            "Home tackles made",
            "Away tackles made",
            "Home missed tackles",
            "Away missed tackles",
            "Home interceptions",
            "Away interceptions",
            "Home ineffective tackles",
            "Away ineffective tackles",
            "Home errors",
            "Away errors",
            "Home penalties conceded",
            "Away penalties conceded",
            "Home ruck infringements",
            "Away ruck infringements",
            "Home inside 10 metres",
            "Away inside 10 metres",
            "Home on report", 
            "Away on report"
            "Home interchanges",
            "Away interchanges",
            "Home HIA",
            "Away HIA"]
        writer.writerow(headings)
        for round in range(25):
            print(f"Round: {round}")
            driver.get(f'https://www.nrl.com/draw/?competition=111&round=1&season={year}')
            home_team = driver.find_element(By.XPATH, '//*[@id="draw-content"]/section[1]/ul/li/div/div[1]/a/div[1]/div/div/div[2]/div[1]/div/p[2]')
            away_team = driver.find_element(By.XPATH, '//*[@id="draw-content"]/section[1]/ul/li/div/div[1]/a/div[1]/div/div/div[3]/div[1]/div/p[2]')

            #home_team = normalise_name(home_team)
            #away_team = normalise_name(away_team)
            
            print(f"Home team: {home_team.text}")
            print(f"Away team: {away_team.text}")

            #attackStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[2]').text.split('\n')
            #for i, stat in enumerate(attackStats):
            #    print(i, stat)
            #xxx
            
            for game in range(8):
                
                gameData = []
                time.sleep(5)

                link = driver.find_element(By.XPATH, '//*[@id="draw-content"]/section[1]/ul/li/div/div[1]/a')
                #link = driver.find_element(By.LINK_TEXT, 'Team Stats')
                link.click()
                print("Made it past this")

                time.sleep(5) #//*[@id="tabs-match-centre-"]/div[1]/div/div/ul/li[4]/a
                teamStatsButton = driver.find_element(By.LINK_TEXT, 'Team Stats')
                
                print("Team Stats button:")
                print(teamStatsButton.text)
                print('----------')
                #teamStatsButton.click()
                #teamStatsLink = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/div[1]/div/div/ul/li[4]/a')
                #teamStatsLink.click()
                #time.sleep(5)
                print("Did we make it past this?")
                #print(driver.print_page)
                newStat = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[1]/div/div[1]/div/div/p[2]')
                print(newStat)
                print(newStat.accessible_name)
                print(newStat.id)
                print(newStat.aria_role)
                print(newStat.text)
                xxxxx
                print("Away possession:")
                for i, stat in enumerate(newStat):
                    print(i, stat)
                print('--------')
                possComp = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[1]/div/h4').text.split('\n')
                print("possComp:")
                for i, stat in enumerate(possComp):
                    print(i, stat)
                print('-------')

                homeScore = int(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div[2]/div[2]').text.split('\n')[1])
                awayScore = int(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div/div[3]/div[2]').text.split('\n')[1])
                print(f"Score: {homeScore} : {awayScore}")
                gameData.append(homeScore)
                gameData.append(awayScore)

                homeTries = int(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]/div[1]/h3/span[2]/span').text)
                awayTries = int(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]/div[1]/h3/span[4]/span').text)
                print(f"Tries: {homeTries} : {awayTries}")
                gameData.append(homeTries)
                gameData.append(awayTries)

                homeConversionFrac = driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]/div[2]/h3/span[2]/span').text
                awayConversionFrac = driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]/div[2]/h3/span[4]/span').text
                print(f"Conversions: {homeConversionFrac} : {awayConversionFrac}")
                gameData.append(homeConversionFrac)
                gameData.append(awayConversionFrac)

                homePenaltyGoals = driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]/div[3]/h3/span[2]/span').text
                awayPenatlyGoals = driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]/div[3]/h3/span[4]/span').text
                print(f"Penalties: {homePenaltyGoals} : {awayPenatlyGoals}")
                gameData.append(homePenaltyGoals)
                gameData.append(awayPenatlyGoals)

                homeHalfTime = int(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]/div[4]/h3/span[2]/span').text)
                awayHalfTime = int(driver.find_element(By.XPATH, '//*[@id="vue-match-centre"]/div/div[1]/div/div/div[3]/div[4]/h3/span[4]/span').text)
                print(f"Half time score: {homeHalfTime} : {awayHalfTime}")
                gameData.append(homeHalfTime)
                gameData.append(awayHalfTime)

                """
                print(driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[1]/div').text)
                possessionStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[1]/div').text.split('\n')
                print(possessionStats)

                homePossessionPercent = int(possessionStats[2][:-1])
                awayPossessionPercent = int(possessionStats[4][:-1])
                homePosTimeSplit = possessionStats[7].split(':')
                homePossessionTime = float(homePosTimeSplit[0]) + float(homePosTimeSplit[1])/60
                awayPosTimeSplit = possessionStats[9].split(':')
                awayPossessionTime = float(awayPosTimeSplit[0]) + float(awayPosTimeSplit[1])/60
                homeCompletionRate = int(possessionStats[11])
                awayCompletionRate = int(possessionStats[14])
                homeCompletionFrac = possessionStats[13]
                awayCompletionFrac = possessionStats[16]
                gameData.append(homePossessionPercent)
                gameData.append(awayPossessionPercent)
                gameData.append(homePossessionTime)
                gameData.append(awayPossessionTime)
                gameData.append(homeCompletionRate)
                gameData.append(awayCompletionFrac)
                gameData.append(homeCompletionFrac)
                gameData.append(awayCompletionFrac)
                """
                #print("Home all runs", driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[2]/div/div[1]/figure/dl/div[1]/dd'))
                #print(":", driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[2]/div').text)
                #//*[@id="tabs-match-centre-3"]/section/div/div/div[2]
                #//*[@id="tabs-match-centre-3"]/section/div/div


                newSection = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[5]/div/div[1]/h3').text.split('\n')
                print("New Section")
                for i, stat in enumerate(newSection):
                    print(i, stat)
                print('--------')
                sections = driver.find_elements(By.CLASS_NAME, 'u-spacing-mb-24')
                print("Elements detected by css selector")
                for i, section in enumerate(sections):
                    print(i, section.text)
                print(len(sections))
                xxxx

                attackElement = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[2]/div/h4').text
                print(attackElement)

                allText = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]').text.split('\n')
                print(allText)
                for i, text in enumerate(allText):
                    print(i, text)


                attackStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[2]/div').text.split('\n')

                print("Attack stats:", attackStats)
                for i, stat in enumerate(attackStats):
                    print(i, stat)
                xxxx
                
                homeAllRun = int(attackStats[3])
                awayAllRun = int(attackStats[5])

                if len(attackStats[8]) > 3:
                    commaVar = attackStats[8].split(',')
                    homeAllRunMetres = int(commaVar[0])*1000 + int(commaVar[1])
                else: 
                    homeAllRunMetres = int(attackStats[8])

                if len(attackStats[10]) > 3:
                    commaVar = attackStats[10].split(',')
                    awayAllRunMetres = int(commaVar[0])*1000 + int(commaVar[1])
                else:
                    awayAllRunMetres = int(attackStats[10])
                homePostContact = int(attackStats[13])
                awayPostContact = int(attackStats[15])
                homeLineBreaks = int(attackStats[18])
                awayLineBreaks = int(attackStats[20])
                homeTackleBreaks = int(attackStats[23])
                awayTackleBreaks = int(attackStats[25])
                homeAvgSetDist = float(attackStats[28])
                awayAvgSetDist = float(attackStats[30])
                homeKickReturn = int(attackStats[33])
                awayKickReturn = int(attackStats[35])
                homePlayBall = float(attackStats[37][:-1])
                awayPlayBall = float(attackStats[38][:-1])

                gameData.append(homeAllRun)
                gameData.append(awayAllRun)
                gameData.append(homeAllRunMetres)
                gameData.append(awayAllRunMetres)
                gameData.append(homePostContact)
                gameData.append(awayPostContact)
                gameData.append(homeLineBreaks)
                gameData.append(awayLineBreaks)
                gameData.append(homeTackleBreaks)
                gameData.append(awayTackleBreaks)
                gameData.append(homeAvgSetDist)
                gameData.append(awayAvgSetDist)
                gameData.append(homeKickReturn)
                gameData.append(awayKickReturn)
                gameData.append(homePlayBall)
                gameData.append(awayPlayBall)

                passingStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[3]/div').text.split("\n")
                homeOffloads = int(passingStats[3])
                awayOfflaods = int(passingStats[5])
                homeReceipts = int(passingStats[8])
                awayReceipts = int(passingStats[10])
                homeTotalPasses = int(passingStats[13])
                awayTotalPasses = int(passingStats[15])
                homeDummyPasses = int(passingStats[18])
                awayDummyPasses = int(passingStats[20])

                gameData.append(homeOffloads)
                gameData.append(awayOfflaods)
                gameData.append(homeReceipts)
                gameData.append(awayReceipts)
                gameData.append(homeTotalPasses)
                gameData.append(awayTotalPasses)
                gameData.append(homeDummyPasses)
                gameData.append(awayDummyPasses)

                kickingStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[4]/div').text.split("\n")

                homeKicks = int(kickingStats[3])
                awayKicks = int(kickingStats[5])
                homeKickingMetres = int(kickingStats[8])
                awayKickingMetres = int(kickingStats[10])
                homeForcedDropout = int(kickingStats[13])
                awayForcedDropout = int(kickingStats[15])
                homeKickDefusal = int(kickingStats[17])
                awayKickDefusal = int(kickingStats[19])
                homeBombs = int(kickingStats[23])
                awayBombs = int(kickingStats[25])
                homeGrubbers = int(kickingStats[28])
                awayGrubbers = int(kickingStats[30])

                gameData.append(homeKicks)
                gameData.append(awayKicks)
                gameData.append(homeKickingMetres)
                gameData.append(awayKickingMetres)
                gameData.append(homeForcedDropout)
                gameData.append(awayForcedDropout)
                gameData.append(homeKickDefusal)
                gameData.append(awayKickDefusal)
                gameData.append(homeBombs)
                gameData.append(awayBombs)
                gameData.append(homeGrubbers)
                gameData.append(awayGrubbers)

                defenceStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[5]/div').text.split('\n')
                homeEffectiveTackles = float(defenceStats[2])
                awayEffectiveTackles = float(defenceStats[4])
                homeTacklesMade = int(defenceStats[8])
                awayTacklesMade = int(defenceStats[10])
                homeMissedTackles = int(defenceStats[13])
                awayMissedTackles = int(defenceStats[15])
                homeIneffectiveTackles = int(defenceStats[18])
                awayIneffectiveTackles = int(defenceStats[20])

                gameData.append(homeEffectiveTackles)
                gameData.append(awayEffectiveTackles)
                gameData.append(homeTacklesMade)
                gameData.append(awayTacklesMade)
                gameData.append(homeMissedTackles)
                gameData.append(awayMissedTackles)
                gameData.append(homeIneffectiveTackles)
                gameData.append(awayIneffectiveTackles)

                negativePlayStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[6]/div').text.split('\n')
                homeErrors = int(negativePlayStats[3])
                awayErrors = int(negativePlayStats[5])
                homePensConceeded = int(negativePlayStats[8])
                awayPensConceeded = int(negativePlayStats[10])
                homeRuckInfringements = int(negativePlayStats[13])
                awayRuckInfringements = int(negativePlayStats[15])
                if len(negativePlayStats) > 16:
                    homeInsideTen = int(negativePlayStats[18])
                    awayInsideTen = int(negativePlayStats[20])
                    if len(negativePlayStats) > 21:
                        homeOnReports = int(negativePlayStats[23])
                        awayOnReports = int(negativePlayStats[25])

                gameData.append(homeErrors)
                gameData.append(awayErrors)
                gameData.append(homePensConceeded)
                gameData.append(awayPensConceeded)
                gameData.append(homeRuckInfringements)
                gameData.append(awayRuckInfringements)
                gameData.append(homeInsideTen)
                gameData.append(awayInsideTen)
                gameData.append(homeOnReports)
                gameData.append(awayOnReports)


                interchangeStats = driver.find_element(By.XPATH, '//*[@id="tabs-match-centre-3"]/section/div/div/div[7]/div').text.split('\n')
                homeInterchanges = int(interchangeStats[3])
                awayInterchanges = int(interchangeStats[5])

                gameData.append(homeInterchanges)
                gameData.append(awayInterchanges)
            
                writer.writerow(gameData)





"""
print("Possession Stats:\n")
print(f"Possession: {homePossessionPercent}% : {awayPossessionPercent}%")
print(f"Time in possession: {homePossessionTime} : {awayPossessionTime}")
print(f"Completion Rate: {homeCompletionRate}% : {awayCompletionRate}%")
print(f"Completions: {homeCompletionFrac} : {awayCompletionFrac}")

print("Attack stats: \n")
print(f"All Run: {homeAllRun} : {awayAllRun}")
print(f"All Run Metres: {homeAllRunMetres} : {awayAllRunMetres}")
print(f"Post Contact Metres: {homePostContact} : {awayPostContact}")
print(f"Line Breaks: {homeLineBreaks} : {awayLineBreaks}")
print(f"Tackle Breaks: {homeTackleBreaks} : {awayTackleBreaks}")
print(f"Average Set distance: {homeAvgSetDist} : {awayAvgSetDist}")
print(f"Kick Return Metres: {homeKickReturn} : {awayKickReturn}")
print(f"Average Play the ball speed: {homePlayBall} : {awayPlayBall}")
print("Interchange Stats:\n")
print(f"Interchanges: {homeInterchanges} : {awayInterchanges}")

print("Negative Play Stats:\n")
print(f"Errors: {homeErrors} : {awayErrors}")
print(f"Penalties conceeded: {homePensConceeded} : {awayPensConceeded}")
print(f"Ruck Infringements: {homeRuckInfringements} : {awayRuckInfringements}")
print(f"Inside 10 metres: {homeInsideTen} : {awayInsideTen}")
print(f"On reports: {homeOnReports} : {awayOnReports}")

print("Defence Stats:\n")
print(f"Effective Tackles: {homeEffectiveTackles}% : {awayEffectiveTackles}%")
print(f"Tackles made: {homeTacklesMade} : {awayTacklesMade}")
print(f"Missed Tackles: {homeMissedTackles} : {awayMissedTackles}")
print(f"Ineffective tackles: {homeIneffectiveTackles} : {awayIneffectiveTackles}")

print("Kicking Stats")
print(f"Kicks: {homeKicks} : {awayKicks}")
print(f"Kicking meters: {homeKickingMetres} : {awayKickingMetres}")
print(f"Forced Drop outs: {homeForcedDropout} : {awayForcedDropout}")
print(f"Kick defusal (%): {homeKickDefusal} : {awayKickDefusal}")
print(f"Bombs: {homeBombs} : {awayBombs}")
print(f"Grubbers: {homeGrubbers} : {awayGrubbers}")

print("Passing Stats: \n")
print(f"Offloads: {homeOffloads} : {awayOfflaods}")
print(f"Receipts: {homeReceipts} : {awayReceipts}")
print(f"Total passes: {homeTotalPasses} : {awayTotalPasses}")
print(f"Dummy passes: {homeDummyPasses} : {awayDummyPasses}")


print("Home score:", homeScore)
print("Away score:", awayScore)
print("Home tries:", homeTries)
print("Away tires:", awayTries)
print("Home Conversions:", homeConversionFrac)
print("Away Converstions:", awayConversionFrac)
print("Home penatlies:", homePenaltyGoals)
print("Away penalties:", awayPenatlyGoals)
print("Home half time:", homeHalfTime)
print("Away half time:", awayHalfTime)
print("Home possesion (%):", homePossesion)
print("Away possesion (%):", awayPossesion)
print("Home possesion (time):", homePossesionTime)
print("Away possesion (time):", awayPossesionTime)
print("Home completion rate (%):", homeCompletionPercent)
print("Away completion rate (%):", awayCompletionPercent)
print("Home completion rate:", homeCompletionRate)
print("Away completion rate:", awayCompletionRate)
print("Home all run metres:", homeAllRun)
print("Away all run metres:", awayAllRun)
print("Home post contact metres:", homePostContact)
print("Away post contact metres:", awayPostContact)
print("Home line breaks:", homeLineBreaks)
print("Away line breaks:", awayLineBreaks)
print("Home tackle breaks:", homeTackleBreaks)
print("Away tackle breaks:", awayTackleBreaks)
print("Home average set distance:", homeAvgSetDistance)
print("Away avg set distance:", awayAvgSetDistance)
print("Home kick return:", homeKickReturn)
print("Away kick return:", awayKickReturn)
print("Home avg play the ball speed:", homePlayBall)
print("Away avg play the ball speed:", awayPlayBall)
"""

time.sleep(20)







