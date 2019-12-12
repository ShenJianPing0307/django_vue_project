from rest_framework.authentication import BaseAuthentication
import time
import hashlib
from crm.models import *
from rest_framework.exceptions import AuthenticationFailed

class AuthToken(BaseAuthentication):
    """
    认证类
    """
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        在请求头中获取token进行验证,如果前端的请求头是Authorization，django请求头必须以大写HTTP开头，
        中间以_分隔的大写键值
        """
        token = request._request.META.get("HTTP_AUTHORIZATION")
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise AuthenticationFailed({
            "data":{},
            "meta":{
                "code":2003,
                "message":"用户认证失败"
            }
        })
        return (token_obj.user,token_obj)

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass


def get_md5(username):
    """
    生成对应用户的token
    :param username: 用户名
    :return:
    """
    m=hashlib.md5(bytes(username,encoding="utf-8")) #加盐
    ctime = str(time.time())
    m.update(bytes(ctime,encoding="utf-8"))
    return m.hexdigest()