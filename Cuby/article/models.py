from django.db import models


class Article(models.Model):
    title = models.CharField(verbose_name="标题", max_length=256)
    abstract = models.CharField(verbose_name="摘要", max_length=256)
    content = models.TextField(verbose_name="全文")
    tag = models.CharField(verbose_name="标签集合", max_length=512)
    # column = models.CharField(verbose_name="专栏", max_length=256)  # todo: Column里面已经多对多了，现在还要么？
    views = models.IntegerField(verbose_name="阅读量")
    stars = models.IntegerField(verbose_name="收藏量")
    likes = models.IntegerField(verbose_name="点赞量")
    url = models.CharField(verbose_name="文章url", max_length=256)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    edit_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    author_name = models.ForeignKey('user.User', related_name="article_author", on_delete=models.CASCADE)


class Column(models.Model):
    title = models.CharField(verbose_name="专栏名称", max_length=256)
    views = models.IntegerField(verbose_name="阅读量")
    article_num = models.IntegerField(verbose_name="文章数量")
    articles = models.ManyToManyField(Article, related_name='articles_in_column')


class Tag(models.Model):
    name = models.CharField(verbose_name="标签名", max_length=256)
    article_num = models.IntegerField(verbose_name="标签下文章的数量")
    articles = models.ManyToManyField(Article, related_name='tagged_articles')
