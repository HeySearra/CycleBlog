# Generated by Django 3.0.3 on 2020-06-08 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='view_week',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='最近一周浏览量'),
        ),
    ]