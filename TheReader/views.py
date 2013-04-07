from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext

def home(request):
	return render_to_response('main/home.html', context_instance=RequestContext(request))

def about(request):
	return render_to_response('main/about.html')

def contact(request):
	return render_to_response('main/contact.html')
