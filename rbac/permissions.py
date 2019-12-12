

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re
from django.shortcuts import HttpResponse
import json
from crm.utils.session import SessionStore
from rest_framework import exceptions
from rest_framework.response import Response

from rest_framework.permissions import BasePermission


class Permission(BasePermission):

    message = "无权限访问"

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        permissions_dict = {}
        menus_dict = {}

        """
        从数据库拿到该用户的所有权限，
        request.user是认证后拿到的元组第一个值
        """
        permissions_queryset = request.user.roles.filter(
            permissions__url__isnull=False).values(
            'permissions__id',
            'permissions__url',
            'permissions__title',
            'permissions__parent_id',
            'permissions__action__code',
            'permissions__menu_id',
            'permissions__menu__title',
            'permissions__menu__icon',
            'permissions__menu__position').distinct()

        """
        将用户的权限进行数据结构的调整
        {

            '/index.html': ['GET','POST','DEL','EDIT],
            r'/detail-(\d+).html': ['GET','POST','DEL','EDIT],

        }
        """
        for row in permissions_queryset:
            if row["permissions__url"] in permissions_dict:
                permissions_dict[row["permissions__url"]].append(
                    row["permissions__action__code"])
            else:
                permissions_dict[row["permissions__url"]] = [
                    row["permissions__action__code"], ]
        """
        初始化用户菜单，也就是该用户可以访问的菜单
        """
        for row in permissions_queryset:
            menu_id = row["permissions__menu_id"]
            if not menu_id:
                continue

            if menu_id not in menus_dict:
                menus_dict[row["permissions__menu__position"]] = {
                    "id": row["permissions__menu_id"],
                    "title": row["permissions__menu__title"],
                    "icon": row["permissions__menu__icon"],
                    "children": [
                        {
                            'id': row['permissions__id'],
                            'title': row['permissions__title'],
                            'url': row['permissions__url']

                        }
                    ]
                }

            else:
                menus_dict[row["permissions__menu__position"]]["children"].append(
                    {
                        'id': row['permissions__id'],
                        'title': row['permissions__title'],
                        'url': row['permissions__url']

                    }
                )
        """
        将该用户的权限赋值给视图，这样在视图中可以拿到对应的权限，
        传给前端进行按钮级别的权限验证
        """
        view.permissions_dict = permissions_dict
        """
        将该用户的菜单赋值给视图，这样在视图中可以拿到对应的菜单，
        传给前端进行左侧菜单的初始化
        """
        view.menus_dict = menus_dict

        """
        过滤白名单
        """

        for pattern in settings.RBAC_NO_AUTH_URL:

            if re.match(pattern, request.path_info):
                return None

        if not permissions_dict:
            return False

        # 请求url与用户拥有的权限进行匹配
        """
        /crm/menus {'/rights': ['get'], '/user': ['get', 'post'], '/roles': ['get']}
        """
        flag = False
        for pattern, code_list in permissions_dict.items():
            upper_code_list = [item.upper() for item in code_list]
            request_permission_code = request.method

            if re.match(pattern, request.path_info):
                if request_permission_code in upper_code_list:
                    permission_code_list = upper_code_list

                    # 将用户角色拥有的请求方式赋值给视图
                    view.PERMISSION_CODE_LIST_KEY = permission_code_list

                    flag = True
                    break

        if not flag:
            return False

        return True
