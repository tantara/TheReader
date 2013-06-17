# -*- coding: utf-8 -*-
from django.db import models

class Game(models.Model):
	## Custom Field
	url = models.CharField(max_length=200)
	cur_seqno = models.IntegerField(default=0)

	## Naver Field
	game_id = models.CharField("Naver gameId", max_length=200, primary_key=True)

	def __unicode__(self):
		return self.url

class GameLog(models.Model):
	## Relation
	game = models.ForeignKey(Game)
	action = models.ForeignKey(Action)

	## Naver Field
	inn = models.IntegerField(default=1)
	seqno = models.IntegerField(default=1)
	live_text = models.CharField(max_length=200)
	text_style = models.IntegerField(default=0)
	btop = models.IntegerField(default=0)
	flag = models.IntegerField(default=0) #FIXME

	def __unicode__(self):
		return self.live_text

class Action(models.Model): # 볼, 스트라이크, ...
	name = models.CharField(max_length=40)

class Voice(models.Model): # 최희 버전, ...
	name = models.CharField(max_length=40)
	description = models.CharField(max_length=200)

def sound_file_name(instance, filename):
    return '/'.join(['sound', instance.action.id, filename])
class Sound(models.Model): # Action에 해당하는 음원 파일
	## Relation
	action = models.ForeignKey(Action)
	voice = models.ForeignKey(Voice)

	description = models.CharField(max_length=200)
	attachment = models.FileField(upload_to=sound_file_name, max_length=200)

def team_file_name(instance, filename):
    return '/'.join(['team', instance.action.id, filename])
class Team(models.Model):
	## Relation
	game = models.ForeignKey(Game)

	name = models.CharField(max_length=40)
	description = models.CharField(max_length=200)
	attachment = models.FileField(upload_to=team_file_name, max_length=200)
	
def player_file_name(instance, filename):
    return '/'.join(['player', instance.action.id, filename])
class Player(models.Model):
	## Relation
	team = models.ForeignKey(Team)

	name = models.CharField(max_length=40)
	description = models.CharField(max_length=200)
	attachment = models.FileField(upload_to=player_file_name, max_length=200)
