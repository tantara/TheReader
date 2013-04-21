from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from nsdUtils.nsdParser import UrlParser
import json
from django.views.decorators.csrf import csrf_exempt
from Broadcast.models import Game, GameLog
from django.core import serializers

def enter(request):
	if request.method == "POST":
		url = request.POST['url']
		nsdData = UrlParser(url)
		l = url.index('gameId')
		gameId = url[l+7:l+20]
		game = Game.objects.get(game_id = gameId)
		return redirect('/broadcast/' + game.game_id)
	else:
		return HttpResponse(status=500)

def show(request, gameId):
	if request.method == "GET":
		game = Game.objects.get(game_id = gameId)
		return render_to_response('broadcast/show.html', {'game': game})
	else:
		return HttpResponse(status=500)

@csrf_exempt
def reload(request):
	if request.method == "POST":
		gameId = request.POST['gameId']
		seqno = request.POST['seqno']
		gameLog = GameLog.objects.all()#filter(game_id = gameId, seqno__gt = seqno)
		json = serializers.serialize('json', gameLog, fields=('seqno','live_text'))
		return HttpResponse(json)
	else:
		return HttpResponse(status=500)
