from django.db import models
from article.models import Tag


class Resource(models.Model):
    title = models.CharField(verbose_name="标题", max_length=256, default='')
    description = models.CharField(blank=True, verbose_name="描述", max_length=256, default='')
    file_path = models.FileField(blank=True, verbose_name="资源路径", max_length=256, default='')
    file_size = models.CharField(blank=True, verbose_name="大小", max_length=256, default='')
    views = models.IntegerField(blank=True, verbose_name="阅读量", default=0)
    stars = models.IntegerField(blank=True, verbose_name="收藏量", default=0)
    likes = models.IntegerField(blank=True, verbose_name="点赞量", default=0)
    points = models.IntegerField(blank=True, verbose_name="所需积分", default=0)
    create_time = models.DateTimeField(blank=True, verbose_name='上传时间', auto_now_add=True)
    edit_time = models.DateTimeField(blank=True, verbose_name='修改时间', auto_now=True)
    blocked = models.BooleanField(blank=True, verbose_name='被封禁', default=False)

    tags = models.ManyToManyField(Tag, related_name='tagged_resources')
    author = models.ForeignKey(null=True, to='user.User', related_name="resource_author", on_delete=models.CASCADE)
    who_like = models.ManyToManyField('user.User', verbose_name='like_person')  # 被谁点赞


class ResourceComment(models.Model):
    content = models.CharField(verbose_name="内容", max_length=512, default='')
    likes = models.IntegerField(blank=True, verbose_name="点赞量", default=0)
    blocked = models.BooleanField(verbose_name='被封禁', default=False)

    author = models.ForeignKey(null=True, to="user.User", related_name="resource_comment_author", on_delete=models.CASCADE)
    fa_resources = models.ForeignKey(null=True, to=Resource, related_name="comment_resource", on_delete=models.CASCADE)
    who_like = models.ManyToManyField('user.User', verbose_name='like_person')


class Message(models.Model):
    # 它的功能是举报
    content = models.CharField(verbose_name="举报理由", max_length=512, default='')
    condition = models.BooleanField(verbose_name='被处理', default=False)

    owner = models.ForeignKey('user.User', related_name='message_owner', verbose_name="举报者", on_delete=models.CASCADE)
    handler = models.ForeignKey('user.User', related_name='message_handler', verbose_name="处理者", on_delete=models.CASCADE)

    article = models.ForeignKey('article.Article', null=True, on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource', null=True, on_delete=models.CASCADE)
    article_comment = models.ForeignKey('article.ArticleComment', null=True, on_delete=models.CASCADE)
    resource_comment = models.ForeignKey('ResourceComment', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', null=True, on_delete=models.CASCADE)


class Download(models.Model):
    owner = models.ForeignKey('user.User', related_name='download_owner', on_delete=models.CASCADE)
    resources = models.ManyToManyField('resource.Resource', through='DownloadMembership')


class DownloadMembership(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    download = models.ForeignKey('Download', on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE)
