import urllib2
import urllib
import ast
import operator
from Broadcast.models import Game,GameLog

class GameUpdater: # Gmae db Updater
	## naver sports data url parser & save Game if not exists
	def __init__(self, Url):
		l = Url.index('gameId')
		gameId = Url[l+7:l+20]

		checkExists = Game.objects.get_or_create(game_id=gameId)
		self.game = checkExists[0]

		if checkExists[1]:
			year = gameId[:4]
			month = gameId[4:6]

			self.game.url = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (year, month, gameId)
			self.game.save()
			
		while not checkGameEnd():
			updateNsdDic()
			updateGameLog()
	
	## update naver sports data dictonary
	def updateNsdDic(self):
		url = self.game.url

		data = urllib2.urlopen(url).read()
		x = data.index('{"games')
		y = data.index(');</script>')
		self.nsdDic = ast.literal_eval(data[x:y])

	## update GameLog by game
	def updateGameLog(self):
		game = self.game
		curSeqno = game.cur_seqno
		curInn = 1
		if curSeqno != 0:
			curInn = GameLog.objects.get(game=self.game, seqno=curSeqno).inn

		l = len(self.nsdDic["relayTexts"])
		l = l - 3
		if 'final' in self.nsdDic['relayTexts']:
			l = l - 1

		liveTexts = []
		for i in xrange(curInn, l):
			liveTexts += liveTexts + self.nsdDic['relayTexts'][str(i)]

		liveTexts.sort(key=operator.itemgetter('seqno'))

		for text in self.liveTexts:
			if text['seqno'] > self.game.cur_seqno:
				newLog = GameLog()
				newLog.game = self.game
				newLog.inn = text['inn']
				newLog.seqno = text['seqno']
				newLog.live_text = text['liveText']
				newLog.btop = text['btop']
				newLog.save()

				curSeqno = text['seqno']
		
		self.game.cur_seqno = curSeqno
		self.game.save()

	## test function
	def testData(self):
		print self.nsdDic["relayTexts"]["1"][3]["seqno"]

	## check Game End
	def checkGameEnd(self):
		game = self.game
		seqNo = game.cur_seqno

		if seqNo == 0:
			return False

		return GameLog.objects.filter(game=game, seqno=seqNo).live_text != u'경기종료'
