from bs4 import BeautifulSoup
from MySQLdb import connect
import time
import urllib

req = urllib.request.urlopen("http://www.lepoint.fr/24h-infos/rss.xml")
xml = BeautifulSoup(req,"xml")
db = connect(host="localhost",user="root",passwd="metromg1",db="EpicDB")
cursor = db.cursor()


def parse_links():
    for item in xml.findAll("link")[3:]:
        url = item.text
        cursor.execute("SELECT * FROM links WHERE link=('"+(url)+"')")
        rows=cursor.fetchall()
        if len(rows)==0:
            cursor.execute("INSERT INTO links (time,link) VALUES (%s,%s)", (time.time(),url))
            db.commit()
            print("Found a new link !")
        else:
            print("Link already in database !")
            
        time.sleep(10)
    
    db.close()
    
    
while True:
    parse_links()
    