import json
from easydict import EasyDict
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, F, Q, Min
from resource.models import Resource
from user.models import User
import os
from utils.response import JSR
from resource.hypers import *


class GetUploadLimit(View):
    @JSR('size', 'byte')
    def get(self):
        return MAX_UPLOADED_FSIZE_DESC, MAX_UPLOADED_FSIZE


class UploadFile(View):
    @JSR('src', 'status', 'wrong_msg')
    def post(self, request):
        errc = EasyDict()
        errc.unknown = -1
        errc.toobig = 1

        file = request.FILES.get("file", None)
        if not file:
            return '', errc.unknown, '获取文件失败'
        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return '', errc.unknown, '获取用户失败'
        u = u.get()
        
        if u.filesize + file.size > MAX_UPLOADED_FSIZE:
            return '', errc.toobig, f'上传资源的总大小超过了限制({MAX_UPLOADED_FSIZE_DESC})'
        
        file_path = os.path.join(DEFAULT_FILE_ROOT, file.name)
        with open(file_path, 'wb+') as dest:
            [dest.write(chunk) for chunk in file.chunks]
        res = Resource(title=file.name, file_path=file_path, file_size=file.size)
        try:
            res.save()
        except:
            return '', errc.unknown, '文件保存失败'
        return file_path, 0, ''


class EditFileMessage(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        errc = EasyDict()
        errc.unknown = -1
        errc.notfound = 1
        errc.notag = 2
        errc.notitle = 3
        errc.title_toolong = 4
        
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'title', 'introduction', 'tags', 'points', 'src', 'rid'}:
            return errc.unknown, '参数错误'
        
        if not Resource.objects.filter(title=kwargs['title']).exist():
            return errc.notfound, '资源不在博客网站中'
        
        if kwargs['tags'] == '':
            return errc.notag, '标签为空'
        
        if kwargs['tags'] == '':
            return errc.notitle, '名称为空'
        
        if kwargs['tags'].len > 20:
            return errc.title_toolong, '名称过长'
        
        Resource.objects.get(title=kwargs['title']).update(title=kwargs['title'],
                                                           description=kwargs['introduction'],
                                                           tags=kwargs['tags'],
                                                           points=kwargs['points'],
                                                           file_path=kwargs['src'],
                                                           id=kwargs['rid'])
        return 0, ''


class GetResource(View):
    @JSR('rid', 'amount')
    def get(self, request):
        kwargs: dict = json.loads(request.body)
        res = Resource.objects.all()
        num = res.count()
        res = res[(kwargs['page'] - 1) * kwargs['each']:kwargs['page'] * kwargs['each']]
        
        return [i.id for i in res], num


class GetDownload(View):
    @JSR('rid', 'amount')
    def get(self, request):
        kwargs: dict = json.loads(request.body)
        resource = User.download.filter(user=User.objects.filter(id=request.session['uid']).get())
        num = len(resource)
        resource = resource[(kwargs['page'] - 1) * kwargs['each']:kwargs['page'] * kwargs['each']]
        rid = []
        for i in resource:
            rid.append(i.id)

        return rid, num


class DelResource(View):
    @JSR('status', 'wrong_msg')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'rid'}:
            return -1, '参数错误'

        if Resource.objects.filter(id=kwargs['rid']).exist():
            Resource.objects.filter(id=kwargs['rid']).delete()
            return 0, ''
        else:
            return 1, '没有该文件'
