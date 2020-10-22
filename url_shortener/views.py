from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.http.response import JsonResponse
from rest_framework import status
from url_shortener.models import ShorteneddURL
import random
import json


def index(request):
    return render(request, 'url_shortener/index.html')


def create_key():
    _x = list(range(0, 10)) + [c for c in 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz']
    _x = [str(item) for item in _x]
    random.shuffle(_x)
    key = ''.join(_x[:7])
    return key


@require_POST
def shorten_url(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    url  = data['url']

    try:
        short = ShorteneddURL.objects.get(url=url)
    except ShorteneddURL.DoesNotExist:
        short = ShorteneddURL.objects.create(url=url, key=create_key())

    return JsonResponse({'key': short.key}, status=status.HTTP_201_CREATED)


@require_GET
def get_url(request, key):
    short = get_object_or_404(ShorteneddURL, key=key)

    return redirect(short.url)