#!/usr/bin/python
# -*- coding: utf-8 -*-
''' prepares news feed for eink devies '''

import threading
import urllib
from HTMLParser import HTMLParser
from PIL import Image, ImageDraw, ImageFont
from bottle import route, run
from feedparser import parse

RSS_FEEDS = [
    'http://www.transfermarkt.de/rss/news',
    'http://www.bz-berlin.de/feed',
    'http://www.bild.de/rssfeeds/vw-news/vw-news-16726644,sort=1,view=rss2.bild.xml',
]
WIDTH = 264
HEIGHT = 167
FONTSIZE = 10
FONT = ImageFont.truetype("res/FreeMonoBold.ttf", FONTSIZE)
XOFFSET = 5
YOFFSET = 5

def addTextToImage(text):
    ''' want already correctly split text '''
    image = Image.new("1", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(image)
    height = YOFFSET
    for h in range(0, len(text)):
        draw_txt = text[h]
        (_, theight) = FONT.getsize(draw_txt)
        draw.text((XOFFSET, height), draw_txt, 255, font=FONT)
        height += theight + 2
    return image


def splitText(text):
    ''' split text to match display '''
    txt_array = text.split()
    line_txt = []
    start = 0
    for i in range(0, len(txt_array) + 1):
        (tlength, _) = FONT.getsize(' '.join(txt_array[start:i]))
        if tlength > WIDTH - XOFFSET:
            utmp = ' '.join(txt_array[start:i - 1])
            line_txt.append(utmp)
            start = i -1
        if i == len(txt_array):
            utmp = ' '.join(txt_array[start:i])
            line_txt.append(utmp)
    return line_txt


def convertHtml(text):
    ''' unescapes html codes '''
    h = HTMLParser()
    return h.unescape(text)

class NewsAggregator(threading.Thread):
    newsfeeds = []
    image = None

    def run(self):
        pass

    def updateImage(self):
        for feed in RSS_FEEDS:
            newsfeed = parse(feed)
            self.newsfeeds.append(newsfeed)

        transfermarkt = self.newsfeeds[0]['items'][0]['summary']
        bz = self.newsfeeds[1]['entries'][0]['summary']
        bild = self.newsfeeds[2]['entries'][0]['title']

        transfermarkt_txt = 'TM: ' + convertHtml(transfermarkt)
        bz_txt = 'BZ: ' + convertHtml(bz)
        bild_txt = 'BILD: ' + convertHtml(bild)

        line_txt = []
        line_txt.extend(splitText(transfermarkt_txt))
        line_txt.extend(['|'])
        line_txt.extend(splitText(bz_txt))
        line_txt.extend(['|'])
        line_txt.extend(splitText(bild_txt))


        self.image = addTextToImage(line_txt)
        #image.save("output2.xbm", "XBM")

@route('/news')
def getnews(response):
    response.set_header('Content-type', 'image/jpeg')



if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, quiet=False)

    news = NewsAggregator()
    news.start()