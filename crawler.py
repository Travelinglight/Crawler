import os
import re
import time
import random
import shutil
import requests
from bs4 import BeautifulSoup

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
    global path
    for i in range(24043, 24188):
        month = (i - 1) % 12 + 1
        year = i / 12
        my = '%02d' % month + '-' + str(year)
        makeTimeDir(year, month)
        url = gallery + my
        source_code = requests.get(url)
        # just get the code, no headers or anything
        plain_text = source_code.text
        # BeautifulSoup objects can be sorted through easy
        soup = BeautifulSoup(plain_text, "html.parser")
        for room in soup.findAll('div', {'class':'gal_list'}):
            room = seed + room.contents[0]['href']
            path += '/' + re.findall('^.*/([a-zA-Z]*)/', room)[0]
            makepath()
            getLarge(room)
            path = path[0:path.rfind('/')]
            time.sleep(0.5)


def getLarge(page):
    source_code = requests.get(page)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for div in soup.findAll('div', {'class':'gal_list'}):
        pic = seed + div.contents[0]['href']
        source_code = requests.get(pic)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        savePic(soup.findAll('img')[0]['src'])
        time.sleep(random.uniform(1, 5))


def savePic(url):
    global path
    print '////////////////////////////////////'
    start_time = time.time()
    dup = path + re.findall(r'/[^/]*$', url)[0]
    pattern = '\.(jpg|JPG|jpeg|JPEG|png|PNG|tif|TIF|tiff|TIFF|bmp|BMP)'
    if re.findall(pattern, dup) == []:
        return
    elapsed_time = time.time() - start_time
    print '/ regexp: ' + str(elapsed_time)
    start_time = time.time()
    response = requests.get(url, stream=True)
    elapsed_time = time.time() - start_time
    print '/ request: ' + str(elapsed_time)
    start_time = time.time()
    with open(dup, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    elapsed_time = time.time() - start_time
    print '/ write: ' + str(elapsed_time)
    del response


skimCode(gallery)
