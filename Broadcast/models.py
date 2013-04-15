from django.db import models

class Game(models.Model):
	## Custom Field
	url = models.CharField(max_length=200)

	## Naver Field
	game_id = models.CharField("Naver gameId", max_length=200)

	def __unicode__(self):
		return self.url

class GameLog(models.Model):
	## Relation
	game = models.ForeignKey(Game)

	## Naver Field
	inn = models.IntegerField(default=1)
	seqno = models.IntegerField(default=1)
	live_text = models.CharField(max_length=200)
	text_style = models.IntegerField(default=0)
	btop = models.IntegerField(default=0)
	flag = models.IntegerField(default=0)

	def __unicode__(self):
		return self.live_text

class Action(models.Model):
	name = models.CharField(max_length=200)

class Voice(models.Model):
	name = models.CharField(max_length=200)

def sound_file_name(instance, filename):
    return '/'.join(['sound', instance.action.id, filename])
class Sound(models.Model):
	## Relation
	action = models.ForeignKey(Action)
	voice = models.ForeignKey(Voice)

	description = models.CharField(max_length=200)
	attachment = models.FileField(upload_to=sound_file_name, max_length=200)
