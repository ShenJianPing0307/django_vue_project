from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rbac.serializer import *
import json
from crm.utils.session import SessionStore
from django.conf import settings

# Create your views here.

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet


class RoleModelView(GenericViewSet):

    def list(self, request, *args, **kwargs):
        role_queryset = models.Role.objects.all()

        role_list = []

        for row in role_queryset:
            role_dict = {}
            role_dict["id"] = row.id
            role_dict["title"] = row.title
            role_dict["desc"] = row.desc
            role_dict["children"] = []

            permissions = row.permissions.values('id', 'title', 'url', 'action__code', 'parent_id', 'menu_id')

            # menu_list = [models.Menu.objects.filter(id=item["menu_id"]).values('id','title','desc') for item in permissions]
            menu_list = []
            unrepeat_list = []
            menu_dict = {}
            permission_dict = {}
            for item in permissions:
                if item["menu_id"]:
                    menu_queryset = models.Menu.objects.filter(id=item['menu_id']).values('id', 'title')
                    for item in menu_queryset:
                        menu_list.append(item)

            print(row, menu_list)
            for item in menu_list:
                if item not in unrepeat_list:
                    unrepeat_list.append(item)
            print(row, unrepeat_list)
            for item in unrepeat_list:
                item["children"] = []
                menu_dict[item["id"]] = item
                role_dict["children"].append(item)

                # item_dict = {}
                # item_dict["id"] = item.id
                # item_dict["title"] = item.title
                # item_dict["children"] = []
                # menu_dict[item.id] = item_dict
                # role_dict["children"].append(item_dict)

            for item in permissions:
                if not item["parent_id"]:
                    item["children"] = []
                    permission_dict[item["id"]] = item
                    menu_id = item["menu_id"]
                    menu_dict[menu_id]["children"].append(item)

            for item in permissions:
                pid = item["parent_id"]

                if pid:
                    print(pid)
                    print('permission', permission_dict)
                    permission_dict[pid]["children"].append(item)
            # role_has_permission = [item for menu_id, item in menu_dict.items()]
            role_list.append(role_dict)

        return Response({"data": role_list, "meta": {
            "message": "获取数据成功", "code": 2000}})


