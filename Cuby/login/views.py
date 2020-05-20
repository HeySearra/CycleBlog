from django.core.paginator import Paginator
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.shortcuts import render
import simplejson
import login.models as login_models


def register(request):
    pass


def index(request):
    pass


def login(request):
    if request.session.get('is_login', None):
        return redirect(reverse('index'))
    if request.method == 'POST':
        data = simplejson.loads(request.body)
        new_user = login_models.User()
        new_user.name = data['name']
        new_user.password = hash(data['password'])
        new_user.account = data['account']
        new_user.save()
        return JsonResponse({'status': 0})
