import urllib2
import lxml.html
import time
import datetime
import itertools
import re
import sqlite3

days = 1
base = "http://wiki.okfn.org/wiki/index.php?title=Special:RecentChanges&days=%s&from=&limit=500"%days

p = urllib2.urlopen(base).read()

r = lxml.html.fromstring(p)

dates = [i.text.strip() for i in r.xpath("//h4")]
dates = [i for i in itertools.ifilter(lambda x: x, dates)]

for d in dates:
    a = time.strptime(d,"%d %B %Y")
    d = datetime.date(a.tm_year,a.tm_mon,a.tm_mday)

uls = [i.xpath("./li") for i in r.xpath("//ul[@class='special']")]

conn = sqlite3.connect("data.sqlite")
c = conn.cursor()

for (d,i) in zip(dates,uls):
   a = time.strptime(d,"%d %B %Y")
   d = datetime.date(a.tm_year,a.tm_mon,a.tm_mday)
   for li in i: 
        links = li.xpath("./a/@href")
        href = links[-2]
        try: 
            user = re.match(".*?User:([a-zA-Z0-9-_]+).*?",links[-1]).group(1)
        
            data = {"date": d,
                    "user": user,
                     "page": href}

            c.execute("INSERT INTO data VALUES('%s','%s','%s');"% (d, user,
            href))
        except AttributeError:
            pass

conn.commit()