class RightsModelView(GenericViewSet):
    queryset = models.Permission.objects.all()

    def list(self, request, *args, **kwargs):
        """
               所有的一级菜单
               all_menu_dict
               {1: {'id': 1, 'children': [], 'title': '用户管理'}, 2: {'id': 2, 'children': [], 'title': '权限管理'}}
               """
        type = kwargs.get("type", '')
        if type == "tree":
            all_menu_list = models.Menu.objects.values('id', 'title')
            all_menu_dict = {}
            for item in all_menu_list:
                item["is_menu"] = True
                item["children"] = []
                all_menu_dict[item["id"]] = item

            """
            # 所有二级菜单
            {
        "1": {
            "url": "/user",
            "title": "用户列表",
            "action__code": "list",
            "children": [],
            "id": 1,
            "parent_id": null
        },
        "2": {
            "url": "/rights",
            "title": "权限列表",
            "action__code": "list",
            "children": [],
            "id": 2,
            "parent_id": null
        }
    }
            """
            all_second_menu_list = models.Permission.objects.filter(parent_id__isnull=True).values(
                'id', 'title', 'url', 'action__code', 'parent_id', 'menu_id')
            all_second_menu_dict = {}
            for item in all_second_menu_list:
                item["children"] = []
                all_second_menu_dict[item["id"]] = item

                menu_id = item["menu_id"]
                all_menu_dict[menu_id]["children"].append(item)

            """
            # 所有三级菜单（不能做菜单的权限,做按钮的权限）
            [
        {
            "title": "添加用户",
            "parent_id": 1,
            "url": "/user",
            "action__code": "create",
            "id": 3
        },
        {
            "title": "删除用户",
            "parent_id": 1,
            "url": "user/(?P<pk>\\d+)$",
            "action__code": "destroy",
            "id": 4
        }
    ]
            """
            all_third_permission_list = models.Permission.objects.filter(parent_id__isnull=False).values('id', 'title', 'url',
                                                                                                   'action__code',
                                                                                       'parent_id')
            for item in all_third_permission_list:
                pid = item["parent_id"]
                if not pid:
                    continue
                all_second_menu_dict[pid]["children"].append(item)
            menu_list = [item for menu_id, item in all_menu_dict.items()]
            return Response({
                "data": menu_list,
                "meta": {
                    "message": "获取成功",
                    "code": 2000
                }
            }
            )

        elif type == "list":
            permission_queryset = self.get_queryset().order_by("id")
            ser = PermissionSerilizer(instance=permission_queryset, many=True)
            return Response({
                "data": ser.data,
                "meta": {
                    "message": "获取成功",
                    "code": 2000
                }
            })

    from rest_framework.request import Request
    def destroy(self, request, *args, **kwargs):
        ret = {"data": [], "meta": {
            "message": "删除权限成功", "code": 2000}}
        try:
            roleId = kwargs["roleId"]
            if roleId:
                role_obj = models.Role.objects.filter(id=roleId).first()

                # permissions = role_obj.permissions.values('id', 'title', 'url', 'action__code', 'parent_id', 'menu_id')
                # permission_dict = {}
                # menu_dict = {}
                #
                # for item in permissions:
                #     if item["menu_id"]:
                #         menu_list = models.Menu.objects.filter(id=item['menu_id']).values('id', 'title').distinct()
                #         for item in menu_list:
                #             item["children"] = []
                #             menu_dict[item["id"]] = item

                # for item in permissions:
                #     if not item["parent_id"]:
                #         item["children"] = []
                #         permission_dict[item["id"]] = item
                #
                #
                #
                # last_perrmission_dict = {}
                # for item in permissions:
                #     pid = item["parent_id"]
                #     if pid:
                #         last_perrmission_dict[item["id"]] = item
                #         permission_dict[pid]["children"].append(last_perrmission_dict)

                permissionId = int(kwargs["permissionId"])
                if permissionId:
                    all_permissions = role_obj.permissions.all()
                    permissionIdList = [item.id for item in all_permissions]
                    if permissionId in permissionIdList:
                        obj = models.Permission.objects.filter(id=permissionId).first()
                        if obj.parent_id:
                            # 删除例如添加用户的权限
                            role_obj.permissions.remove(obj)
                        else:
                            # 删除例如用户列表的权限
                            exclude_root_permissions = models.Permission.objects.filter(parent_id=obj.id).all()
                            for row in exclude_root_permissions:
                                role_obj.permissions.remove(row)
                            role_obj.permissions.remove(obj)
        except Exception as e:
            ret["meta"]["message"] = "删除失败"
            ret["meta"]["code"] = 2001

        return Response(ret)

    def update(self,request,*args,**kwargs):
        ret = {"data": [], "meta": {
            "message": "更新权限成功", "code": 2000}}
        try:
            roleId = kwargs.get("roleId",'')
            permissionIdList = request.data
            print(type(permissionIdList),permissionIdList)
            if roleId:
                roleId = int(roleId)
                roleObj = models.Role.objects.filter(id=roleId).first()
                roleObj.permissions.clear()
                roleObj.permissions.add(*permissionIdList)
        except Exception as e:
            ret["meta"]["message"] = "更新权限失败"
            ret["meta"]["code"] = 2001
        return Response(ret)

class RightsView(GenericViewSet):

    def list(self,request,*args,**kwargs):
        """
        从redis中获取权限相关，用于前台按钮级别权限检验
        {'/crm/dept$': ['get'], 'rights/(?P<type>\\w+)$': ['get'], '/crm/menus': ['get']
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        #从redis中获取permission_dict
        ret = {"data": {}, "meta": {
            "message": "获取权限信息成功", "code": 2000}}
        try:
            # permission_bytes = SessionStore().get_session(settings.PERMISSION_SESSION_KEY)
            # permission_dict = eval(permission_bytes)
            # ret["data"] = permission_dict
            ret["data"] = self.permissions_dict
        except Exception as e:
            ret["meta"]["message"] = "获取权限信息失败"
            ret["meta"]["code"] = 2001

        return Response(ret)




class MenuModelView(GenericViewSet):
    pass
