from django.db import models


class Resource(models.Model):
    title = models.CharField(verbose_name="标题", max_length=256)
    description = models.CharField(blank=True, verbose_name="描述", max_length=256)
    file_path = models.CharField(blank=True, verbose_name="资源路径", max_length=256)
    file_size = models.CharField(blank=True, verbose_name="大小", max_length=256)
    views = models.IntegerField(blank=True, verbose_name="阅读量", default=0)
    stars = models.IntegerField(blank=True, verbose_name="收藏量", default=0)
    likes = models.IntegerField(blank=True, verbose_name="点赞量", default=0)
    points = models.IntegerField(blank=True, verbose_name="所需积分", default=0)
    create_time = models.DateTimeField(blank=True, verbose_name='上传时间', auto_now_add=True)
    edit_time = models.DateTimeField(blank=True, verbose_name='修改时间', auto_now=True)
    blocked = models.BooleanField(blank=True, verbose_name='被封禁', default=False)

    author = models.ForeignKey(null=True, to='user.User', related_name="resource_author", on_delete=models.CASCADE)
    who_like = models.ManyToManyField('user.User', verbose_name='like_person')  # 被谁点赞
    collection = models.ManyToManyField('article.Collection')  # 被谁收藏


class Comment(models.Model):
    fa_author = models.ForeignKey(null=True, to="user.User", related_name="comment_author", on_delete=models.CASCADE)
    fa_article = models.ForeignKey(null=True, to="article.Article", related_name="comment_article", on_delete=models.CASCADE)
    fa_resources = models.ForeignKey(null=True, to=Resource, related_name="comment_article", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="内容", max_length=512)
    likes = models.IntegerField(blank=True, verbose_name="点赞量", default=0)
    stars = models.IntegerField(blank=True, verbose_name="收藏量", default=0)  # 评论被收藏？
    blocked = models.BooleanField(blank=True, verbose_name='被封禁', default=False)

    who_like = models.ManyToManyField('user.User', verbose_name='like_person')