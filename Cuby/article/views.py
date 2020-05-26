import json
from easydict import EasyDict
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.db.models import Count, F, Q, Min
from article.models import Article, Collection, Collect
from user.models import User
from resource.models import Resource
#from utils.response import JSR


class GetClist(View):
    def get(self, request):
        col = Collection.objects.all()
        ret = []
        for collection in col:
            ret.append({'cid': collection.id,
                        'title': collection.name,
                        'condition': 1 if collection.hide else 0,
                        'count': collection.totalnum})
        return JsonResponse({'collections': ret})


class GetCinfo(View):
    def get(self, request):
        kwargs: dict = json.loads(request.body)
        u = Collection.objects.filter(id=kwargs['cid']).get().owner.id
        col = Collect.objects.filter(user=u).order_by('time')
        num = len(col)
        col = col[(kwargs['page'] - 1) * kwargs['each']:kwargs['page'] * kwargs['each']]
        rid = []
        for i in col:
            if
            rid.append({})

        return JsonResponse({'dist': rid, 'amount': num})


class AddArticle(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)

