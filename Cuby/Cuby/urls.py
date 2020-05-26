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
from resource.views import GetUploadLimit, UploadFile, EditFileMessage, GetResource, GetDownload, DelResource
from article.views import GetClist, GetCinfo, AddArticle, AddResource, RemoveArticle, RemoveResource, NewCollection, Rename, SetCondition, DelCollection, MoveArticle, MoveResource

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('logout/submit/'),
    # path('side/user_info/'),
    # path('base/', include([
    #     path('article_view/'),
    #     path('resource_view/'),
    # ])),
    # path('create/article/', include([
    #     path('list/'),
    #     path('article_edit'),
    #     path('delete/'),
    #     path('top/'),
    # ])),
    # path('edit/submit/'),
    # path('create/spacial/', include([
    #     path('list/'),
    #     path('info/'),
    #     path('info_for_edit/'),
    #     path('edit/'),
    #     path('rename/'),
    #     path('new/'),
    #     path('delete/'),
    # ])),
    # path('create/recycle/', include([
    #     path('list/'),
    #     path('article_recycle/'),
    #     path('recover/'),
    #     path('delete/'),
    # ])),
    # path('create/resource/', include([
    #     path('upload_limit/'),
    #     path('upload_file/'),
    #     path('new/'),
    #     path('upload_list/'),
    #     path('edit/'),
    #     path('download_list/'),
    #     path('delete/'),
    # ])),
    # path('create_point/', include([
    #     path('list/'),
    # ])),
    # path('create/data/', include([
    #     path(''),
    # ])),
    # path('collection/', include([
    #     path('list/'),
    #     path('info/'),
    #     path('add_article/'),
    #     path('add_resource/'),
    #     path('remove_article/'),
    #     path('remove_resource/'),
    #     path('new/'),
    #     path('rename/'),
    #     path('delete/'),
    #     path('move_article/'),
    #     path('move_resource/'),
    # ])),
    # path('article/', include([
    #
    # ])),
    # path('resource/', include([
    #     path('all/'),
    #     path('download/'),
    # ])),
    # path('comment/', include([
    #
    # ])),

    # 他本来就是从完整的url了，前面加/会报warning
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('register/submit', Register.as_view(), name='register'),
    path('login/submit', Login.as_view(), name='login'),
    path('member/apply/', Member.as_view(), name='vip'),
    path('user/', include([
        path('info/', UserInfo.as_view(), name='user_info'),
        path('change_account/', ChangeAccount.as_view(), name='user_account'),
        path('change_password/', ChangePassword.as_view(), name='user_password'),
    ])),
    path('create/resource/upload_limit', GetUploadLimit.as_view(), name='upload_limit'),
    path('create/resource/upload_file', UploadFile.as_view(), name='uploadfile'),
    path('create/resource/new', EditFileMessage.as_view(), name='edit_file_message'),
    path('create/resource/upload_list', GetResource.as_view(), name='get_resource'),
    path('create/resource/download_list', GetDownload.as_view(), name='get_download'),
    path('create/resource/delete', DelResource.as_view(), name='del_resource'),
    path('collection/list', GetClist.as_view(), name='get_collection_list'),
    path('collection/info', GetCinfo.as_view(), name='get_collection_info'),
    path('collection/add_article', AddArticle.as_view(), name='add_article'),
    path('collection/add_resource', AddResource.as_view(), name='add_resource'),
    path('collection/remove_article', RemoveArticle.as_view(), name='remove_article'),
    path('collection/remove_resource', RemoveResource.as_view(), name='remove_resource'),
    path('collection/new', NewCollection.as_view(), name='new_collection'),
    path('collection/rename', Rename.as_view(), name='rename_collection'),
    path('collection/condition', SetCondition.as_view(), name='change_condition'),
    path('collection/delete', DelCollection.as_view(), name='delete_collection'),
    path('collection/move_article', MoveArticle.as_view(), name='move_article'),
    path('collection/move_resource', MoveResource, name='move_resource'),
    re_path(r'.*', TemplateView.as_view(template_name='index.html')),
]
