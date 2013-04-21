import thread
from Broadcast.models import Game
from nsdUtils.gameUpdater import GameUpdater

def runDBUpdater(url):
	if Game.Object.filter(url=url):
		thread.start_new_thread(GameUpdater, (url,))
