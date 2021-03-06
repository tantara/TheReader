import threading
from Broadcast.models import Game
from nsdUtils.gameUpdater import GameUpdater

def runDBUpdater(url):
	l = url.index('gameId')
	gameId = url[l+7:l+20]
	threadMap = {}

	if not gameId in threadMap.keys():
		year = gameId[:4]
		month = gameId[4:6]

		g = Game(game_id=gameId)
		g.url = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (year, month, gameId)
		g.save()
		gameUpdater = threading.Thread(target=GameUpdater, args=(g,))
		
		gameUpdater.start()		

		threadMap[gameId] = gameUpdater

	print threadMap

	for key in threadMap:
		updater = threadMap[key]
		print key

		if not updater.isAlive():
			print key
			del threadMap[key]	
