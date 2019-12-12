

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re
from django.shortcuts import HttpResponse
import json
from crm.utils.session import SessionStore

class RbacMiddleware(MiddlewareMixin):

    def process_request(self,request,*args,**kwargs):

        """跳过无需权限访问的URL"""
        # permission_dict = request.session.get(settings.RBAC_PERMISSION_SESSION_KEY)
        print('process_request',request.path_info)

        for pattern in settings.RBAC_NO_AUTH_URL:

            if re.match(pattern, request.path_info):
                return None

        # permission_str= SessionStore().get_session(settings.PERMISSION_SESSION_KEY)
        # permission_dict = eval(permission_str)
        #
        # print(request.path_info,permission_dict)
        """
        /crm/menus {'/rights': ['get'], '/user': ['get', 'post'], '/roles': ['get']}
        """
        #
        # # permission_dict = json.loads(permission_str)
        # print(type(permission_dict))

        #从redis中获取permission_dict
        permission_bytes = SessionStore().get_session(settings.PERMISSION_SESSION_KEY)

        print('bytes',permission_bytes)

        permission_dict = eval(permission_bytes)
        if not permission_dict:
            return HttpResponse(json.dumps({"data": {}, "meta": {"message": "无权限访问", "code": 2002}}))

        print('permi',permission_dict)

        #请求url与redis中存储的权限进行匹配
        """
        /crm/menus {'/rights': ['get'], '/user': ['get', 'post'], '/roles': ['get']}
        """
        flag = False
        for pattern,code_list in permission_dict.items():
            print('par,code...',pattern,request.path_info)
            upper_code_list=[item.upper() for item in code_list]
            request_permission_code = request.method

            if re.match(pattern,request.path_info):
                print(request_permission_code)
                print(upper_code_list)
                if request_permission_code in upper_code_list:
                    permission_code_list = upper_code_list
                    #将用户角色拥有的请求方式存储起来，传给前端进行按钮权限的验证
                    SessionStore().set_session(settings.PERMISSION_CODE_LIST_KEY,permission_code_list)
                    flag = True
                    break
        print(flag)

        if not flag:
            return HttpResponse(json.dumps({"data": {}, "meta": {"message": "rbac无权限访问", "code": 2002}}))









