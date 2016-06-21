#!/usr/bin/python
# -*- coding: utf-8 -*-
''' prepares news feed for eink devies '''

import threading
import urllib
from HTMLParser import HTMLParser
from PIL import Image, ImageDraw, ImageFont
from bottle import route, run, static_file
from feedparser import parse

RSS_FEEDS = [
    'http://www.transfermarkt.de/rss/news',
    'http://www.bz-berlin.de/feed',
    'http://www.bild.de/rssfeeds/vw-news/vw-news-16726644,sort=1,view=rss2.bild.xml',
]
WIDTH = 200
HEIGHT = 96
FONTSIZE =12
FONT = ImageFont.truetype("res/FreeMonoBold.ttf", FONTSIZE)
XOFFSET = 2
YOFFSET = 2

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

class NewsAggregator(object):
    newsfeeds = []
    image = None


    def __init__(self):
        pass

    def updateImage(self):
        for feed in RSS_FEEDS:
            newsfeed = parse(feed)
            self.newsfeeds.append(newsfeed)

        transfermarkt = self.newsfeeds[0]['items'][0]['title']
        bz = self.newsfeeds[1]['entries'][0]['title']
        bild = self.newsfeeds[2]['entries'][0]['title']

        transfermarkt_txt = convertHtml(transfermarkt)
        bz_txt = convertHtml(bz)
        bild_txt = convertHtml(bild)

        # @future me, please clean this mess up :P
        line_txt = ['transfermarkt:','','']
        line_txt.extend(splitText(transfermarkt_txt))
        line_txt.extend(['','','','', 'BZ:','',''])
        line_txt.extend(splitText(bz_txt))
        line_txt.extend(['','','','', 'Bild:','',''])
        line_txt.extend(splitText(bild_txt))


        self.image = addTextToImage(line_txt)
        self.image.save("output.xbm", "XBM")

NEWS = NewsAggregator()
@route('/news')
def getnews():
    NEWS.updateImage()
    return static_file("output.xbm",
                       root=".",
                       mimetype='image/xbm')


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, quiet=False)
