import bs4
import json
import requests as rq
import time
from bs4 import BeautifulSoup

backend = "https://api.crichunt.in"

def points():
    r = []
    data = rq.get(
        "https://www.espncricinfo.com/series/ipl-2021-1249214/points-table-standings",
        headers={
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        })
    soup = bs4.BeautifulSoup(data.content, "html.parser")
    data = json.loads(soup.find("script", id="__NEXT_DATA__").text)
    data = data['props']['pageProps']['data']['pageData']['content']['standings']['groups'][0]['teamStats']
    for item in data:
        r.append({'team': item['teamInfo']['abbreviation'], 'play': item['matchesPlayed'],
                  'win': str(item['matchesWon']), 'loss': str(item['matchesLost']),
                  'tie': str(item['matchesTied']), 'nrr': str(item['nrr']),
                  'pts': str(item['points']), 'nr': '0'})
    rq.get(backend + "/api/table/drop")
    for obj in r:
        rq.post(backend + "/api/table/add",
                data=json.dumps(obj),
                headers={'Content-type': 'application/json'})
    time.sleep(3600)


while True:
    points()
    break
