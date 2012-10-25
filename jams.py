from flask import Flask, Response
import json
from contextlib import closing
import urllib
import logging
import PyRSS2Gen
import datetime

# Change this URL to point to your account (replace andyhd with your username).
timj_api_url = "http://api.thisismyjam.com/1/andyhd/jams.json"
feed_title = "Andy's Jams"
feed_url = "http://www.thisismyjam.com/andyhd"
feed_description =  "RSS feed of my jams on thisismyjam.com"

logging.basicConfig()

app = Flask(__name__)

def makeItem(jam):
    return PyRSS2Gen.RSSItem(
        title = jam['artist'] + ' - ' + jam['title'],
        link = jam.get('viaUrl', jam['url']),
        description = jam['caption'],
        guid = PyRSS2Gen.Guid(jam['url']),
        pubDate = datetime.datetime.strptime(jam['creationDate'], "%a, %d %b %Y %H:%M:%S +0000"))

@app.route('/jams.rss')
def jams():
    items = []
    with closing(urllib.urlopen(timj_api_url)) as feed:
        data = json.loads(''.join(feed.readlines()))
        items = [makeItem(jam) for jam in data['jams']]
    rss = PyRSS2Gen.RSS2(
        title = feed_title,
        link = feed_link,
        description = feed_description,
        lastBuildDate = datetime.datetime.now(),
        items = items)
    return Response(rss.to_xml(), mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run()
