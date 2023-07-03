from django.shortcuts import render
from django.http import HttpResponse #new

def index(request): #new
    return HttpResponse('<h1>Django Include URLs</h1>')
