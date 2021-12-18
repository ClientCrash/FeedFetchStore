#!/usr/bin/python
import feedparser
import time
import mysql.connector
import random
import sys
import os

print("python x.py <dbconf> <url list file> <sleeptime between request>")
CONF_SLEEPTIME = int(sys.argv[3])
print("Go!")
urls = []
dbfile = open(str(sys.argv[1]), "r")
print(dbfile.readline())  # skip fist line for comment and title
DB_HOST = dbfile.readline()
DB_USER = dbfile.readline()
DB_PASSWORD = dbfile.readline()
DB_DATABASE = dbfile.readline()
DB_TABLE = dbfile.readline()
dbfile.close()
urlfile = open(str(sys.argv[2]), "r")
urlfile.readline()
while urlfile:
    line = urlfile.readline()
    if line == "":
        break
    if line.startswith("#"):
        continue
    urls.append(line)
urlfile.close()

v = False
if len(sys.argv) == 5:
    if sys.argv[4] == "verbose":
        v = True

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

        f = feedparser.parse(url)
        try:
            print("#> " + f.feed.title + "")
            feedname = f.feed.title
        except Exception as e:
            print(str(e))
            feedname = "0"
        for e in f.entries:
            title = e.title
            try:
                id = e.id
            except:
                id = e.title
                #print("!!! ERROR ID MISSING REPLACING WITH TITLE!!!")
            try:
                date = e.published
            except:
                date = "- " + str(time.ctime())
            try:
                desc = e.description
            except:
                desc = "-"
            try:
                su = e.summary
            except:
                su = "-"
            try:
                link = e.link
            except:
                link = "-"
                #print(bcolors.FAIL + " LINK MISSING ")
            try:

                con = e.content
            except:
                con = "-"

                #print(" CONTENT MISSING ")

            if id in items:
                pass
            else:
                items.append(id)
                print(
                    str(feedname + " [" + str(date) + "]" + " #"+id+"   : " + title) + "")
            sql = "INSERT IGNORE INTO "+DB_TABLE + \
                " (title, date, id, description, pcastname, raw, summary, content, link, feed_url) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s,%s)"
            val = (title, date, id, desc, feedname,
                   str(e), su, str(con), link, url)
            mycursor.execute(sql, val)

            mydb.commit()


while True:
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n---- FETCHING ----")
    sys.stdout.flush()
    fetch()
    print("---- DONE NOW SLEEPING ----")
    sys.stdout.flush()
    time.sleep(CONF_SLEEPTIME+random.randint(4, 137))
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
