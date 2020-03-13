#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import csv
import time
import random
import logging

from waveshare_epd import epd2in13d
from PIL import Image, ImageDraw, ImageFont


# Globals
picdir = "/home/pi/Kindler/fonts"
quote_location = "/home/pi/Kindler/quotes.csv"
MAX_LINES_SMALL_FONT = 28
MAX_LINES_BIG_FONT = 20
LEN_BRACKET = 50
SPACE_BETWEEN_LINES_BIG_FONT = 15
SPACE_BETWEEN_LINES_SMALL_FONT = 20
CHANGE_QUOTE_EVERY = 3 # 60*60 # hour


#Set output log level
logging.basicConfig(level=logging.DEBUG)


def _split_words(text, n):
	words = text.split(" ")
	lines = []
	this_line = ""
	for word in words:
		if len(this_line) + len(word) > n:
			lines.append(this_line)
			this_line = word
			continue
		else:
			this_line += " %s" %word

	if this_line != "":
		lines.append(this_line)
	return lines

try:
	logging.info("epd2in13d Demo")
	epd = epd2in13d.EPD()
	logging.info("init and Clear")
	epd.init()
	epd.Clear(0xFF)
except :
	logging.error("Could not clear and find monitor!")
	sys.exit()

font_quoter = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
font_quote_small = ImageFont.truetype(os.path.join(picdir, 'EBGaramond.ttf'), 15)
font_quote_big = ImageFont.truetype(os.path.join(picdir, 'EBGaramond.ttf'), 20)
font_quote_char = ImageFont.truetype(os.path.join(picdir, 'EBGaramond.ttf'), 50)


QUOTES = []
with open(quote_location, 'r') as csvfile:
	r = csv.DictReader(csvfile, delimiter=",", quotechar="\"")
	for line in r:
		QUOTES.append([line['quote'], line['author'].replace("\"", "")])


while True:
	QUOTE, AUTHOR = random.choice(QUOTES)
	Himage = Image.new('1', (epd.height, epd.width), 0)
	draw = ImageDraw.Draw(Himage)

	if len(QUOTE) > LEN_BRACKET:
		# Big quote
		splitted = _split_words(QUOTE, n=MAX_LINES_SMALL_FONT)
		used_font = font_quote_small
		bracket = SPACE_BETWEEN_LINES_BIG_FONT

	else:
		# Small Quote
		splitted = _split_words(QUOTE, n=MAX_LINES_BIG_FONT)
		used_font = font_quote_big
		bracket = SPACE_BETWEEN_LINES_SMALL_FONT

	height = 10
	for i in splitted:
		draw.text((10, height), i.decode("utf-8").strip(), font=used_font, fill=0)
		height += bracket
	draw.text((90, 75), "- %s" % AUTHOR.decode("utf-8"), font=font_quoter, fill=0)
	# draw.text((2, 2), "\"", (100), font=font_quote_char)

	epd.display(epd.getbuffer(Himage))
	time.sleep(CHANGE_QUOTE_EVERY)
	epd.Clear(0xFF)			                # Important - Clear frame.
