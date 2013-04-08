from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from nsdUtils.nsdParser import UrlParser

def show(request):
	if request.method == "POST":
		form = request.POST
		url = form['url']
		nsdData = UrlParser(url)
		nsdData.parsingLiveTexts()
		return render_to_response('broadcast/show.html', {'url': url, 'nsdData': nsdData})
	else:
		return HttpResponse(status=500)
