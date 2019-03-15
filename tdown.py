#!/usr/bin/python3
import os
import sys
import subprocess
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

dq = subprocess.check_output('echo "looking for torrent?" | dmenu', shell=True)
dq = str(dq).replace("b'","").replace("\\n'","")

query = dq

qurl = piratebay + query

soup = soupMaker(qurl)

torrentpage = soup.find('table',{'id':'searchResult'})
torrentlist = torrentpage.find_all('td')

resultlist={}

for t in torrentlist:
    try:
        name = t.find('div',{'class':'detName'}).text.strip()
        magnet = t.find('a',{'title':'Download this torrent using magnet'}).get('href')
        resultlist[name] = magnet
    except:
        pass

arg = ""
for k in resultlist.keys():
    arg = arg + k + "\n"

dmr = subprocess.check_output('printf "'+arg+'"|dmenu', shell=True)
dmr = str(dmr).replace("b'","").replace("\\n'","")
magnet = resultlist[dmr]

os.system(torrentClient + " " + magnet)


