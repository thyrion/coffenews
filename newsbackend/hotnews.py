#!/usr/bin/python
# -*- coding: ISO8859-1 -*-
''' prepares news feed for eink devies '''

from random import choice
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
FONTSIZE = 8
#FONT = ImageFont.truetype("res/Minecraftia-Regular.ttf", FONTSIZE)
FONT = ImageFont.load("res/pilfonts/charR08.pil")
XOFFSET = 2
YOFFSET = 2

def addTextToImage(text):
    ''' want already correctly split text '''
    image = Image.new("1", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(image)
    height = YOFFSET
    for h in range(0, len(text)):
        draw_txt = text[h]
        #(_, theight) = FONT.getsize(draw_txt)
        draw.text((XOFFSET, height), draw_txt, 255, font=FONT)
        height += 10
    return image


def splitText(text):
    ''' split text to match display '''
    txt_array = text.split()
    line_txt = []
    start = 0
    for i in range(0, len(txt_array) + 1):
        #(tlength, _) = FONT.getsize(' '.join(txt_array[start:i]))
        tlength = len(' '.join(txt_array[start:i])) * 5
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
    txt = h.unescape(text).encode('ISO8859-1')
    return h.unescape(txt)

class NewsAggregator(object):
    newsfeeds = []
    image = None


    def __init__(self):
        pass

    def updateImage(self):
        for feed in RSS_FEEDS:
            newsfeed = parse(feed)
            self.newsfeeds.append(newsfeed)

        transfermarkt = choice(self.newsfeeds[0]['items'])['title']
        bz = choice(self.newsfeeds[1]['entries'])['title']
        bild = choice(self.newsfeeds[2]['entries'])['title']

        transfermarkt_txt = convertHtml(transfermarkt)
        bz_txt = convertHtml(bz)
        bild_txt = convertHtml(bild)

        # @future me, please clean this mess up :P
        #line_txt = ['transfermarkt:','','']
        line_txt = ['transfermarkt:']
        line_txt.extend(splitText(transfermarkt_txt))
        #line_txt.extend(['','','','', 'BZ:','',''])
        line_txt.extend(['BZ:'])
        line_txt.extend(splitText(bz_txt))
        #line_txt.extend(['','','','', 'Bild:','',''])
        line_txt.extend(['Bild:'])
        line_txt.extend(splitText(bild_txt))


        self.image = addTextToImage(line_txt)
        self.image.save("output.xbm", "XBM")
        with open('output.xbm') as inp, open('outputcrlf.xbm', 'w') as out:
            txt = inp.read()
            txt = txt.replace('\n', '\r\n')
            out.write(txt)

NEWS = NewsAggregator()
@route('/news')
def getnews():
    NEWS.updateImage()
    return static_file("outputcrlf.xbm",
                       root=".",
                       mimetype='image/xbm')


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, quiet=False)
