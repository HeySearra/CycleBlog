import json

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from easydict import EasyDict
from django.views import View
from django.db.utils import IntegrityError, DataError

from user.models import User
from user.hypers import *
from utils.response import JSR


class Register(View):
    @JSR('status')
    def post(self, request):
        E = EasyDict()
        E.uk = -1
        E.acc, E.pwd, E.name, E.uni = 1, 2, 3, 4
        
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'password', 'name'}:
            return E.uk
        if not CHECK_ACC(kwargs['account']):
            return E.acc
        if not CHECK_PWD(kwargs['password']):
            return E.pwd
        if not CHECK_NAME(kwargs['name']):
            return E.name
        
        kwargs.update({'email' if '@' in kwargs['account'] else 'tel': kwargs['account']})
        kwargs.pop('account')
        
        u = User(**kwargs)
        try:
            u.save()
        except IntegrityError:
            return E.uni  # 字段unique未满足
        except DataError:
            return E.uk  # 诸如某个CharField超过了max_len的错误
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
        E.exist, E.pwd, E.max_wrong, E.block = 1, 2, 3, 4
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'password'}:
            return 0, E.uk
        
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
        E.exist = 1
        
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'time'}:
            return E.uk
        
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
    @JSR('status')
    def post(self, request):
        E = EasyDict()
        E.uk = -1
        E.name, E.org, E.job, E.intro = 1, 2, 3, 4
        
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'sex', 'birthday', 'organization', 'job', 'introduction'}:
            return E.uk
        
        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return E.uk
        u = u.get()
        
        if not CHECK_NAME(kwargs['name']):
            return E.name
        if str(kwargs['sex']) not in GENDER_DICT.keys():
            return E.uk
        if not CHECK_DESCS(kwargs['organization']):
            return E.org
        if not CHECK_DESCS(kwargs['job']):
            return E.job
        if not CHECK_DESCS(kwargs['introduction']):
            return E.intro
        
        u.name = kwargs['name']
        u.sex = GENDER_DICT[str(kwargs['sex'])]
        u.birthday = datetime.strptime(kwargs['birthday'], '%Y-%m-%d').date()
        u.organization = kwargs['organization']
        u.job = kwargs['job']
        u.intro = kwargs['introduction']
        
        try:
            u.save()
        except:
            return E.uk
        return 0
    
    @JSR('uid', 'name', 'sex', 'birthday', 'organization', 'job', 'introduction')
    def get(self, request):
        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return tuple([''] * 6)
        u = u.get()
        return u.id, u.name, u.gender, u.birthday.strftime('%Y-%m-%d'), u.organization, u.job, u.intro


class ChangeAccount(View):
    @JSR('status')
    def post(self, request):
        E = EasyDict()
        E.uk = -1
        E.pwd, E.acc, E.exist = 1, 2, 3
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'password'}:
            return E.uk
        
        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return E.uk
        u = u.get()

        if not CHECK_ACC(kwargs['account']):
            return E.acc
        if u.password != kwargs['password']:
            return E.pwd
        
        attr = 'email' if '@' in kwargs['account'] else 'tel'
        if User.objects.filter(**{attr: kwargs['account']}).exists():
            return E.exist
        setattr(u, attr, kwargs['account'])
        try:
            u.save()
        except:
            return E.uk
        return 0


class ChangePassword(View):
    @JSR('status')
    def post(self, request):
        E = EasyDict()
        E.uk = -1
        E.wr_pwd, E.same_pwd, E.ill_pwd = 1, 2, 3
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'old_password', 'new_password'}:
            return E.uk

        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return E.uk
        u = u.get()
    
        if kwargs['old_password'] != u.password:
            return E.wr_pwd
        if kwargs['old_password'] == kwargs['new_password']:
            return E.same_pwd
        if not CHECK_PWD(kwargs['new_password']):
            return E.ill_pwd
        
        u.password = kwargs['new_password']
        try:
            u.save()
        except:
            return E.uk
        return 0


class FollowList(View):
    @JSR('uid', 'amount')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'page', 'each'}:
            return [], 0

        list = []
        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return list, 0
        u = u.get()

        page = int(kwargs['page'])
        each = int(kwargs['each'])
        follow_set = u.followings.all()[(page - 1) * each: page * each]
        for u in follow_set:
            list.append(u.id)
        return list, len(list)

    @JSR('status')
    def get(self, request):
        # 关注或取关
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'uid', 'condition'}:
            return -1

        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return -1
        u = u.get()

        uf = User.objects.filter(id=int(kwargs['uid']))
        if not uf.exists():
            return 0

        if u.followings.filter(id=int(kwargs['uid'])).exists():
            u.followings.remove(uf)
        else:
            u.followings.add(uf)
        return 0


class FanList(View):
    @JSR('uid', 'status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'page', 'each'}:
            return [], 0

        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return [], 0
        u = u.get()

        list = []
        page = int(kwargs['page'])
        each = int(kwargs['each'])
        follow_set = u.followers.all()[(page - 1) * each: page * each]
        for u in follow_set:
            list.append(u.id)
        return list, len(list)


class DataFF(View):
    @JSR('fans', 'followings')
    def get(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'uid'}:
            return 0, 0

        u = User.objects.filter(id=int(kwargs['uid']))
        if not u.exists():
            return 0, 0
        u = u.get()
        return u.followers.count(), u.followings.count()
