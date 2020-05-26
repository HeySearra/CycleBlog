import json

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from easydict import EasyDict
from django.http import JsonResponse
from django.views import View
from user.models import User
from user.hypers import *
from utils.jsonpack import UserInfoJson
from utils.response import dict_jsr, JSR
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
    @JSR('status')
    def post(self, request):
        E = EasyDict()
        E.uk = -1
        E.key, E.acc, E.pwd, E.name, E.uni = 1, 2, 3, 4, 5
        
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
        except:
            return E.uk
        return 0


class Login(View):
    @JSR('count', 'status')
    def post(self, request):
        if request.session.get('is_login', None):
            return 0, 0
        
        E = EasyDict()
        E.uk = -1
        E.key, E.exist, E.pwd, E.max_wrong, E.block = 1, 2, 3, 4, 5
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'password'}:
            return 0, E.key
        
        u = (User.objects.filter(email=kwargs['account']) if '@' in kwargs['account']
             else User.objects.filter(tel=kwargs['account']))
        if not u.exists():
            return 0, E.exist
        u = u.get()

        if u.login_date != date.today():
            u.login_date = date.today()
            u.wrong_count = 0
            try:
                u.save()
            except:
                return u.wrong_count, E.uk

        if u.blocked:
            return u.wrong_count, E.block
        
        if u.wrong_count == MAX_WRONG_PWD:
            return u.wrong_count, E.max_wrong
        
        if u.password != kwargs['password']:
            u.wrong_count += 1
            return u.wrong_count, E.pwd
        
        u.verify_vip()
        request.session['is_login'] = True
        request.session['uid'] = u.id
        request.session['name'] = u.name
        request.session['identity'] = u.identity
        request.session.save()
        u.session_key = request.session.session_key
        try:
            u.save()
        except:
            return u.wrong_count, E.uk
        return u.wrong_count, 0
    
    @JSR('status')
    def get(self, request):
        if request.session.get('is_login', None):
            request.session.flush()
            return 0
        else:
            return -1


class Member(View):
    @JSR('status')
    def post(self, request):
        E = EasyDict()
        E.uk = -1
        E.key, E.exist = 1, 2

        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'time'}:
            return E.key

        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return E.exist
        u = u.get()
        
        if u.vip_time < date.today():
            u.vip_time = date.today()
        u.vip_time = u.vip_time + relativedelta(months=int(kwargs['time']))
        u.identity = 'vip'
        try:
            u.save()
        except:
            return E.uk
        request.session['identity'] = 'vip'
        request.save()
        return 0
    
    @JSR('date', 'is_member')
    def get(self, request):
        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return '', False
        u = u.get()
        is_vip = u.verify_vip()
        try:
            u.save()
        except:
            return '', False
        return u.vip_date.strftime("%Y-%m-%d") if is_vip else '', is_vip


class UserInfo(View):
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'sex', 'birthday', 'organization', 'job', 'introduction'}:
            return JsonResponse(msg_dict.missing)
        
        try:
            user = User.objects.get(id=request.session['uid'])
            user.name = kwargs.name  # Todo:printable字符检验？ @tky
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
