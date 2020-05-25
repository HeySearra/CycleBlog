import json

from django.utils import timezone
from datetime import datetime
from easydict import EasyDict
from django.http import JsonResponse
from django.views import View
from user.models import User
from user.hypers import *
from utils.jsonpack import UserInfoJson
from utils.response import single_value_jsr
from django.db.utils import IntegrityError, DataError


def AddYearOrMonth(startDate, year, month):
    y = startDate.year + (month / 12) + year
    m = startDate.month + (month % 12)
    if m > 12:
        m %= 12
        y += 1
    d2 = datetime.strptime('%d-%02d-%02d' % (y, m, startDate.day), "%Y-%m-%d")
    return d2


class Register(View):
    @single_value_jsr
    def post(self, request):
        E = EasyDict()
        E.uk = -1
        E.key, E.acc, E.pwd, E.name, E.uni = tuple(range(1, 5+1))
        
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'password', 'name'}:
            return E.key
        if not CHECK_ACC(kwargs['account']):
            return E.acc
        if not CHECK_PWD(kwargs['password']):
            return E.pwd
        if not CHECK_NAME(kwargs['name']):
            return E.name
        
        kwargs.update({'email' if '@' in kwargs['account'] else 'tel': kwargs['account']})
        kwargs.pop('account')
        
        u = User(kwargs)
        try:
            u.save()
        except IntegrityError:
            return E.uni    # 字段unique未满足
        except DataError:
            return E.uk     # 诸如某个CharField超过了max_len的错误
        except
        return 0


class Login(View):  # todo: 石墨上没有参数
    expected_keys = {'email', 'password'}
    status_map = {''}

    def post(self, request):
        if request.session.get('is_login', None):
            print("ddddd")
            return JsonResponse({'status': 0, 'wrong_msg': ''})
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != self.expected_keys:
            return JsonResponse(msg_dict.missing)

        try:
            user = User.objects.get(email=kwargs['email'])
            if user.blocked == False:
                if user.password == kwargs['password'] and (user.wrong_count < 5 or user.login_time.strftime('%Y%m%d') != timezone.now().strftime('%Y%m%d')):
                    request.session['is_login'] = True
                    request.session['uid'] = user.id
                    request.session['name'] = user.name
                    if(user.vip_time.__le__(timezone.now())):
                        user.identity = 'user'
                    else:
                        user.identity = 'vip'
                    request.session['identity'] = user.identity
                    request.session.save()
                    user.session_key = request.session.session_key
                    user.save()
                    return JsonResponse({'count': 0, 'status': 0, 'wrong_msg': ''})
                else:
                    if user.login_time.strftime('%Y%m%d') == timezone.now().strftime('%Y%m%d'):
                        if(user.wrong_count >= 5):
                            return JsonResponse({'count': user.wrong_count + 1, 'status': 3, 'wrong_msg': '今天已输错' + (str)(user.wrong_count + 1) + '次密码，请明天再试'})
                    else:
                        user.wrong_count = 1
                        user.save()
                    return JsonResponse({'count': 1, 'status': 3, 'wrong_msg': '密码错误'})
            else:
                return JsonResponse({'count': 0, 'status': 4, 'wrong_msg': '您已被封号'})
        except:
            return JsonResponse({'status': 2, 'wrong_msg': '用户不存在'})

    def get(self, request):
        if request.session.get('is_login', None):
            request.session.flush()
            return JsonResponse(msg_dict.success)
        else:
            return JsonResponse(msg_dict.unknown)


class Member(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'time'}:
            return JsonResponse(msg_dict.missing)

        try:    # Todo:打钱？
            user = User.objects.get(id=request.session['uid'])
            if user.vip_time <= timezone.now():
                user.vip_time = AddYearOrMonth(timezone.now(), 0, kwargs.time)
                user.identity = 'vip'
                user.save()
                request.session['identity'] = 'vip'
                request.save()
            else:
                user.vip_time = AddYearOrMonth(user.vip_time, 0, kwargs.time)
                user.save()
            return JsonResponse(msg_dict.success)
        except:
            return JsonResponse(msg_dict.unknown)

    def get(self, request):
        try:
            user = User.objects.get(id=request.session['uid'])
            if user.vip_time > timezone.now():
                user.identity = 'user'
                user.save()
                return JsonResponse({'date': '', 'is_member': False})
            else:
                return JsonResponse({'date': user.vip_time.strftime("%Y-%m-%d"), 'is_member': True})
        except:
            return JsonResponse({'date': '', 'is_member': False})


class UserInfo(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'sex', 'birthday', 'organization', 'job', 'introduction'}:
            return JsonResponse(msg_dict.missing)

        try:
            user = User.objects.get(id=request.session['uid'])
            user.name = kwargs.name     # Todo:printable字符检验？ @tky
            user.sex = kwargs.sex if kwargs.sex in ['0', '1', '2'] else '0'
            user.birthday = datetime.strptime(kwargs.birthday, "%Y-%m-%d")
            user.organization = kwargs.organization
            user.job = kwargs.job
            user.intro = kwargs.introduction
            user.save()
            return JsonResponse(msg_dict.success)
        except:
            return JsonResponse(msg_dict.unknown)

    def get(self, request):
        try:
            user = User.objects.get(id=request.session['uid'])
            return JsonResponse(UserInfoJson(user).pack())
        except:
            return JsonResponse({})


class UserAccount(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'email', 'password'}:
            return JsonResponse(msg_dict.missing)

        try:
            user = User.objects.get(id=request.session['uid'])
            User.objects.get(email=kwargs.email)
            if ValidEmail(kwargs.email) and not User.objects.filter(email=kwargs.email).exists():
                if user.password == HashPassword(kwargs.password):
                    # Todo:邮箱验证
                    user.email = kwargs.email
                    user.save()
                    return JsonResponse(msg_dict.success)
                else:
                    return JsonResponse({'status': 1, 'wrong_msg': '密码错误'})
            elif User.objects.filter(email=kwargs.email).exists():
                return JsonResponse({'status': 3, 'wrong_msg': '账号已存在'})
            else:
                return JsonResponse({'status': 2, 'wrong_msg': '账号非法'})
        except:
            return JsonResponse(msg_dict.unknown)


class UserPassword(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'old_password', 'new_password'}:
            return JsonResponse(msg_dict.missing)

        try:
            user = User.objects.get(id=request.session['uid'])
            if user.password == HashPassword(kwargs.old_password):
                if ValidPassword(kwargs.new_password):
                    user.password = kwargs.password
                    user.save()
                    return JsonResponse(msg_dict.success)
                else:
                    return JsonResponse({'status': 3, 'wrong_msg': '新密码不合法'})
            else:
                return JsonResponse({'status': 1, 'wrong_msg': '旧密码错误'})
        except:
            return JsonResponse(msg_dict.unknown)