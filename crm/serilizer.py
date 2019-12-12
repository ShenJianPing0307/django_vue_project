from rest_framework import serializers
from crm import models
from rbac import models as rmodels


class RoleModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = rmodels.Role
        fields = '__all__'


class DeptModelSerialize(serializers.ModelSerializer):
    class Meta:
        model = models.DepartMent
        fields = '__all__'

class UserModelSerlizer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = '__all__'

    gender = serializers.CharField(source="get_gender_display")
    department = serializers.CharField(source="department.name")
    # department = DeptModelSerialize()
    # roles = RoleModelSerilizer(many=True)

    roles = serializers.SerializerMethodField()  # 自定义显示

    def get_roles(self, row):
        roles_list = row.roles.all()
        return ["%s、" % item.title for item in roles_list]

class RetrieveUserModelSerlizer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = '__all__'

    gender = serializers.CharField(source="get_gender_display")
    department = DeptModelSerialize()
    roles = RoleModelSerilizer(many=True)


class EditUserSerialize(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        max_length=16,
        error_messages={
            "required": "密码不能为空"
        }
    )
    email = serializers.EmailField(
        error_messages={
            "required": "邮箱不能为空",
            "invalid": "无效的邮箱地址"
        }
    )
    phone = serializers.IntegerField(
        error_messages={
            "required": "手机号不能为空"
        })

    def update(self, instance, validated_data):
        instance.username = validated_data["username"]
        instance.password = validated_data["password"]
        instance.email = validated_data["email"]
        instance.phone = validated_data["phone"]
        instance.save()
        return instance


class AddUserModelSerilizer(serializers.ModelSerializer):
    # department = DeptModelSerialize()

    class Meta:
        model = models.UserInfo
        fields = "__all__"

    def create(self, validated_data):
        user = models.UserInfo.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.roles.remove(*[obj.id for obj in instance.roles.all()])
        print('old',instance)
        # instance.roles.add(*list(validated_data["roles"]))
        instance.roles.set([ obj.id for obj in validated_data["roles"]])
        print('new',[ obj.id for obj in validated_data["roles"]])
        return instance
#
# class SetUserRoleModelSerilizer(serializers.ModelSerializer):
#     # department = DeptModelSerialize()
#
#     class Meta:
#         model = models.UserInfo
#         fields = ("roles", )
#
#     def update(self, instance, validated_data):
#         print(type(validated_data["roles"]))
#         print('nnn',instance.roles)
#         instance.roles.set(validated_data["roles"])
#         # instance.save()
#         return instance







