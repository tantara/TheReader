from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import nsdUtils.runDBUpdater as dbUpdater
import json
from django.views.decorators.csrf import csrf_exempt

def show(request):
	if request.method == "POST":
		url = request.POST['url']
		return render_to_response('broadcast/show.html', {'url': url})
	else:
		return HttpResponse(status=500)

@csrf_exempt
def reload(request):
	if request.method == "POST":
		url = request.POST['url']
		dbUpdater.runDBUpdater(url)
		nsdData.parsingLiveTexts()
		return HttpResponse(json.dumps(nsdData.liveTexts))
	else:
		return HttpResponse(status=500)
