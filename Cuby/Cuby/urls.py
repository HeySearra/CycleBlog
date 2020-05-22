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
from user.views import Register, Login

urlpatterns = [
    path('/admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('register/submit', Register.as_view(), name='register'),
    path('login/submit', Login.as_view(), name='register'),
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
    # path('member/', include([
    #
    # ])),
    re_path(r'.*', TemplateView.as_view(template_name='index.html')),
]
