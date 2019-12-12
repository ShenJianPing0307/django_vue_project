"""yw_django_vue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from crm import views

#使用路由器不用自己写路由
from rest_framework import routers
# router=routers.DefaultRouter()
# router.register('user',views.UserModelView) #user前缀



app_name='[crm]'

urlpatterns = [
    url(r'^user$',views.UserModelView.as_view({"get":"list","post":"create"}), name="user-list"),
    url(r'^user/(?P<pk>\d+)$', views.UserModelView.as_view({"delete":"destroy","get":"retrieve","put":"update"}), name="user-delete"),
    # url(r'^user', views.UserModelView.as_view({"delete": "destroy", "get": "retrieve", "put": "update"}),
    #     name="user-delete"),

    url(r'^user/(?P<pk>\d+)/role$', views.UserRoleView.as_view({"put": "update"}), name="set-role"),

    url(r'^dept$', views.DeptModelView.as_view({"get": "list", }), name="dept-list"),

    #菜单信息
    url(r'^menus$', views.MenuModelView.as_view({"get": "list", }), name="menus-list"),

    #
#     #     re_path('authors/$', views.AuthorModelView.as_view({"get":"list","post":"create"}), name="authors"),
# #         url(r'^', include(router.urls)),
]

