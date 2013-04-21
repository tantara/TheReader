import thread
from Broadcast.models import Game
from nsdUtils.gameUpdater import GameUpdater

def runDBUpdater(url):
	if not Game.objects.filter(url=url):
		l = url.index('gameId')
		gameId = url[l+7:l+20]
		g = Game(game_id=gameId)
		g.save()
		thread.start_new_thread(GameUpdater, (g,))
