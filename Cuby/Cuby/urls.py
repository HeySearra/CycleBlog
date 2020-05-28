"""Cuby URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from user.views import *
from resource.views import *
from article.views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    # 他本来就是从完整的url了，前面加/会报warning
    path('register/submit', Register.as_view(), name='register'),
    path('login/submit', Login.as_view(), name='login'),
    path('simple_user_info', UserInfo.as_view(), name='simple_user_info'),
    path('member/apply', Member.as_view(), name='vip'),
    path('user/', include([
        path('change_account', ChangeAccount.as_view(), name='user_account'),
        path('change_password', ChangePassword.as_view(), name='user_password'),
    ])),
    path('create/resource', include([
        path('upload_limit', GetUploadLimit.as_view(), name='upload_limit'),
        path('upload_file', UploadFile.as_view(), name='uploadfile'),
        path('new', EditFileMessage.as_view(), name='edit_file_message'),
        path('upload_list', GetResource.as_view(), name='get_resource'),
        path('download_list', GetDownload.as_view(), name='get_download'),
        path('delete', DelResource.as_view(), name='del_resource'),
    ])),
    path('edit/submit', SubmitArticle.as_view()),
    path('create/', include([
        path('follow', FollowList.as_view(), name='follow_list'),
        path('fan', FanList.as_view(), name='fan_list'),
    ])),
    path('data/', include([
        path('follows_and_fans', DataFF.as_view()),
    ])),
    path('collection/', include([
        path('list', GetClist.as_view(), name='get_collection_list'),
        path('info', GetCinfo.as_view(), name='get_collection_info'),
        path('add_article', CollectArticle.as_view(), name='add_article'),
        path('add_resource', CollectResource.as_view(), name='add_resource'),
        path('remove_article', RemoveArticleFromCollection.as_view(), name='remove_article'),
        path('remove_resource', RemoveResourceFromCollection.as_view(), name='remove_resource'),
        path('new', NewCollection.as_view(), name='new_collection'),
        path('rename', Rename.as_view(), name='rename_collection'),
        path('condition', SetCondition.as_view(), name='change_condition'),
        path('delete', DelCollection.as_view(), name='delete_collection'),
        path('move_article', MoveArticle.as_view(), name='move_article'),
        path('move_resource', MoveResource, name='move_resource'),
    ])),
    re_path(r'.*', TemplateView.as_view(template_name='index.html')),
]
