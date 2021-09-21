import bs4
from bs4 import BeautifulSoup
import requests as rq
import json

backend = "https://api.crichunt.in"


def columnName(name):
    dict_ = dict(column_1="team",
                 column_2="play",
                 column_3="win",
                 column_4="loss",
                 column_5="tie",
                 column_6="nr",
                 column_7="pts",
                 column_8="nrr")
    return dict_[name.replace("-", "_")]


def points():
    r = []
    data = rq.get(
        "https://vivoiplpointstable.com/",
        headers={
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        })
    soup = bs4.BeautifulSoup(data.content, "html.parser")
    for item in soup.find_all("table", class_='tablepress-id-18'):
        tbody = item.find("tbody")
        for tr in tbody.find_all("tr"):
            teamData = dict()
            for td in tr.find_all("td"):
                teamData[columnName(td['class'][0])] = td.text
            r.append(teamData)
    rq.get(backend + "/api/table/drop")
    for obj in r:
        rq.post(backend + "/api/table/add",
                data=json.dumps(obj),
                headers={'Content-type': 'application/json'})
    return "Hey"


print(points())