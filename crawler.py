import os
import re
import time
import random
import shutil
import requests
import threading
from bs4 import BeautifulSoup

seed = 'http://www.kindgirls.com'
gallery = 'http://www.kindgirls.com/photo-archive/?s='
path = './image'

# thread class
class mythread(threading.Thread):
    def __init__(self, threadID, src):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.src = src
    def run(self):
        savePic(self.src)

# make directory for categorizing pics
def makepath():
    if not os.path.exists(path):
        os.makedirs(path)

# make directory depending on year-month
def makeTimeDir(year, month):
    global path
    path = './image/' + str(year) + '/' + '%02d' % month
    makepath()

def myRequest(url, st = False):
    try:
        r = requests.get(url, stream=st)
    except:
        print 'requests.exception: ' + str(time.ctime())
        time.sleep(600)
        r = myRequest(url)
    return r

# find galleries of each Code
def skimCode(sYear, sMonth, eYear, eMonth):
    global path
    for i in range(sYear * 12 + sMonth, eYear * 12 + eMonth):  # enumerate month from 2003-07 to 2015-08
        month = (i - 1) % 12 + 1
        year = (i - 1) / 12
        my = '%02d' % month + '-' + str(year) # my = month-year
        makeTimeDir(year, month) # set up directory
        url = gallery + my # get gallery url
        source_code = myRequest(url) # request source code
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for room in soup.findAll('div', {'class':'gal_list'}):
            room = seed + room.contents[0]['href']
            path += '/' + re.findall('^.*/([a-zA-Z\- \(\)]*)/', room)[0]
            makepath() # make a directory folder for each gallery
            getLarge(room) # go to large img and download them
            path = path[0:path.rfind('/')]

def getLarge(page):
    tid = 0
    threads = []
    source_code = myRequest(page)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for div in soup.findAll('div', {'class':'gal_list'}): # going through the gallery
        tid += 1
        pic = seed + div.contents[0]['href']
        source_code = myRequest(pic) # request page that contains large picture
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        threads.append(mythread(tid, soup.findAll('img')[0]['src'])) # insert new threads into list
    for t in threads: # starts all threads
        t.start()
        time.sleep(0.5)
    for t in threads: # wait for all threads to end
        t.join()
    time.sleep(random.uniform(1, 5)) # sleep for a random period of time to avoid being recognized as machine

# download and save picture into the proper directory
def savePic(url):
    global path
    dup = path + re.findall(r'/[^/]*$', url)[0] # img full name
    pattern = '\.(jpg|JPG|jpeg|JPEG|png|PNG|tif|TIF|tiff|TIFF|bmp|BMP)'
    if re.findall(pattern, dup) == []: # make sure the src url is an image
        return
    response = myRequest(url, True) # download image
    with open(dup, 'wb') as out_file: # same image
        shutil.copyfileobj(response.raw, out_file)
    del response

# start project
def pandora():
    sYear = input("Please input the start year:\n")
    sMonth = input("Please input the start month:\n")
    eYear = input("Please input the end year:\n")
    eMonth = input("Please input the end month:\n")
    skimCode(sYear, sMonth, eYear, eMonth)

pandora()
