import urllib2
import urllib

class UrlParser(): # Url Parser
	## naver sports data url parser
	nsd_url = ""
	def	nsd_parsing(self, Url):
		l = len(Url)
		game_id = Url[l-13:]
		year = game_id[:4]
		month = game_id[4:6]
		print game_id
		print year
		print month

		self.nsd_url = "http://sportsdata.naver.com/ndata//kbo/%s/%s/%s.nsd" % (year, month, game_id)
		data = urllib2.urlopen(self.nsd_url).read()
		print data

urlParser = UrlParser()
urlParser.nsd_parsing("http://sports.news.naver.com/gameCenter/miniTextRelay.nhn?category=kbo&date=20130403&gameId=20130403LGWO0")
