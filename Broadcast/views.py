from django.http import HttpResponse
from django.shortcuts import render, render_to_response
import nsd_utils.nsd_parser

def show(request):
	if request.method == "POST":
		form = request.POST
		url = form['url']
		return render_to_response('broadcast/show.html', {'url': url})
	else:
		return HttpResponse(status=500)
