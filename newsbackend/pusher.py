#!/usr/bin/python
# -*- coding: ISO8859-1 -*-
''' prepares news feed for eink devies '''

from random import choice
from time import sleep
from HTMLParser import HTMLParser
from PIL import Image, ImageDraw, ImageFont
from feedparser import parse
from serial import Serial

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


def clear_serial(ser):
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read()
    print out

if __name__ == '__main__':
    newsfeeds = []
    image = None

    interface = '/dev/ttyACM0'
    # interface = '/dev/rfcomm1'
    with Serial(interface, 9600, timeout=1) as ser:
        clear_serial(ser)
        while True:
            for feed in RSS_FEEDS:
                newsfeed = parse(feed)
                newsfeeds.append(newsfeed)

            transfermarkt = choice(newsfeeds[0]['items'])['title']
            bz = choice(newsfeeds[1]['entries'])['title']
            bild = choice(newsfeeds[2]['entries'])['title']

            try:
                transfermarkt_txt = convertHtml(transfermarkt)
                bz_txt = convertHtml(bz)
                bild_txt = convertHtml(bild)
            except:
                continue

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


            image = addTextToImage(line_txt)
            image.save("output.xbm", "XBM")
            output = None
            with open('output.xbm') as inp:
                txt = inp.readlines()
                output = ''.join(txt[3:len(txt)-1])

            output = output.replace('\n', '\r\n')
            #print repr(output)
            print output

            sleep(5)
            clear_serial(ser)
            sleep(3)
            ser.write('e01\r')
            sleep(3)
            ser.write('e01\r')
            sleep(3)
            ser.write('w\r')
            sleep(3)
            ser.write('e01\r')
            sleep(3)
            ser.write('e01\r')
            clear_serial(ser)
            sleep(3)
            ser.write('u01\r')
            sleep(3)
            clear_serial(ser)
            sleep(3)
            ser.write(repr(output))
            sleep(3)
            ser.write(';\r')
            sleep(4)
            ser.write('i01\r')
            clear_serial(ser)
            sleep(10)
