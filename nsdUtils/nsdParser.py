import urllib2
import urllib
import ast
import operator
from Broadcast.models import Game,GameLog

class UrlParser: # Url Parser
	## naver sports data url parser & save Game if not exists
	def __init__(self, Url):
		self.seqno = 0

		l = Url.index('gameId')
		gameId = Url[l+7:l+20]
		checkExists = Game.objects.get_or_create(game_id=gameID)
		game = checkExists[0]
		if checkExists[1]:
			year = gameId[:4]
			month = gameId[4:6]

			nsdUrl = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (year, month, gameId)
			game.url = nsdUrl
			game.save()
		else:
			nsdUrl = game.url

		data = urllib2.urlopen(nsdUrl).read()
		x = data.index('{"games')
		y = data.index(');</script>')
		self.nsdDic = ast.literal_eval(data[x:y])

	## test function
	def testData(self):
		print self.nsdDic["relayTexts"]["1"][3]["seqno"]

	## update GameLog by game
	def parseGameLog(self, game):
		curSeqno = game.cur_seqno
		curInn = GameLog.objects.get(game=game, seqno=curSeqno).inn

		l = len(self.nsdDic["relayTexts"])
		l = l - 3
		if 'final' in self.nsdDic['relayTexts']:
			l = l - 1

		liveTexts = []
		for i in xrange(curInn, l):
			liveTexts += liveTexts + self.nsdDic['relayTexts'][str(i)]

		self.liveTexts.sort(key=operator.itemgetter('seqno'))

		for text in self.liveTexts:
			if text['seqno'] > game.cur_seqno:
				newLog = GameLog()
				newLog.game = game
				newLog.inn = text['inn']
				newLog.seqno = text['seqno']
				newLog.live_text = text['liveText']
				newLog.save()

				curSeqno = text['seqno']
		
		game.cur_seqno = curSeqno
		game.save()

	## parsing by (text, flag) list after readed seqno
	def matchingTexts(self):
		def matchingText(liveText):
			textData = {'text': liveText.decode('utf-8'), 'flag': 1}
			return textData

		l = len(self.liveTexts)
		voiceList = []

		for i in xrange(self.seqno+1, l):
			voiceList.append(matchingText(self.liveTexts[i]['liveText']))

		self.seqno = l
		return voiceList
			
