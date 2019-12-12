from django_filters.rest_framework import DjangoFilterBackend,OrderingFilter
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, HttpResponse,render_to_response
from django.views import View
from crm.forms.login import LoginForm
from django.middleware.csrf import get_token, rotate_token
# Create your views here.
import json
from crm.models import *
import uuid
from rest_framework import viewsets
from crm.serilizer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from crm.utils.auth import get_md5, AuthToken
from crm.permissions.InitPermission import InitPermission
from django.conf import settings
from django.template import RequestContext
# from django.core.exceptions import PermissionDenied
from rest_framework import exceptions


class LoginView(APIView):
    authentication_classes = []  # 登陆页面免认证
    permission_classes = []

    def post(self, request, *args, **kwargs):

        ret = {
            "data": {},
            "meta": {
                "code": 2001,
                "message": "用户名或密码错误"
            }
        }
        user_obj = json.loads(str(request._request.body, encoding='utf8'))
        username = user_obj.get('username')
        password = user_obj.get('password')
        if username and password:
            obj = UserInfo.objects.filter(
                username=username, password=password).first()
            if obj:
                #初始化权限信息

                # InitPermission(request,obj).init_permissions_dict()
                # InitPermission(request,obj).init_menus_dict()
                # InitPermission(request,obj).init_permissions_dict()

                # menus_dict = request._request.session.get(settings.MENU_SESSION_KEY)


                # 生成token值
                # token=str(uuid.uuid4()) #uuid生成token
                token = get_md5(username)
                # 自动去数据库检查，如果没有就创建，否则更新token
                UserToken.objects.update_or_create(user=obj, defaults={'token': token})
                # user_token=UserToken.objects.filter(user=obj).first()
                # if not user_token:
                #     UserToken.objects.create(user=obj,token=token)
                ret["data"]["username"] = username
                ret["data"]["password"] = password
                ret["data"]["token"] = token
                # ret["data"]["permission_session_id"] = settings.PERMISSION_SESSION_KEY
                # ret["data"]["menu_session_id"] = settings.MENU_SESSION_KEY
                ret["meta"]["code"] = 2000
                ret["meta"]["message"] = "登陆成功"
            else:
                pass
        else:
            pass
        return HttpResponse(json.dumps(ret, ensure_ascii=False))
# class LoginView(View):
#
#     def get(self,request):
#         pass
#
#     def post(self,request):
#         ret={
#             "data":{},
#             "meta":{
#                 "code":2001,
#                 "message":"用户名或密码错误"
#             }
#         }
#         user_obj=json.loads(str(request.body,encoding='utf8'))
#         username=user_obj.get('username')
#         password=user_obj.get('password')
#         if username and password:
#             obj=UserInfo.objects.filter(username=username,password=password).first()
#             if obj:
#                 #生成token值
#                 token=str(uuid.uuid4())
#                 user_token=UserToken.objects.filter(user=obj).first()
#                 if not user_token:
#                     UserToken.objects.create(user=obj,token=token)
#                 ret["data"]["username"]=username
#                 ret["data"]["password"]=password
#                 ret["data"]["token"]=token
#                 ret["meta"]["code"]=2000
#                 ret["meta"]["message"]="登陆成功"
#             else:
#                 pass
#         else:
#             pass
#         return HttpResponse(json.dumps(ret,ensure_ascii=False))


class MyPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'size'
    max_page_size = 5
    page_query_param = 'page'

from rest_framework.permissions import DjangoModelPermissions


