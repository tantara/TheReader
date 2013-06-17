# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse
import time
from Broadcast.models import Game

year = time.strftime("%Y")
month = time.strftime("%m")
day = time.strftime("%d") 
date = year + month + day # "20130615"

print date

def crawl_games():
	url = "http://sports.news.naver.com/schedule/scoreBoard.nhn?date=" +  date
	html = urllib2.urlopen(url).read()

	soup = BeautifulSoup(html, "lxml")
	game_list = soup.find("ul", class_="sch_lst")

	games = game_list.find_all("li")
	
	for game in games:
		home = game.find("div", class_="sch_lft").p.strong.string
		away = game.find("div", class_="sch_rgt").p.strong.string

		try:
			link = game.find("div", class_="sch_btn_lft").a['href']
			o = urlparse(link)
			query = dict([q.split("=") for q in o.query.split("&")])

			category = query['category']
			gameId = query['gameId']
		except:
			category = "null"
			gameId = "null"

		g = Game(game_id=gameId)
		g.url = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (year, month, gameId)
		g.save()

		print home + " vs " + away + "(" + id + ", " + category + ")"

crawl_games()
