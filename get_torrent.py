from lxml import html
import urllib2
from datetime import datetime
import os



def get_torrent(show):
    url = "https://torrentz.in/search?q="+show.replace("_", "+")
    source = urllib2.urlopen(url).read()
    tree = html.document_fromstring(source)
    
    f = open("/home/gaurav/workspace/show-scrapper/showdir/"+show+".txt", "r+")
    data = f.read()
    data = data.split("\n")[0].split(" ")
    tz_data = tree.itertext()
    for text in tz_data:
        if data[1].strip() in text:
            print "matched"
            return show + " " + data[1].strip() + " available now"
    print "not matched"
    return ""