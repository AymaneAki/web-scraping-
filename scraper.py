from bs4 import BeautifulSoup
import requests
import csv

url = "https://www.footmercato.net/live/europe/ligue-des-champions-uefa/2025-01-22"
response = requests.get(url)

# To verify if the request is succesful 
if(response.status_code != 200):
    print("Error")
    exit()

# Analyze HTML 
soup = BeautifulSoup( response.text ,"lxml")

csv_file = "today.csv"

teams_list = soup.find_all('span', class_='matchTeam__name')
scores = soup.find_all('span', class_='matchFull__score')
league_name = soup.find('a', class_='title__leftLink')
n = len(scores)

title = league_name.text
match = []
for i in range(0, n, 2):
    team1 = teams_list[i].text
    team2 = teams_list[i+1].text
    score1 = scores[i].text
    score2 = scores[i+1].text
    score = (f"{score1}:{score2}")        
    match.append([ team1, team2, score ])

for x in match:
     print(x)

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([f"League: {title}"])
        writer.writerow(['Team 1', 'Team 2', 'Score'])
        writer.writerows(match)

