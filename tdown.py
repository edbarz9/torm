import os
import sys
from urllib.request import urlopen as uOpn
from urllib.request import urlretrieve as uRtv
from bs4 import BeautifulSoup as bsoup
from urllib.request import Request

piratebay = "https://pirateproxy.bet/search/"

torrentClient = "transmission-gtk"

def soupMaker(url):
    req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    uClient = uOpn(req)
    html_page = uClient.read()
    uClient.close()
    soup = bsoup(html_page,"html.parser")
    return soup

def parseQuery():
    query = ""
    i = -1
    for i in range(len(sys.argv) - 2):
        query = query + sys.argv[i+1] + "%20"

    query = query + sys.argv[i+2]
    return query

query = parseQuery()

#print(query)
qurl = piratebay + query
#print(qurl)
#print(type(qurl))

soup = soupMaker(qurl)

torrentpage = soup.find('table',{'id':'searchResult'})
torrentlist = torrentpage.find_all('td')

for t in torrentlist:
    try:
        name = t.find('div',{'class':'detName'})
        magnet = t.find('a',{'title':'Download this torrent using magnet'})
        print(name)
        print(magnet)
    except:
        pass

#print(soup)

#os.system(torrentClient + " " + magnet)


