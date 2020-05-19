from django.db import models

# Create your models here.


class User(models.Model):

    gender = (
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知'),
    )
    admin = (
        ('user', "普通用户"),
        ('vip', '会员'),
        ('admin', '管理员'),
    )

    account = models.CharField(verbose_name="帐号", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=256)
    name = models.CharField(verbose_name="姓名", max_length=128)
    intro = models.CharField(verbose_name="简介", max_length=512)
    birthday = models.DateField()
    organization = models.CharField(verbose_name="公司或学校", max_length=256)
    position = models.CharField(verbose_name="职位", max_length=256)
    sex = models.CharField(verbose_name="性别", max_length=32, choices=gender, default='unknown')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    profile_photo = models.FileField(verbose_name="头像", upload_to='img/profile_photo',
                                     default="img/profile_photo/default_handsome.jpg")
    auth = models.CharField(verbose_name="权限", max_length=128, choices=admin, default='student')
    follow = models.ManyToManyField('self')
    fan = models.ManyToManyField('self')
