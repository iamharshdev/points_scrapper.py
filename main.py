from flask import Flask,jsonify
from flask_restful import Api,Resource
from flask_cors import CORS
import bs4
from bs4 import BeautifulSoup
import requests as rq
import random

app=Flask(__name__)
api=Api(app)
CORS(app)
cors=CORS(app,resources={
    r"/*":{
        "news":"*"
}
})

def scrap():
    r=[]
    # techcrunchdata
    tech='https://techcrunch.com/tag/coronavirus/'
    datatech=rq.get(tech)
    soap=bs4.BeautifulSoup(datatech.content,'html.parser')
    article=soap.find_all('div',class_='post-block')
    for p in article:
        articletitle=p.h2
        articletitle=articletitle.text
        articletitle=articletitle.strip()
        articleimg=p.img
        articleimg=articleimg.get('src')
        articleimg=articleimg.replace('w=300&h=160','w=730')
        articlelink=p.a
        articlelink=articlelink.get('href')
        r.append({'title':articletitle,'link':articlelink,'img':articleimg})

    link = "https://www.thehindu.com/topic/coronavirus/"
    data = rq.get(link)
    soup = bs4.BeautifulSoup(data.content, "lxml")
    divs = soup.find_all("div", {"class": "story-card"})
    imgs = []
    for i in divs:
        imgs.append(i.find("img", {"class": "media-object lazy adaptive placeholder"}))
        t=i.h3
        t=t.text
        t=t.strip()
        atag=i.a
        a=atag.get('href')
        for i in imgs:
            i=i["data-src-template"].replace("BINARY/thumbnail", "alternates/FREE_960")
            r.append({'title':t,'link':a,'img':i})

    link2 = "https://www.indiatoday.in/coronavirus-covid-19-outbreak"
    data2 = rq.get(link2)
    soup2 = bs4.BeautifulSoup(data2.content, "lxml")
    divs2 = soup2.find_all("div", {"class": "catagory-listing"})
    for news in divs2:
        img=news.img
        img=img.get('src')
        img=img.replace('170x96','647x363')
        title=news.h2
        title=title.text
        title=title.strip()
        alink=news.a
        r.append({'title':title,'link':'https://www.indiatoday.in'+alink.get('href'),
        'img':img})

    link3 = "https://www.indiatoday.in/coronavirus-covid-19-outbreak?page=1"
    data3 = rq.get(link3)
    soup3 = bs4.BeautifulSoup(data3.content, "lxml")
    divs3 = soup3.find_all("div", {"class": "catagory-listing"})
    for o in divs3:
        img1=o.img
        img1=img1.get('src')
        img1=img1.replace('170x96','647x363')
        title1=o.h2
        alink1=o.a
        # -647x363
        r.append({'title':title1.text,'link':'https://www.indiatoday.in'+alink1.get('href'),
        'img':img1})

    indiacom=rq.get('https://news.abplive.com/search?s=coronavirus')
    indiasop=bs4.BeautifulSoup(indiacom.content,'html.parser')
    indiadiv=indiasop.find_all('a',class_='news_featured')
    for h in indiadiv:
        titleindia=h.p
        titleindia=titleindia.text
        titleindia=titleindia.strip()
        linkindia=h.get('href')
        imginida=h.img
        imginida=imginida.get('src')
        r.append({'title':titleindia,'link':linkindia,'img':imginida})
    random.shuffle(r)
    return r

class UserAPI(Resource):
    def get(self):
        r=scrap()
        return jsonify({'news':r})

api.add_resource(UserAPI, '/')

if __name__=='__main__':
    app.run()
