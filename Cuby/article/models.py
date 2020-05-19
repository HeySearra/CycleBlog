from django.db import models
import sys
# Create your models here.


class Tag(models.Model):
    name = models.CharField(verbose_name="标签名", max_length=256)
    article_num = models.IntegerField(verbose_name="标签下文章的数量")
    articles = models.ManyToManyField("Atc")


class Column(models.Model):
    title = models.CharField(verbose_name="专栏名称", max_length=256)
    views = models.IntegerField(verbose_name="阅读量")
    article_num = models.IntegerField(verbose_name="专栏下文章的数量")
    articles = models.ManyToManyField("Atc")


class Comment(models.Model):
    comment_to = models.ForeignKey("User", related_name="comment_author", on_delete=models.CASCADE())
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
    edit_year = models.IntegerField(verbose_name="文章最近修改时间：年", max_length=256)
    edit_month = models.IntegerField(verbose_name="文章最近修改时间：月", max_length=256)
    edit_day = models.IntegerField(verbose_name="文章最近修改时间：日", max_length=256)
    edit_hour = models.IntegerField(verbose_name="文章最近修改时间：时", max_length=256)
    edit_minute = models.IntegerField(verbose_name="文章最近修改时间：分", max_length=256)
    edit_second = models.IntegerField(verbose_name="文章最近修改时间：秒", max_length=256)
    author_name = models.ForeignKey("User", related_name="article_author", on_delete=models.CASCADE())
