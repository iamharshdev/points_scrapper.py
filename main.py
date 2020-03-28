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
}})

def scrap():
    r=[]
    imgsrcsdefault='https://raw.githubusercontent.com/theuitown/COROAPIWEB/master/20200328_183732_0000.png'
    # techcrunchdata
    tech='https://techcrunch.com/tag/coronavirus/'
    datatech=rq.get(tech)
    soap=bs4.BeautifulSoup(datatech.content,'html.parser')
    article=soap.find_all('div',class_='post-block')
    for p in article:
        articletitle=p.h2
        articletitle=articletitle.text
        articletitle=articletitle.strip()
        if p.img:
            articleimg=p.img
            articleimg=articleimg.get('src')
            articleimg=articleimg.replace('w=300&h=160','w=730')
        else:
            articleimg=imgsrcsdefault
        articlelink=p.a
        articlelink=articlelink.get('href')
        try:
            r.append({'title':articletitle,'link':articlelink,'img':articleimg})
        except :
            continue

    link2 = "https://www.indiatoday.in/coronavirus-covid-19-outbreak"
    data2 = rq.get(link2)
    soup2 = bs4.BeautifulSoup(data2.content, "lxml")
    divs2 = soup2.find_all("div", {"class": "catagory-listing"})
    for news in divs2:
        title=news.h2
        title=title.text
        title=title.strip()
        alink=news.a
        if news.img:
            img=news.img
            img=img.get('src')
            img=img.replace('170x96','647x363')
        else:
            img=imgsrcsdefault     
        try:
            r.append({'title':title,'link':'https://www.indiatoday.in'+alink.get('href'),
            'img':img})
        except:
            continue

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    indiacom=rq.get('https://news.abplive.com/search?s=coronavirus',headers=headers)
    indiasop=bs4.BeautifulSoup(indiacom.content,'html.parser')
    indiadiv=indiasop.find_all('a',class_='news_featured')
    for h in indiadiv:
        titleindia=h.p
        titleindia=titleindia.text
        titleindia=titleindia.strip()
        linkindia=h.get('href')
        imginida=h.img
        imginida=imginida.get('src')
        if(imginida=='https://static.abplive.com/frontend/abplive/images/default.png?impolicy=abp_cdn&imwidth=309'):
            imginida=imgsrcsdefault
            try:
                r.append({'title':titleindia,'link':linkindia,'img':imginida})
            except:
                continue
        else:
            try:
                r.append({'title':titleindia,'link':linkindia,'img':imginida})
            except:
                continue

    linkkreu = "https://www.reuters.com/search/news?blob=Coronavirus&sortBy=relevance&dateRange=pastDay"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    reuters=rq.get(linkkreu,headers=headers)
    reuterssoap=bs4.BeautifulSoup(reuters.content,'html.parser')
    reutersdiv=reuterssoap.find_all('div',class_='search-result-content')
    for f in reutersdiv:
        titlereu=f.h3
        titlereu=titlereu.text
        linkreu=f.a
        linkreu=linkreu.get('href')
        if(f.img):
            imgreu=f.img
            imgreu=imgreu.get('src')
            imgreu=imgreu.replace('w=116','w=1280')
        else:
            imgreu=imgsrcsdefault        
        try:
            r.append({'title':titlereu,'link':'https://www.reuters.com/article/idUSKBN21D2TN'+linkreu,'img':imgreu})
        except:
            continue

    # news nation    
    nnlink='https://www.newsnation.in/topic/coronavirus-news/'
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
    nn=rq.get(nnlink,headers=headers)
    nnsoap=bs4.BeautifulSoup(nn.content,'html.parser')
    nndiv=nnsoap.find_all('div',class_='col-xs-12 col-sm-6 col-md-4 col-lg-4 col-xl-4 mt-2')      
    for y in nndiv:
        nna=y.a
        nna=nna.get('href')
        nna='https://www.newsnation.in'+nna
        nnimg=y.img
        nnimg=nnimg.get('src')
        if(nnimg=='https://static.newsnation.in/nn-web/images/lazy-loading.png'):
            nnimg=imgsrcsdefault    
        else:
            nnimg=nnimg
        nnt=y.h3
        nnt=nnt.text
        try:
            r.append({'title':nnt,'link':nna,'img':nnimg})
        except:
            continue 
    
    
    anilink='https://www.aninews.in/topic/coronavirus/'
    ani=rq.get(anilink)
    soap=bs4.BeautifulSoup(ani.content,'html.parser')
    anidiv=soap.find_all('div',class_='card')
    for b in anidiv:
        if(b.img):
            aniimg=b.img
            aniimg=aniimg.get('data-src')
            aniimg=aniimg.replace('/__sized__/','/')
            aniimg=aniimg.replace('-thumbnail-320x180-70.','.')
        else:
            aniimg=imgsrcsdefault
        tit=b.h6
        try:
            tit=tit.text
        except:
            continue
        aani=b.a
        try:
            aani=aani.get('href')
            aani='https://www.aninews.in'+aani
        except:
            continue
        r.append({'title':tit,'link':aani,'img':aniimg})    

    link3 = "https://www.indiatoday.in/coronavirus-covid-19-outbreak?page=1"
    data3 = rq.get(link3)
    soup3 = bs4.BeautifulSoup(data3.content, "lxml")
    divs3 = soup3.find_all("div", {"class": "catagory-listing"})
    for news in divs3:
        title=news.h2
        title=title.text
        title=title.strip()
        alink=news.a
        if news.img:
            img=news.img
            img=img.get('src')
            img=img.replace('170x96','647x363')
        else:
            img=imgsrcsdefault     
        try:
            r.append({'title':title,'link':'https://www.indiatoday.in'+alink.get('href'),
            'img':img})
        except:
            continue
    random.shuffle(r)
    return r

def stats():
    link = "https://www.worldometers.info/coronavirus/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    data = rq.get(link, headers=headers)
    soup = bs4.BeautifulSoup(data.content, "html.parser")
    table = soup.find("table")
    d = {}
    for row in table.find_all("tr"):
        r = []
        for data in row.find_all("td"):
            r.append(data.text.strip())
        # print(r)
        try:
            d[r[0]] = {'total': r[1], 'deaths': r[3], 'cured': r[5], 'active': r[6]}
        except:
            continue
    return d['India']

class UserAPI(Resource):
    def get(self):
        r=scrap()
        return jsonify({'news':r})

class UserIndia(Resource):
    def get(self):
        d=stats()
        return jsonify({'stats':d})

api.add_resource(UserAPI, '/')
api.add_resource(UserIndia, '/stats')

if __name__=='__main__':
    app.run()
