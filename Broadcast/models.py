from django.db import models

class Setting(models.Model): # Voice, etc
	## Field
	name = models.CharField(max_length=140)
	def __unicode__(self):
		return self.name

class Game(models.Model):
	## Relation
	setting = models.ForeignKey(Setting)

	## Custom Field
	url = models.CharField(max_length=200)
	title = models.CharField(max_length=140)

	## Naver Field
	game_id = models.CharField("Naver gameId", max_length=200)
	date = models.DateTimeField("Naver gdate")
	day = models.CharField("Naver gweek", max_length=1)
	a_full_name = models.CharField("Naver aFullName", max_length=200)
	h_full_name = models.CharField("Naver hFullName", max_length=200)
	a_score = models.IntegerField("Naver aScore", default=0)
	h_score = models.IntegerField("Naver hScore", default=0)
	rheb = models.CommaSeparatedIntegerField("Naver rheb", max_length=200)
	score_board = models.CommaSeparatedIntegerField("Naver scoreBoard", max_length=200)

class GameLog(models.Model):
	## Relation
	game = models.ForeignKey(Game)

	## Naver Field
	inn = models.IntegerField(default=1)
	seqno = models.IntegerField(default=1)
	live_text = models.CharField(max_length=200)
	text_style = models.IntegerField(default=0)
	btop = models.IntegerField(default=0)
