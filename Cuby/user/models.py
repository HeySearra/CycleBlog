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
        ('unknown', '未知'),
        ('male', '男'),
        ('female', '女'),
    )
    identity_chs = (
        ('user', '普通用户'),
        ('vip', '会员'),
        ('admin', '管理员'),
    )
    
    # basis
    # account = models.CharField(verbose_name='帐号', max_length=BASIS_MAX_LEN)  # todo: 超过max_length会怎么样？
    email = models.EmailField(blank=True, verbose_name='邮箱', validators=[validate_email])
    # telephone = models.CharField(blank=True, verbose_name='电话', max_length=BASIS_MAX_LEN, validators=[LambdaValidator(
    #     lambda tele: len(tele) == TELE_LEN and all(c.isnumeric() for c in tele)
    # )])
    password = models.CharField(verbose_name='密码', max_length=BASIS_MAX_LEN)
    name = models.CharField(verbose_name='姓名', max_length=BASIS_MAX_LEN)
    
    # mini
    gender = models.CharField(blank=True, verbose_name='性别', max_length=MINI_MAX_LEN, choices=gender_chs, default='unknown')
    identity = models.CharField(blank=True, verbose_name='身份', max_length=MINI_MAX_LEN, choices=identity_chs, default='user')
    position = models.CharField(blank=True, verbose_name='职位', max_length=MINI_MAX_LEN)
    
    # intro
    intro = models.CharField(blank=True, verbose_name='简介', max_length=INTRO_MAX_LEN)
    organization = models.CharField(blank=True, verbose_name='公司或学校', max_length=INTRO_MAX_LEN)
    
    # others
    create_time = models.DateTimeField(blank=True, verbose_name='创建时间', auto_now_add=True)
    blocked = models.BooleanField(blank=True, verbose_name='被封禁', default=False)
    birthday = models.DateField(blank=True, verbose_name='生日')
    filesize = models.IntegerField(blank=True, verbose_name='上传资源总大小')
    favourite_articles = models.ManyToManyField(blank=True, to='article.Article')  # todo: ManyToManyField是null=True还是blank=True？
    favourite_resources = models.ManyToManyField(blank=True, to='resource.Resource')
    followings = models.ManyToManyField(blank=True, to='self')
    followers = models.ManyToManyField(blank=True, to='self')
    point = models.IntegerField(verbose_name='积分', default=0)


class Detail(models.Model):
    point = models.IntegerField(verbose_name="积分变动", default=0)
    reason = models.CharField(verbose_name="理由", max_length=256)
    time = models.DateTimeField(verbose_name="时间", auto_now_add=True)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)
