from datetime import date, datetime
from django.db import models
from user.hypers import *


class User(models.Model):
    # basic fields
    tel = models.CharField(null=True, unique=True, verbose_name='电话', max_length=BASIC_MAX_LEN)
    email = models.EmailField(null=True, unique=True, verbose_name='邮箱', max_length=BASIC_MAX_LEN)
    password = models.CharField(verbose_name='密码', max_length=BASIC_MAX_LEN)
    name = models.CharField(verbose_name='姓名', max_length=BASIC_MAX_LEN)
    
    # mini fields
    gender = models.CharField(blank=True, verbose_name='性别', max_length=MINI_MAX_LEN, choices=GENDER_CHS, default='unknown')
    identity = models.CharField(blank=True, verbose_name='身份', max_length=MINI_MAX_LEN, choices=IDENTITY_CHS, default='user')
    
    # extended fields
    intro = models.CharField(blank=True, verbose_name='简介', max_length=EXT_MAX_LEN, default='')
    position = models.CharField(blank=True, verbose_name='职位', max_length=EXT_MAX_LEN, default='')
    organization = models.CharField(blank=True, verbose_name='公司或学校', max_length=EXT_MAX_LEN, default='')
    session_key = models.CharField(blank=True, verbose_name='session键', max_length=EXT_MAX_LEN, default='')
    
    # other fields
    login_date = models.DateField(blank=True, verbose_name='最近登录时间', auto_now=True)
    wrong_count = models.IntegerField(blank=True, verbose_name='最近一天密码错误次数', default=0)
    vip_date = models.DateField(blank=True, verbose_name='会员到期时间', default=date(1900, 1, 1))
    create_time = models.DateTimeField(blank=True, verbose_name='创建时间', auto_now_add=True)
    blocked = models.BooleanField(blank=True, verbose_name='被封禁', default=False)
    birthday = models.DateField(blank=True, verbose_name='生日', default=date(1900, 1, 1))
    filesize = models.IntegerField(blank=True, verbose_name='上传资源总大小', default=0)
    favourite_articles = models.ManyToManyField(blank=True, to='article.Article')
    favourite_resources = models.ManyToManyField(blank=True, to='resource.Resource')
    followings = models.ManyToManyField(blank=True, to='self')
    followers = models.ManyToManyField(blank=True, to='self')
    point = models.IntegerField(blank=True, verbose_name='积分', default=0)
    profile_photo = models.FileField(blank=True, verbose_name='头像', upload_to='img/profile_photo',
                                     default='img/profile_photo/default_handsome.jpg')

    def verify_vip(self) -> bool:
        if self.vip_date < date.today():
            self.identity = 'user'
            self.save()
        return self.identity == 'user'
# class Detail(models.Model):
#     point = models.IntegerField(verbose_name="积分变动", default=0)
#     reason = models.CharField(verbose_name="理由", max_length=256)
#     time = models.DateTimeField(verbose_name="时间", auto_now_add=True)
#     owner = models.ForeignKey('user.User', on_delete=models.CASCADE)
