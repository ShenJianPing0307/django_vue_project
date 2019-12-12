from rbac import models
from django.conf import settings
from crm.utils.session import SessionStore
import json

class InitPermission(object):

    def __init__(self, request, user):
        self.request = request
        self.user = user
        self.permissions_dict = {}
        self.menus_dict = {}

    def init_data(self):
        """
        从数据库中获取权限信息以及用户信息
        :return:
        """
        self.permissions_queryset = self.user.roles.filter(permissions__url__isnull=False).values(
            'permissions__id',
            'permissions__url',
            'permissions__title',
            'permissions__parent_id',
            'permissions__action__code',
            'permissions__menu_id',
            'permissions__menu__title',
            'permissions__menu__icon',
            'permissions__menu__position'
        ).distinct()
        return self.permissions_queryset


    def init_permissions_dict(self):
        """
            初始化权限，获取当前用户权限并添加到session中
        将当前用户权限信息转换为以下格式，并将其添加到Session中
        {
            '/index.html': ['GET','POST','DEL','EDIT],
            '/detail-(\d+).html': ['GET','POST','DEL','EDIT],
        }
        :return:
        """

        for row in self.init_data():
            if row["permissions__url"] in self.permissions_dict:
                self.permissions_dict[row["permissions__url"]].append(row["permissions__action__code"])
            else:
                self.permissions_dict[row["permissions__url"]] = [row["permissions__action__code"], ]

        self.request.permissions_dict = self.permissions_dict

        # self.request._request.session[settings.PERMISSION_SESSION_KEY] = self.permissions_dict
        # self.request._request.session[settings.PERMISSION_SESSION_KEY] = self.permissions_dict
        # SessionStore().set_session(settings.PERMISSION_SESSION_KEY,self.permissions_dict)

        return self.permissions_dict


    def init_menus_dict(self):
        """
               构建菜单字典并且存入session,之所以构建字典，可以通过制定的position进行排序
               self.menus_dict={
               1:{
               title:'客户管理',icon:'fa fa-coffe',children:[
               {'id':1,'url':'/customer/list/','title':'客户列表'}
               ...
               ]
               }
               }
               :return:
        """
        for row in self.init_data():
            menu_id = row["permissions__menu_id"]
            if not menu_id:
                continue

            if menu_id not in self.menus_dict:
                self.menus_dict[row["permissions__menu__position"]] = {
                    "id":row["permissions__menu_id"],
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
                self.menus_dict[row["permissions__menu__position"]]["children"].append(
                    {
                        'id': row['permissions__id'],
                        'title': row['permissions__title'],
                        'url': row['permissions__url']

                    }
                )
        # print(self.menus_dict)
        # self.request._request.session[settings.MENU_SESSION_KEY] = self.menus_dict
        self.request.menus_dict = self.menus_dict

        return self.menus_dict
