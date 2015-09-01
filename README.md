# Crawler
Crawler is a web-crawler to scrape images of beautiful girls from webpage: http://www.kindgirls.com/
## Testing Environment
OS: OS X 10.10.5
Python: v2.7.10
Packages: re, os, time, random, shutil, requests, threading, BeautifulSoup4
## How to use
1. Close this repo
2. Run crawler.py: "python crawler"
3. Input the starting year-month and ending year-month. Notice that the earliest time is 2003-07, and the latest time is present month
4. Wait for a while and go to the "image" folder in the same directory as crawler.py

## About implementation
1. This web-crawler is only used to scrape images from Kindgirls. On other websites, which may have a different structure, this web-crawler may not work.
2. Within each gallery (year/month/girlname), crawler creates a thread for each image. Threads starts in queue with a 0.5s delay after each one. After a gallery is scraped, crawler suspends for a random number (1-5) of seconds so that it will not be detected as robot
3. Occasionally, the requests from crawler would be refused by remote host for unkown reasons. In this case, the crawler would sleep for 10 minutes and start again