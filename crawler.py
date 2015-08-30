import os
import time
import shutil
import requests
from bs4 import BeautifulSoup
import savePic

seed = 'http://www.kindgirls.com'
gallery = 'http://www.kindgirls.com/photo-archive/?s='
path = './image'


def makepath():
    if not os.path.exists(path):
        os.makedirs(path)


def makeTimeDir(year, month):
    global path
    path = './image/' + str(year) + '-' + '%02d' % month
    makepath()


def skimCode(gallery):
    print 'haha'
    for i in range(24043, 24188):
        month = i % 12
        year = i / 12
        my = '%02d' % month + '-' + str(year)
        makeTimeDir(year, month)
        print path
        url = gallery + my
        print(url)
        source_code = requests.get(url)
        # just get the code, no headers or anything
        plain_text = source_code.text
        # BeautifulSoup objects can be sorted through easy
        soup = BeautifulSoup(plain_text, "html.parser")
        for room in soup.findAll('div', {'class':'gal_list'}):
            room = seed + room.contents[0]['href']
            getLarge(room)
            time.sleep(0.5)


def getLarge(page):
    print page
    source_code = requests.get(page)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for div in soup.findAll('div', {'class':'gal_list'}):
        pic = seed + div.contents[0]['href']
        print pic
        source_code = requests.get(pic)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        savePic.savePic(soup.findAll('img')[0]['src'])
        time.sleep(0.5)


skimCode(gallery)
