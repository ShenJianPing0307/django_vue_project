from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        print('response.data',response.status_code)
        response.data.clear()
        # response.data['code'] = 2002
        response.data['data'] = {}
        response.data['meta'] = {}
        response.data['meta']['code'] = 2002


        if response.status_code == 404:
            try:
                response.data['message'] = response.data.pop('detail')
                response.data['message'] = "Not found"
            except KeyError:
                response.data['message'] = "Not found"

        if response.status_code == 400:
            response.data['message'] = 'Input error'

        elif response.status_code == 401:
            response.data['message'] = "Auth failed"

        elif response.status_code >= 500:
            response.data['message'] = "Internal service errors"

        elif response.status_code == 403:
            response.data['meta']['message'] = "无权限访问"

        elif response.status_code == 405:
            response.data['message'] = 'Request method error'
    print(response.data) #{'data': {}, 'meta': {'code': 2002, 'message': '无权限访问'}}
    return response
# {"data": {}, "meta": {"message": "rbac无权限访问", "code": 2002}}

