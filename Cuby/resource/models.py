from django.db import models


class Comment(models.Model):
    author = models.ForeignKey("User", related_name="comment_author", on_delete=models.CASCADE())
    article = models.ForeignKey("Atc", related_name="comment_article", on_delete=models.CASCADE())
    content = models.CharField(verbose_name="评论内容", max_length=512)
    likes = models.IntegerField(verbose_name="点赞量")
    stars = models.IntegerField(verbose_name="收藏量")
    reported = models.BooleanField(verbose_name="举报状态")


class Resource(models.Model):

    title = models.CharField(verbose_name="标题", max_length=256)
    description = models.CharField(verbose_name="描述", max_length=256)
    file_path = models.CharField(verbose_name="资源路径", max_length=256)
    file_size = models.CharField(verbose_name="大小", max_length=256)
    views = models.IntegerField(verbose_name="阅读量")
    stars = models.IntegerField(verbose_name="收藏量")
    likes = models.IntegerField(verbose_name="点赞量")
    points = models.IntegerField(verbose_name="所需积分")
    upload_time = models.DateTimeField(verbose_name='上传时间', auto_now_add=True)
    fix_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    author_name = models.ForeignKey("User", related_name="article_author", on_delete=models.CASCADE())
    reported = models.BooleanField(verbose_name="举报状态")

