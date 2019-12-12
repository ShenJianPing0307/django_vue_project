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
from django.conf.urls import url, include
from django.contrib import admin
from rbac import views

app_name = '[rbac]'

urlpatterns = [
    url(r'^roles$', views.RoleModelView.as_view({"get": "list", }), name="role-list"),
    url(r'^rights/(?P<type>\w+)$', views.RightsModelView.as_view({"get": "list"}), name="rights-list"),
    url(r'^roles/(?P<roleId>\d+)/permission/(?P<permissionId>\d+)$',
        views.RightsModelView.as_view({"delete": "destroy"}), name="rights-destroy"),
    url(r'^roles/(?P<roleId>\d+)/permission$',
        views.RightsModelView.as_view({"put": "update"}), name="rights-update"),

    url(r'^roles/(?P<roleId>\d+)/permission$',
        views.RightsModelView.as_view({"put": "update"}), name="rights-update"),

    #前端获取权限，用于按钮级别的权限检验
    url(r'^roles/rights$',views.RightsView.as_view({"get": "list"}), name="roles-rights-list"),


    # url(r'^rights/list$', views.RightsModelView.as_view({"get": "list", }), name="rights-list"),

    #     url(r'^login',views.LoginView.as_view(), name='login'),
    #     url(r'^login', views.LoginView.as_view(), name='login'),
    #
    #     re_path('authors/$', views.AuthorModelView.as_view({"get":"list","post":"create"}), name="authors"),
    # # re_path('authors/(?P<pk>\d+)/$', views.AuthorModelView.as_view({"get":"retrieve","put":"update","delete":"destroy"}), name="authorsdetail"),
    #

]
