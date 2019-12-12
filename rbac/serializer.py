
from rest_framework import serializers
from rbac import models
from rest_framework.response import Response



class RoleModelSrializer(serializers.ModelSerializer):

    permissions = serializers.SerializerMethodField()

    def get_permissions(self,row):
        permissions=row.permissions.values('id','title','url','action__code','parent_id','menu_id')
        permission_dict = {}

        menu_dict = {}

        for item in permissions:
            if item["menu_id"]:
                menu_list= models.Menu.objects.filter(id=item['menu_id']).values('id','title').distinct()
                for item in menu_list:
                    item["children"] = []
                    menu_dict[item["id"]] = item

        for item in permissions:
            if not item["parent_id"]:
                item["children"] = []
                permission_dict[item["id"]] = item
                menu_id=item["menu_id"]
                menu_dict[menu_id]["children"].append(item)

        for item in permissions:
            pid = item["parent_id"]

            if pid:
                print('pid',item)
                print('permission_dict', permission_dict)

            #     print(permission_dict[pid])
                # permission_dict[pid]["children"].append(item)
        role_has_permission = [item for menu_id,item in menu_dict.items()]

        return permission_dict

    class Meta:
        model = models.Role
        fields= "__all__"
        # exclude = ['permissions']

# class ActionSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Action
#         fields = "__all__"
#
# class MenuSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Menu
#         fields = "__all__"
#
# class ParentSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Permission
#         fields = "__all__"

class PermissionSerilizer(serializers.ModelSerializer):
    action = serializers.SerializerMethodField()  # 自定义显示

    def get_action(self, row):
        return row.action.code

    menu = serializers.SerializerMethodField()  # 自定义显示

    def get_menu(self, row):
        if row.menu:
            return row.menu.title

    class Meta:
        model = models.Permission
        fields = "__all__"




