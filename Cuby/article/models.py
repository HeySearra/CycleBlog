from django.db import models


class Column(models.Model):
    title = models.CharField(blank=True, verbose_name="专栏名称", max_length=256, default='')
    views = models.IntegerField(blank=True, verbose_name="阅读量", default=0)  # 专栏下所有文章浏览量的和
    article_num = models.IntegerField(blank=True, verbose_name="文章数量", default=0)
    
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(verbose_name="标签名", max_length=256, default='')
    article_num = models.IntegerField(verbose_name="标签下文章的数量", default=0)
    resource_num = models.IntegerField(verbose_name="标签下资源的数量", default=0)


class Collection(models.Model):
    name = models.CharField(verbose_name="收藏夹名", max_length=256, default='')
    totalnum = models.IntegerField(verbose_name="收藏内容数量", default=0)
    hide = models.BooleanField(verbose_name='是否隐藏', default=False)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)

    articles = models.ManyToManyField('Article', verbose_name='收藏的文章',  related_name='articles_in_collection', through='ArticleCollect')
    resources = models.ManyToManyField('resource.Resource', verbose_name='收藏的资源', related_name='resources_in_collection', through='ResourceCollect')


class ArticleCollect(models.Model):
    time = models.DateTimeField(verbose_name='收藏时间', auto_now_add=True)

    user = models.ForeignKey('Collection', on_delete=models.CASCADE)
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE)


class ResourceCollect(models.Model):
    time = models.DateTimeField(verbose_name='收藏时间', auto_now_add=True)

    user = models.ForeignKey('Collection', on_delete=models.CASCADE)
    resource = models.ForeignKey('resource.Resource', on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField(verbose_name="标题", max_length=256, default='')
    abstract = models.CharField(verbose_name="摘要", max_length=256, default='')
    content = models.TextField(verbose_name="全文", default='')
    views = models.IntegerField(verbose_name="阅读量", default=0)
    stars = models.IntegerField(verbose_name="收藏量", default=0)
    likes = models.IntegerField(verbose_name="点赞量", default=0)
    url = models.CharField(verbose_name="文章url", max_length=256, default='')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    edit_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    recycle_time = models.DateTimeField(verbose_name="删除时间", null=True)
    blocked = models.BooleanField(blank=True, verbose_name='被封禁', default=False)
    recycled = models.BooleanField(blank=True, verbose_name='在回收站里', default=False)
    
    author = models.ForeignKey('user.User', related_name="article_author", on_delete=models.CASCADE)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='article_tag')
    who_like = models.ManyToManyField('user.User', verbose_name='like_person')  # 被谁点赞


class ArticleComment(models.Model):
    content = models.CharField(verbose_name="内容", max_length=512, default='')
    likes = models.IntegerField(blank=True, verbose_name="点赞量", default=0)
    blocked = models.BooleanField(verbose_name='被封禁', default=False)

    author = models.ForeignKey(null=True, to="user.User", related_name="article_comment_author", on_delete=models.CASCADE)
    fa_article = models.ForeignKey(null=True, to="Article", related_name="comment_article", on_delete=models.CASCADE)
    who_like = models.ManyToManyField('user.User', verbose_name='like_person')