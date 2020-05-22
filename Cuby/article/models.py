from django.db import models


class Column(models.Model):
    title = models.CharField(verbose_name="专栏名称", max_length=256)
    views = models.IntegerField(verbose_name="阅读量")     # 专栏下所有文章浏览量的和
    article_num = models.IntegerField(verbose_name="文章数量")

    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(verbose_name="标签名", max_length=256)
    article_num = models.IntegerField(verbose_name="标签下文章的数量", default=0)
    resource_num = models.IntegerField(verbose_name="标签下资源的数量", default=0)


class Collection(models.Model):
    name = models.CharField(verbose_name="收藏夹名", max_length=256)
    source_num = models.IntegerField(verbose_name="收藏内容数量", default=0)

    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField(verbose_name="标题", max_length=256)
    abstract = models.CharField(verbose_name="摘要", max_length=256)
    content = models.TextField(verbose_name="全文")
    tag = models.CharField(verbose_name="标签集合", max_length=512)
    views = models.IntegerField(verbose_name="阅读量")
    stars = models.IntegerField(verbose_name="收藏量")
    likes = models.IntegerField(verbose_name="点赞量")
    url = models.CharField(verbose_name="文章url", max_length=256)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    edit_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    recycle_time = models.DateTimeField(verbose_name="删除时间", null=True)
    blocked = models.BooleanField(blank=True, verbose_name='被封禁', default=False)
    recycled = models.BooleanField(blank=True, verbose_name='在回收站里', default=False)

    author = models.ForeignKey('user.User', related_name="article_author", on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='article_tag')
    who_like = models.ManyToManyField('user.User', verbose_name='like_person')  # 被谁点赞
    collection = models.ManyToManyField(Collection)     # 被谁收藏



