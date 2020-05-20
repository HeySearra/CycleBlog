from django.db import models
from login.models import User
import sys
# Create your models here.



class Comment(models.Model):
    comment_to = models.ForeignKey('login.User', on_delete=models.CASCADE)
    content = models.CharField(verbose_name="文章全文代码", max_length=512)
    likes = models.IntegerField(verbose_name="点赞量")


class Atc(models.Model):

    title = models.CharField(verbose_name="标题", max_length=256)
    content = models.TextField(verbose_name="文章全文代码")
    simple_content = models.CharField(verbose_name="文章前200字内容", max_length=256)
    views = models.IntegerField(verbose_name="阅读量")
    stars = models.IntegerField(verbose_name="收藏量")
    likes = models.IntegerField(verbose_name="点赞量")
    tag = models.CharField(verbose_name="文章的标签", max_length=256)
    column = models.CharField(verbose_name="文章的专栏", max_length=256)
    url = models.CharField(verbose_name="前往文章的url", max_length=256)
    edit_year = models.IntegerField(verbose_name="文章最近修改时间：年")
    edit_month = models.IntegerField(verbose_name="文章最近修改时间：月")
    edit_day = models.IntegerField(verbose_name="文章最近修改时间：日")
    edit_hour = models.IntegerField(verbose_name="文章最近修改时间：时")
    edit_minute = models.IntegerField(verbose_name="文章最近修改时间：分")
    edit_second = models.IntegerField(verbose_name="文章最近修改时间：秒")
    author_name = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name="article_author")


class Tag(models.Model):
    name = models.CharField(verbose_name="标签名", max_length=256)
    article_num = models.IntegerField(verbose_name="标签下文章的数量")
    articles = models.ManyToManyField(Atc)


class Column(models.Model):
    title = models.CharField(verbose_name="专栏名称", max_length=256)
    views = models.IntegerField(verbose_name="阅读量")
    article_num = models.IntegerField(verbose_name="专栏下文章的数量")
    articles = models.ManyToManyField(Atc)