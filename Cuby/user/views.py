import json
from easydict import EasyDict
from django.http import JsonResponse
from django.views import View

from user.models import User


class Register(View):
    def post(self, request):
        errc = EasyDict()
        errc.input = 1
        errc.email = 2
        errc.pwd = 3
        errc.name = 4
        
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'password', 'name'}:
            return JsonResponse({'status': errc.input})
        
        u = User(kwargs)
        u.check()
        if User.objects.filter(account=u.email).exist():
            return JsonResponse({'status': errc.email})
        u.save()
        return JsonResponse({'status': 0})


class Login(View):  # todo: 石墨上没有参数
    expected_keys = {'account', 'password', 'name'}
    status_map = {''}
    
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != self.expected_keys:
            return JsonResponse({'status': 1})
        
        new_user = User(kwargs)
        new_user.save()
        return JsonResponse({'status': 0})
