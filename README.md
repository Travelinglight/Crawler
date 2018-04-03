# Crawler
Crawler is a web-crawler to scrape images of beautiful girls from webpage: http://www.kindgirls.com/
## Testing Environment
* OS: OS X 10.10.5
* Python: v2.7.10
* Packages: 
   * re 
   * os 
   * time 
   * random 
   * shutil
   * requests
   * threading
   * BeautifulSoup4
## How to Use
1. Clone this repo
2. Run crawler.py: `python crawler`
3. Input the start time and end time in to form of `<year>-<month>`. Notice that the acceptable range is from 2003-07 to the present month
4. Wait for a while and go to the "image" folder in the same directory as crawler.py

## Implementation
1. This web-crawler is only used to scrape images from **Kindgirls**, and may not work on other websites with different structure.
2. Within each gallery (`<year>/<month>/<girlname>`), crawler creates a thread for each image. Threads in queue start with a 0.5s delay after each. After a gallery is scraped, crawler suspends for a random number (1-5) of seconds to avoid being detected as a robot.
3. Occasionally, the requests from crawler would be refused by remote host for unkown reasons. In this case, the crawler would sleep for 10 minutes and restart.
