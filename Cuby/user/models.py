from datetime import date, datetime
from django.db import models
from django.core.validators import validate_email

from utils.validator import LambdaValidator

MINI_MAX_LEN = 32
BASIS_MAX_LEN = 64
INTRO_MAX_LEN = 256
TELE_LEN = 11


class User(models.Model):
    # choices
    gender_chs = (
        ('0', '未知'),
        ('1', '男'),
        ('2', '女'),
    )
    identity_chs = (
        ('user', '普通用户'),
        ('vip', '会员'),
        ('admin', '管理员'),
    )
    
    # basis
    # account = models.CharField(verbose_name='帐号', max_length=BASIS_MAX_LEN)  # todo: 超过max_length会怎么样？
    email = models.EmailField(unique=True, verbose_name='邮箱', validators=[validate_email])
    # telephone = models.CharField(blank=True, verbose_name='电话', max_length=BASIS_MAX_LEN, validators=[LambdaValidator(
    #     lambda tele: len(tele) == TELE_LEN and all(c.isnumeric() for c in tele)
    # )])
    # password = models.CharField(verbose_name='密码', max_length=BASIS_MAX_LEN, validators=[LambdaValidator(
    #     lambda pwd: all([
    #         6 <= len(pwd) <= 32,
    #         all(ord('!') <= ord(c) <= ord('~') for c in pwd),
    #         any(c.isupper() for c in pwd)
    #         + any(c.islower() for c in pwd)
    #         + any(c.isnumeric() for c in pwd)
    #         + any(not c.isalnum() for c in pwd)
    #         >= 2
    #     ]),
    # )])
    password = models.CharField(verbose_name='密码', max_length=BASIS_MAX_LEN)
    # name = models.CharField(verbose_name='姓名', max_length=BASIS_MAX_LEN, validators=[LambdaValidator(
    #     lambda nm: all([
    #         0 < len(nm) <= 32,
    #         all(c.isprintable() for c in nm)
    #     ])
    # )])
    name = models.CharField(verbose_name='姓名', max_length=BASIS_MAX_LEN)
    
    # mini
    gender = models.CharField(blank=True, verbose_name='性别', max_length=MINI_MAX_LEN, choices=gender_chs, default='unknown')
    identity = models.CharField(blank=True, verbose_name='身份', max_length=MINI_MAX_LEN, choices=identity_chs, default='user')
    position = models.CharField(blank=True, verbose_name='职位', max_length=MINI_MAX_LEN)
    
    # intro
    intro = models.CharField(blank=True, verbose_name='简介', max_length=INTRO_MAX_LEN)
    organization = models.CharField(blank=True, verbose_name='公司或学校', max_length=INTRO_MAX_LEN)
    
    # others
    session_key = models.CharField(blank=True, max_length=256)
    login_time = models.DateField(blank=True, verbose_name='最近登录时间', auto_now=True)
    wrong_count = models.IntegerField(verbose_name='最近一天密码错误次数', default=0)
    vip_time = models.DateField(verbose_name='会员到期时间', auto_now_add=True)
    create_time = models.DateTimeField(blank=True, verbose_name='创建时间', auto_now_add=True)
    blocked = models.BooleanField(blank=True, verbose_name='被封禁', default=False)
    birthday = models.DateField(blank=True, verbose_name='生日', default=date(1900, 1, 1))
    filesize = models.IntegerField(blank=True, verbose_name='上传资源总大小', default=0)
    followings = models.ManyToManyField(blank=True, to='self')
    followers = models.ManyToManyField(blank=True, to='self')
    point = models.IntegerField(verbose_name='积分', default=0)
    profile_photo = models.FileField(blank=True, verbose_name='头像', upload_to='img/profile_photo',
                                     default='img/profile_photo/default_handsome.jpg')


class Detail(models.Model):
    point = models.IntegerField(verbose_name="积分变动", default=0)
    reason = models.CharField(verbose_name="理由", max_length=256)
    time = models.DateTimeField(verbose_name="时间", auto_now_add=True)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)

