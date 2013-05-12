# -*- coding: utf-8 -*-
import urllib2
import urllib
import ast
import operator
import time
import re
from Broadcast.models import Game,GameLog

class GameUpdater: # Gmae db Updater
	## naver sports data url parser & save Game if not exists
	def __init__(self, game):
		self.game = game 
			
		while not self.checkGameEnd():
			print "sleep1"
			self.updateNsdDic()
			self.updateGameLog()
			time.sleep(5)
	
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
			liveTexts += self.nsdDic['relayTexts'][str(i)]

		liveTexts.sort(key=operator.itemgetter('seqno'))

		self.hitFlag = False

		for text in liveTexts:
			if text['seqno'] > self.game.cur_seqno:
				newLog = GameLog()
				newLog.game = self.game
				newLog.inn = text['inn']
				newLog.seqno = text['seqno']
				newLog.live_text = text['liveText']
				newLog.btop = text['btop']
				newLog.flag = self.parseFlag(text['liveText'])
				newLog.save()

				curSeqno = text['seqno']
		
		self.game.cur_seqno = curSeqno

		self.game.save()

	## test function
	def testData(self):
		print self.nsdDic["relayTexts"]["1"][3]["seqno"]

	## check Game End
	def checkGameEnd(self):
		print self.game
		game = self.game
		seqNo = game.cur_seqno

		if seqNo == 0:
			return False

		return GameLog.objects.filter(game=game, seqno=seqNo)[0].live_text != u'경기종료'

	def parseFlag(self, liveText):
		if self.hitFlag:
			if bool(re.search('\d번타자', liveText)):
				self.hitFlag = False;
				return 310 + int(re.findall('\d', liveText)[0])
			elif bool(re.search('\d루주자', liveText)):
				position = int(re.findall('\d', liveText)[0])
				if '진루' in livetext:
					return 21100 + position * 10 + int(re.findall('\d', liveText)[1])	#10의자리는 기존의 있던 베이스 1의자리는 진루한 베이스
				elif '홈인' in liveText:
					return 21104 + position * 10 #10의자리는 기존의 있던 베이스 1의자리는 진루한 베이스
				elif '태그아웃' in liveText:
					return 2230 + position #1의자리는 기존에 있던 베이스
			elif '안타' in liveText:
				return 121
			elif '2루타' in liveText:
				return 122
			elif '3루타' in liveText:
				return 123
			elif '홈런' in liveText:
				return 124
			elif '희생번트' in liveText:
				return 128
			elif '실책으로 출루' in liveText:
				return 129
			elif '플라이' in liveText:
				return 132
			elif '땅볼' in liveText:
				return 133
			elif '병살타' in liveText:
				return 134
##			elif '삼중살' in liveText: 아직 모름.
##				return 135
			elif '희생번트' in liveText:
				return 136
			else:
				return 0
		else:
			if '타격' in liveText:
				self.hitFlag = True
				return 0
			elif bool(re.search('\d번타자', liveText)):
				return 310 + int(re.findall('\d', liveText)[0])
			elif bool(re.search('\d루주자', liveText)):
				position = int(re.findall('\d', liveText)[0])
				if '도루실패' in liveText: 
					return 2220 + position #1의자리는 기존에 있던 베이스
				elif '도루' in liveText: 
					return 2130 + position #1의자리는 기존에 있던 베이스
				elif '진루' in liveText:
					return 21100 + position * 10 + int(re.findall('\d', liveText)[1]) #10의자리는 기존의 있던 베이스 1의자리는 진루한 베이스
				elif '홈인' in liveText:
					return 21104 + position * 10 #10의자리는 기존의 있던 베이스 1의자리는 진루한 베이스
			elif '볼넷' in liveText:
				return 125
			elif '몸에 맞는 볼' in liveText:
				return 126
			elif '스트라이크 낫아웃' in liveText:
				return 127
			elif '스트라이크' in liveText:
				return 111
			elif '볼' in liveText:
				return 112
			elif '파울' in liveText:
				return 113
			elif '헛스윙' in liveText:
				return 114
			elif '삼진 아웃' in liveText:
				return 131
			else:
				return 0;
