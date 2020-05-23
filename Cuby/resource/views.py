import json
from easydict import EasyDict
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, F, Q, Min
from resource.models import Resource
from user.models import User
import Cuby.settings
import os


class GetUploadLimit(View):
    def get(self):
        return JsonResponse({'size': '上传的所有资源总大小不能超过100Mb', 'byte': 104857600})


class UploadFile(View):
    def post(self, request):
        errc = EasyDict()
        errc.toobig = -1
        errc.unknown = 1

        file = request.FILES.get("file", None)
        if User.objects.filter().filesize+file.size>104857600:          # 需要更改
            return JsonResponse({'src': '', 'status': errc.tobig, 'wrong_msg': '上传资源的总大小超过了限制'})
        destination = open(os.path.join("~/upload", file.name), 'wb+')
        for chunk in file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        res = Resource(title=file.name, file_path=os.path.join("~/upload", file.name), file_size=file.size);
        res.save()
        return JsonResponse({'src': destination, 'status': 0, 'wrong_msg': ''})


class EditFileMessage(View):
    def post(self, request):
        errc = EasyDict()
        errc.unknown = -1
        errc.notfound = 1
        errc.notag = 2
        errc.notitle = 3
        errc.title_toolong = 4

        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'title', 'introduction', 'tags', 'points', 'src', 'rid'}:
            return JsonResponse({'status': errc.unknown, 'wrong_msg': '参数错误'})

        if ~Resource.objects.filter(title=kwargs['title']).exist():
            return JsonResponse({'status': errc.notfound, 'wrong_msg': '资源不在博客网站中'})

        if kwargs['tags'] == '':
            return JsonResponse({'status': errc.nottag, 'wrong_msg': '标签为空'})

        if kwargs['tags'] == '':
            return JsonResponse({'status': errc.notitle, 'wrong_msg': '名称为空'})

        if kwargs['tags'].len > 20:
            return JsonResponse({'status': errc.title_toolong, 'wrong_msg': '名称过长'})

        Resource.objects.get(title=kwargs['title']).update(title=kwargs['title'],
                                                           description=kwargs['introduction'],
                                                           tags=kwargs['tags'],
                                                           points=kwargs['points'],
                                                           file_path=kwargs['src'],
                                                           id=kwargs['rid'])
        return JsonResponse({'status': 0, 'wrong_msg': ''})


class GetResource(View):
    def get(self, request):
        kwargs: dict = json.loads(request.body)
        res = Resource.objects.all()
        num = len(res)
        res = res[(kwargs['page']-1)*kwargs['each']:kwargs['page']*kwargs['each']]
        rid = [];
        for i in res:
            rid.qppend(i.id)

        return JsonResponse({'rid': rid, 'amount': num})

