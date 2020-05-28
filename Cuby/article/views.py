import json
from easydict import EasyDict
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.db.models import Count, F, Q, Min
from article.models import Article, Collection, ArticleCollect, ResourceCollect
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
        col = ArticleCollect.objects.filter(user=u).order_by('time')
        num = len(col)
        col = col[(kwargs['page'] - 1) * kwargs['each']:kwargs['page'] * kwargs['each']]
        rid = []
        for i in col:
            if i.article < 1:
                rid.append({'rid': i.resource})
            else:
                rid.append({'aid': i.article})
        return rid, num


class CollectArticle(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'aid'}:
            return -1, '参数错误'
        col = Collection.objects.filter(id=kwargs['cid'])
        if not col.exist():
            return 1, '收藏夹不存在'
        col = col.get()
        atc = Article.objects.filter(id=kwargs['aid'])
        if not atc.exist():
            return -1, '文章不存在'
        atc = atc.get()
        src_list = ArticleCollect.objects.filter(collection=col, article=atc)
        if src_list.exists():
            return 2, '文章已经在收藏夹内'
        ArticleCollect.objects.create(Collection=col, Article=atc)
        return 0, ''


class CollectResource(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'rid'}:
            return -1, '参数错误'
        col = Collection.objects.filter(id=kwargs['cid'])
        if not col.exist():
            return 1, '收藏夹不存在'
        col = col.get()
        res = Resource.objects.filter(id=kwargs['rid'])
        if not res.exist():
            return -1, '资源不存在'
        res = res.get()
        src_list = ResourceCollect.objects.filter(collection=col, resource=res)
        if src_list.exists():
            return 2, '资源已经在收藏夹内'
        ResourceCollect.objects.create(Collection=col, Resource=res)
        return 0, ''


class RemoveArticleFromCollection(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'aid'}:
            return -1, '参数错误'
        col = Collection.objects.filter(id=kwargs['cid'])
        if not col.exist():
            return 1, '收藏夹不存在'
        col = col.get()
        atc = Article.objects.filter(id=kwargs['aid'])
        if not atc.exist():
            return -1, '文章不存在'
        atc = atc.get()
        src_list = ArticleCollect.objects.filter(collection=col, article=atc)
        if not src_list.exists():
            return 1, '文章不在收藏夹内'
        atc.delete()
        return 0, ''


class RemoveResourceFromCollection(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'rid'}:
            return -1, '参数错误'
        col = Collection.objects.filter(id=kwargs['cid'])
        if not col.exist():
            return 1, '收藏夹不存在'
        col = col.get()
        res = Resource.objects.filter(id=kwargs['rid'])
        if not res.exist():
            return -1, '资源不存在'
        res = res.get()
        src_list = ResourceCollect.objects.filter(collection=col, resource=res)
        if not src_list.exists():
            return 1, '资源不在收藏夹内'
        src_list.delete()
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
        col = Collection.objects.filter(id=kwargs['cid'])
        if col.exist():
            return 1, 0, '已存在该收藏夹'
        col = Collection.objects.create(name=kwargs['title'], hide=kwargs['condition'], owner=u.id)
        return 0, col.id, ''


class Rename(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'name'}:
            return -1, '参数错误'
        col = Collection.objects.filter(id=kwargs['cid'])
        if not col.exist():
            return 1, '收藏夹不存在'
        col = col.get()
        col.name = kwargs['name']
        col.save()
        return 0, ''


class SetCondition(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'cid', 'condition'}:
            return -1, '参数错误'
        col = Collection.objects.filter(id=kwargs['cid'])
        if not col.exist():
            return 1, '收藏夹不存在'
        col = col.get()
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
        col_src = Collection.objects.filter(id=kwargs['src'])
        if not col_src.exist():
            return 1, '原收藏夹不存在'
        col_src = col_src.get()
        col_dst = Collection.objects.filter(id=kwargs['dst'])
        if not col_dst.exist():
            return 1, '新收藏夹不存在'
        col_dst = col_dst.get()
        res = Article.objects.filter(id=kwargs['aid'])
        if not res.exist():
            return -1, '文章不存在'
        res = res.get()
        src_list = ArticleCollect.objects.filter(collection=col_src, article=res)
        if not src_list.exists():
            return -1, '文章不在原收藏夹内'
        src_list.delete()
        dst_list = ArticleCollect.objects.filter(collection=col_dst, article=res)
        if dst_list.exists():
            return -1, '文章已在新收藏夹内'
        ArticleCollect.objects.create(collection=col_dst, article=res)
        return 0, ''

class MoveResource(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'src', 'dst', 'rid'}:
            return -1, '参数错误'
        col_src = Collection.objects.filter(id=kwargs['src'])
        if not col_src.exist():
            return 1, '原收藏夹不存在'
        col_src = col_src.get()
        col_dst = Collection.objects.filter(id=kwargs['dst'])
        if not col_dst.exist():
            return 1, '新收藏夹不存在'
        col_dst = col_dst.get()
        res = Resource.objects.filter(id=kwargs['rid'])
        if not res.exist():
            return -1, '资源不存在'
        res = res.get()
        src_list = ResourceCollect.objects.filter(collection=col_src, resource=res)
        if not src_list.exists():
            return -1, '资源不在原收藏夹内'
        src_list.delete()
        dst_list = ResourceCollect.objects.filter(collection=col_dst, resource=res)
        if dst_list.exists():
            return -1, '资源已在新收藏夹内'
        ResourceCollect.objects.create(collection=col_dst, resource=res)
        return 0, ''



