# Generated by Django 3.0.3 on 2020-06-04 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0001_initial'),
        ('user', '0001_initial'),
        ('resource', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCollect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256, verbose_name='收藏夹名')),
                ('total_num', models.IntegerField(default=0, verbose_name='收藏内容数量')),
                ('hide', models.BooleanField(default=False, verbose_name='是否隐藏')),
                ('articles', models.ManyToManyField(related_name='articles_in_collection', through='mainpage.ArticleCollect', to='article.Article', verbose_name='收藏的文章')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=256, verbose_name='标签名')),
                ('article', models.ManyToManyField(related_name='tagged_article', to='article.Article')),
                ('resource', models.ManyToManyField(related_name='tagged_resources', to='resource.Resource')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceCollect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resource.Resource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.BooleanField(default=False)),
                ('message', models.CharField(default='', max_length=512, verbose_name='消息内容')),
                ('article_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_comment', to='article.ArticleComment')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_owner', to='user.User')),
                ('resource_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resource_comment', to='resource.ResourceComment')),
            ],
        ),
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=512, verbose_name='举报理由')),
                ('condition', models.BooleanField(default=False, verbose_name='被处理')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Article')),
                ('article_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.ArticleComment')),
                ('handler', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complain_handler', to='user.User', verbose_name='处理者')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complain_owner', to='user.User', verbose_name='举报者')),
                ('resource', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resource.Resource')),
                ('resource_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resource.ResourceComment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='resources',
            field=models.ManyToManyField(related_name='resources_in_collection', through='mainpage.ResourceCollect', to='resource.Resource', verbose_name='收藏的资源'),
        ),
        migrations.AddField(
            model_name='articlecollect',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.Collection'),
        ),
    ]