class UserModelView(GenericViewSet):
    # 认证成功后可以拿到元组参数 request.user,request.auth，用于权限



    queryset = models.UserInfo.objects.all()
    serializer_class = UserModelSerlizer

    # filter_backends = (DjangoFilterBackend,OrderingFilter)
    filter_fields = ('id','username',)
    # filter_class = UserInfoFilter
    # ordering_fields = '__all__'
    # ordering = ('-id',)

    # def permission_denied(self, request, message=None):
    #     """
    #     If request is not permitted, determine what kind of exception to raise.
    #     """
    #     if request.authenticators and not request.successful_authenticator:
    #         raise exceptions.NotAuthenticated()
    #     # return Response(
    #     #     {"data": [], "meta": {"message": "无权限访问", "code": 2003}}
    #     # )
    #     return render_to_response('page_403.html')

    @action(
        methods="post",
        detail=False,
        url_name="user-create",
        url_path="user")
    def create(self, request, *args, **kwargs):
        print(request.data)
        ser = AddUserModelSerilizer(data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({"data": ser.data, "meta": {
                "message": "用户创建成功", "code": 2000}}, status=201)
        return Response(
            {"data": [], "meta": {"message": "用户创建失败", "code": 2001}})

    def list(self, request, *args, **kwargs):
        """
        查询所有用户信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        #支持搜索username
        condition={}
        username = request.query_params.get('username')
        if username:
            condition={"username":username}
            users = self.get_queryset().order_by("id").filter(**condition)
        else:
            users = self.get_queryset().order_by("id").all()
        pg = MyPageNumberPagination()
        pager_users = pg.paginate_queryset(users, request, view=self)
        ser = UserModelSerlizer(instance=pager_users, many=True)
        return pg.get_paginated_response(ser.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RetrieveUserModelSerlizer(instance)
        return Response({
            "data": serializer.data,
            "meta": {
                "message": "获取成功",
                "code": 2000
            }
        })

    def destroy(self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        ret = {
            "data": {},
            "meta": {
                "message": "删除成功",
                "code": 2000
            }
        }
        instance = self.get_object()
        instance.delete()
        return Response(ret)

    def update(self, request, *args, **kwargs):

        ret = {
            "data": {},
            "meta": {
                "message": "修改成功",
                "code": 2000
            }
        }
        instance = self.get_object()
        ret["data"]["id"] = instance.id
        ret["data"]["role_id"] = [{item.id, item.title}
                                  for item in instance.roles.all()]
        ret["data"]["username"] = instance.username
        ret["data"]["password"] = instance.password
        ret["data"]["email"] = instance.email
        ret["data"]["phone"] = instance.phone

        ser = EditUserSerialize(instance=instance, data=request.data)
        if ser.is_valid(raise_exception=True):
            ser.save()

        return Response(ret)

class DeptModelView(ListModelMixin, GenericViewSet):
    queryset = models.DepartMent.objects.all()
    serializer_class = DeptModelSerialize

    def list(self, request, *args, **kwargs):
        response = super(DeptModelView, self).list(request, *args, **kwargs)
        return Response({"data": response.data, "meta": {
            "message": "获取数据成功", "code": 2000}})


class UserRoleView(GenericViewSet):
    queryset = models.UserInfo.objects.all()

    def update(self, request, *args, **kwargs):
        ret = {"data": {}, "meta": {"message": "分配角色成功", "code": 2000}}
        instance = self.get_object()
        try:
            if request.data:
                instance.roles.set([id for id in request.data["roles"]])
                ret["data"]["uid"] = instance.id
                ret["data"]["roleIsList"] = [id for id in request.data["roles"]]
        except Exception as e:
            ret["meta"]["message"] = "分配角色失败"
            ret["meta"]["code"] = 2001
        return Response(ret)

from collections import OrderedDict
from rest_framework.request import Request
class MenuModelView(GenericViewSet):

    # authentication_classes = [AuthToken]

    def list(self,request,*args,**kwargs):

        ret = {"data": {}, "meta": {"message": "获取菜单成功", "code": 2000}}
        try:
            # user = request.user
            # menus_dict = InitPermission(request, user).init_menus_dict()
            menus_dict = self.menus_dict
            print('menusview',menus_dict)
            od = OrderedDict()
            if menus_dict:
                for key in sorted(menus_dict):
                    od[key] = menus_dict[key]
            ret["data"] = {"menus_list":od.values()}
        except Exception as e:
            ret["meta"]["message"] = "获取菜单失败"
            ret["meta"]["code"] = 2001

        return Response(ret)
