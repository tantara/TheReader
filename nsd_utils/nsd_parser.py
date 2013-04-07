import urllib2
import urllib
import ast

class UrlParser(): # Url Parser
	## naver sports data url parser
	nsd_url = ""
	game_id = ""
	year = ""
	month = ""
	nsd_dic = {}

	def	nsd_parsing(self, Url):
		l = len(Url)
		self.game_id = Url[l-13:]
		self.year = self.game_id[:4]
		self.month = self.game_id[4:6]

		self.nsd_url = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (self.year, self.month, self.game_id)
		data = urllib2.urlopen(self.nsd_url).read()
		x = data.index('{"games')
		y = data.index(');</script>')
		self.nsd_dic = ast.literal_eval(data[x:y])
		print self.nsd_dic["gameInfo"]["aFullName"]

	def testData(self):
		print self.nsd_dic["relayTexts"]["1"][3]["seqno"]

urlParser = UrlParser()
urlParser.nsd_parsing("http://sports.news.naver.com/gameCenter/miniTextRelay.nhn?category=kbo&date=20130403&gameId=20130403LGWO0")
