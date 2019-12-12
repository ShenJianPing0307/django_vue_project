# from django.test import TestCase
#
# # Create your tests here.
# {
#     {
#         'title': '用户管理',
#         'icon': 'el-icon-location',
#         'id': 1,
#         'children': [{'title': '用户列表', 'url': '/crm/user', 'id': 1},
#                      {'title': '部门列表', 'url': '/crm/dept', 'id': 11}
#                      ]
#     },
#     {
#         'title': '权限管理',
#         'icon': 'el-icon-s-check',
#         'id': 2,
#         'children': [{'title': '权限列表', 'url': '/rbac/rights/list', 'id': 2},
#                      {'title': '角色列表', 'url': '/rbac/roles', 'id': 7},
#                      {'title': '菜单列表', 'url': '/crm/menus', 'id': 12}
#                      ]
#     }
# }
#
# """
# 权限信息
# """
# {
#     '/crm/dept': ['get'],
#     '/crm/menus': ['get'],
#     '/rbac/roles': ['get'],
#     '/rbac/roles/(?P<roleId>\\d+)/permission$': ['put'],
#     '/rbac/rights/list': ['get'],
#     '/rbac/roles/(?P<roleId>\\d+)/permission/(?P<permissionId>\\d+)$': ['delete'],
#     '/crm/user': ['get', 'post']
# }
from rest_framework import serializers

class RoleSerialize(serializers.Serializer):
    title = serializers.CharField(max_length=32)
    desc = serializers.CharField(max_length=32)
    permissions = serializers.SerializerMethodField()

    def get_permissions(self,row):
        """
        :param row: 每一行对象，也就是Role对象
        :return:
        """
        permissionLsit = row.permissions.all()
        return "、".join([item.title for item in permissionLsit])

from rest_framework.views import APIView
from rbac import models
from rest_framework.response import Response

class RoleView(APIView):
    authentication_classes = []

    def get(self,request,*args,**kwargs):
        RoleList = models.Role.objects.all()
        rl = RoleSerialize(RoleList,many=True)
        return Response(rl.data)

    def post(self,request,*args,**kwargs):
        r1 = RoleSerialize(data=request.data)
        if r1.is_valid():
            print(r1.validated_data)
            r1.save()
            return Response(r1.data)
        else:
            return Response(r1.errors)
