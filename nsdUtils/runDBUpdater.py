import threading
from Broadcast.models import Game
from nsdUtils.gameUpdater import GameUpdater

def runDBUpdater(url):
	l = url.index('gameId')
	gameId = url[l+7:l+20]

	if not Game.objects.filter(game_id=gameId):
		year = gameId[:4]
		month = gameId[4:6]

		g = Game(game_id=gameId)
		g.url = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (year, month, gameId)
		g.save()
		gameUpdater = threading(target=GameUpdater, args=(g))
		
		gameUpdater.start()		

	if not gameUpdater.isAlive():
		gameUpdater.start()
