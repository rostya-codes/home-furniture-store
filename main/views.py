from django.http import HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:
    return HttpResponse('Home page')


def about(request) -> HttpResponse:
    return HttpResponse('About page')

