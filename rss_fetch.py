#!/usr/bin/python
import feedparser
import time
import mysql.connector
import random
import sys
import os

print("python x.py <dbconf> <url list file> <sleeptime between request>")
CONF_SLEEPTIME = sys.argv[3]
class bcolors:
    HEADER = ''
    OKBLUE = ''
    OKCYAN = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''

print (bcolors.OKCYAN + "Go!")
DB_HOST = "localhost" #default values
DB_USER = "user"
DB_PASSWORD = "password"
DB_DATABASE = "db"
DB_TABLE = "tb"

# EXAMPLE VALUES!
# MOST PODCASTS ARE ALSO SUPPORTED!
# HAVE FUN ;)
#urls = [
#        "https://www.spiegel.de/schlagzeilen/index.rss",
#        "https://www.spiegel.de/schlagzeilen/eilmeldungen/index.rss",
#        "https://www.bild.de/rssfeeds/vw-alles/vw-alles-26970192,dzbildplus=false,sort=1,teaserbildmobil=false,view=rss2,wtmc=ob.feed.bild.xml",
#        "https://www.faz.net/rss/aktuell/",
#        "https://news.ycombinator.com/rss",
#        "http://rss.cnn.com/rss/edition.rss",
#        "http://rss.cnn.com/rss/edition_europe.rss",
#        "http://rss.cnn.com/rss/edition_space.rss",
#        "http://rss.cnn.com/rss/edition_technology.rss",
#        "http://rss.cnn.com/rss/edition_us.rss",
#        "http://feeds.foxnews.com/foxnews/latest",
#        "http://feeds.foxnews.com/foxnews/politics",
#        "http://feeds.foxnews.com/foxnews/world",
#        "http://feeds.bbci.co.uk/news/world/europe/rss.xml",
#        "http://feeds.bbci.co.uk/news/politics/rss.xml",
#        "http://feeds.bbci.co.uk/news/technology/rss.xml",
#        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
#        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
#        "https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml",
#        "https://www.tagesschau.de/xml/rss2/",
#        "http://feeds.t-online.de/rss/nachrichten",
#        "https://www.rtl.de/feeds/alle-news",
#        "https://www.rtl.de/feeds/tv",
#        "http://rss.focus.de/fol/XML/rss_folnews.xml",
#        "https://www.heise.de/rss/heise.rdf",
#        "https://newsfeed.kicker.de/news/em",
#        "http://www.aljazeera.com/xml/rss/all.xml",
#        "https://www.buzzfeed.com/world.xml",
#        "https://www.theguardian.com/world/rss",
#        "http://feeds.washingtonpost.com/rss/world"]


urls=[]

def getDBData():
    dbfile = open(str(sys.argv[1]),"r")
    dbfile.readline() # skip fist line for comment and title
    DB_HOST = dbfile.readline()
    DB_USER = dbfile.readline()
    DB_PASSWORD = dbfile.readline()
    DB_DATABASE = dbfile.readline()
    DB_TABLE = dbfile.readline()
    dbfile.close()
    
def getURLs():
    urlfile = open(str(sys.argv[2]),"r")
    urlfile.readline()
    while ulrfile:
        line = urlfile.readline()
        if line == "":
            break
        if line.startswith("#"):
            continue
        urls.append(line)
    urlfile.close()
    


getDBData()
getURLs()
items = []

print("db connect")
mydb = mysql.connector.connect(
  host="localhost",
  user="theblog",
  password="theblogpwdsec",
  database="podmine"
)

mycursor = mydb.cursor()
def fetch():
        for url in urls:
        
                f=feedparser.parse(url)
                try:
                    print (bcolors.UNDERLINE + bcolors.OKBLUE + "#> " + f.feed.title + "")
                    pcastname= f.feed.title
                except Exception as e:
                    print(str(e))
                    pcastname="0"
                for e in f.entries:
                    title = e.title
                    try:
                        id = e.id
                    except:
                        id=e.title
                        #print("!!! ERROR ID MISSING REPLACING WITH TITLE!!!")
                    try:
                        date = e.published
                    except:
                        date="- " + str(time.ctime())
                    try:
                        desc = e.description
                    except:
                        desc="-"
                    try:
                        su = e.summary
                    except:
                        su="-"
                    try:
                        link = e.link
                    except:
                        link = "-"
                        #print(bcolors.FAIL + " LINK MISSING ")
                    try:
                        
                        con = e.content
                    except:
                        con="-"
                        
                        #print(" CONTENT MISSING ")

                    if id in items:
                        pass
                    else:
                        items.append(id)
                        print(str(pcastname +  " [" + str(date) + "]" + " #"+id+"   : " + title ) + "")
                    sql = "INSERT IGNORE INTO "+DB_TABLE+" (title, date, id, description, pcastname, raw, summary, content, link, feed_url) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s)"
                    val = (title, date,id,desc,pcastname,str(e),su,str(con),link,url)
                    mycursor.execute(sql, val)

                    mydb.commit()
while True:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n---- FETCHING ----")
        sys.stdout.flush()
        fetch()
        print("---- DONE NOW SLEEPING ----")
        sys.stdout.flush()
        time.sleep(CONF_SLEEPTIME+random.randint(4,137))
        if os.name == "nt":
            os.system('cls')
        else:
            os.system('clear')
