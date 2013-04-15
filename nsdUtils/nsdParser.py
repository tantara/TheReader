import urllib2
import urllib
import ast
import operator
from Broadcast.models import Game,GameLog

class UrlParser: # Url Parser
	## naver sports data url parser
	def __init__(self, Url):
		self.liveTexts = []
		self.seqno = 0

		l = Url.index('gameId')
		gameId = Url[l+7:l+20]
		year = gameId[:4]
		month = gameId[4:6]

		nsdUrl = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (year, month, gameId)
		data = urllib2.urlopen(nsdUrl).read()
		x = data.index('{"games')
		y = data.index(');</script>')
		self.nsdDic = ast.literal_eval(data[x:y])
	
	def haveGameDB(self, gameId):
		GameList = Game.objects.all() 

	## test function
	def testData(self):
		print self.nsdDic["relayTexts"]["1"][3]["seqno"]

	## live Texts sort by seqno
	def parsingLiveTexts(self):
		l = len(self.nsdDic["relayTexts"])
		l = l - 3
		if 'final' in self.nsdDic['relayTexts']:
			l = l - 1

		for i in xrange(1, l):
			self.liveTexts = self.liveTexts + self.nsdDic['relayTexts'][str(i)]

		self.liveTexts.sort(key=operator.itemgetter('seqno'))
		print self.liveTexts

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
			
