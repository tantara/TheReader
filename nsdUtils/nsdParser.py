import urllib2
import urllib
import ast
import operator

class UrlParser: # Url Parser
	## naver sports data url parser
	def __init__(self, Url):
		l = len(Url)
		gameId = Url[l-13:]
		year = gameId[:4]
		month = gameId[4:6]

		nsdUrl = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (year, month, gameId)
		data = urllib2.urlopen(nsdUrl).read()
		x = data.index('{"games')
		y = data.index(');</script>')
		self.nsdDic = ast.literal_eval(data[x:y])
		self.liveTexts = []
		print self.nsdDic["gameInfo"]["aFullName"]

	def testData(self):
		print self.nsdDic["relayTexts"]["1"][3]["seqno"]

	def parsingLiveTexts(self):
		l = len(self.nsdDic["relayTexts"])
		l = l - 3
		if 'final' in self.nsdDic['relayTexts']:
			l = l - 1

		for i in xrange(1, l):
			self.liveTexts = self.liveTexts + self.nsdDic['relayTexts'][str(i)]

		self.liveTexts.sort(key=operator.itemgetter('seqno'))
		print self.liveTexts
