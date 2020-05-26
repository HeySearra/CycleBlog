import json
from easydict import EasyDict
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.db.models import Count, F, Q, Min
from article.models import Article, Collection, Collect
from user.models import User
from resource.models import Resource
from utils.response import JSR


class GetClist(View):
    @JSR('collections')
    def get(self, request):
        col = Collection.objects.all()
        ret = []
        for collection in col:
            ret.append({'cid': collection.id,
                        'title': collection.name,
                        'condition': 1 if collection.hide else 0,
                        'count': collection.totalnum})
        return ret


class GetCinfo(View):
    @JSR('dist', 'amount')
    def get(self, request):
        kwargs: dict = json.loads(request.body)
        u = Collection.objects.filter(id=kwargs['cid']).get().owner.id
        col = Collect.objects.filter(user=u).order_by('time')
        num = len(col)
        col = col[(kwargs['page'] - 1) * kwargs['each']:kwargs['page'] * kwargs['each']]
        rid = []
        for i in col:
            if i.article < 1:
                rid.append({'rid': i.resource})
            else:
                rid.append({'aid': i.article})
        return rid, num


class AddArticle(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'aid'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['cid']).exist():
            return 1, '收藏夹不存在'
        col = Collection.objects.filter(id=kwargs['cid']).get()
        if not Article.objects.filter(id=kwargs['aid']).exist():
            return -1, '文章不存在'
        article = Article.objects.filter(id=kwargs['aid']).get()
        if article in col.articles.all():
            return 2, '文章已经在收藏夹内'
        col.articles.add(article)
        col.save()
        return 0, ''


class AddResource(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'rid'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['cid']).exist():
            return 1, '收藏夹不存在'
        col = Collection.objects.filter(id=kwargs['cid']).get()
        if not Resource.objects.filter(id=kwargs['rid']).exist():
            return -1, '资源不存在'
        res = Resource.objects.filter(id=kwargs['rid']).get()
        if res in col.resources.all():
            return 2, '资源已经在收藏夹内'
        col.resources.add(res)
        col.save()
        return 0, ''


class RemoveArticle(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'aid'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['cid']).exist():
            return -1, '收藏夹不存在'
        col = Collection.objects.filter(id=kwargs['cid']).get()
        if not Article.objects.filter(id=kwargs['aid']).exist():
            return -1, '文章不存在'
        article = Article.objects.filter(id=kwargs['aid']).get()
        if article not in col.articles.all():
            return 1, '文章不在收藏夹内'
        col.articles.remove(article)
        col.save()
        return 0, ''


class RemoveResource(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'rid'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['cid']).exist():
            return -1, '收藏夹不存在'
        col = Collection.objects.filter(id=kwargs['cid']).get()
        if not Resource.objects.filter(id=kwargs['rid']).exist():
            return -1, '资源不存在'
        res = Resource.objects.filter(id=kwargs['rid']).get()
        if res not in col.resources.all():
            return 1, '资源不在收藏夹内'
        col.resources.remove(res)
        col.save()
        return 0, ''


class NewCollection(View):
    @JSR('status', 'cid', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'title', 'condition'}:
            return -1, '参数错误'
        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return -1, 0, ''
        u = u.get()
        if Collection.objects.filter(id=kwargs['cid']).exist():
            return 1, 0, '已存在该收藏夹'
        col = Collection(name=kwargs['title'], hide=kwargs['condition'], owner=u.id)
        col.save()
        return 0, col.id, ''


class Rename(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'name'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['cid']).exist():
            return 1, '收藏夹不存在'
        col = Collection.objects.filter(id=kwargs['cid']).get()
        col.name = kwargs['name']
        col.save()
        return 0, ''


class SetCondition(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'condition'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['cid']).exist():
            return 1, '收藏夹不存在'
        col = Collection.objects.filter(id=kwargs['cid']).get()
        col.hide = kwargs['condition']
        col.save()
        return 0, ''


class DelCollection(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['cid']).exist():
            return 1, '不存在该收藏夹'
        Collection.objects.filter(id=kwargs['cid']).delete()
        return 0, ''


class MoveArticle(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'src', 'dst', 'aid'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['src']).exist():
            return 1, '原收藏夹不存在'
        if not Collection.objects.filter(id=kwargs['dst']).exist():
            return 1, '新收藏夹不存在'
        col = Collection.objects.filter(id=kwargs['src']).get()
        if not Article.objects.filter(id=kwargs['aid']).exist():
            return -1, '文章不存在'
        article = Article.objects.filter(id=kwargs['aid']).get()
        if article not in col.articles.all():
            return -1, '文章不在原收藏夹内'
        col.articles.remove(article)
        col.save()
        col = Collection.objects.filter(id=kwargs['dst']).get()
        if article in col.articles.all():
            return -1, '文章已在新收藏夹内'
        col.articles.add(article)
        col.save()
        return 0, ''


class MoveResource(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'src', 'dst', 'rid'}:
            return -1, '参数错误'
        if not Collection.objects.filter(id=kwargs['src']).exist():
            return 1, '原收藏夹不存在'
        if not Collection.objects.filter(id=kwargs['dst']).exist():
            return 1, '新收藏夹不存在'
        col = Collection.objects.filter(id=kwargs['src']).get()
        if not Resource.objects.filter(id=kwargs['rid']).exist():
            return -1, '资源不存在'
        res = Resource.objects.filter(id=kwargs['rid']).get()
        if res not in col.resources.all():
            return -1, '资源不在原收藏夹内'
        col.resources.remove(res)
        col.save()
        col = Collection.objects.filter(id=kwargs['dst']).get()
        if res in col.resources.all():
            return -1, '资源已在新收藏夹内'
        col.resources.add(res)
        col.save()
        return 0, ''



