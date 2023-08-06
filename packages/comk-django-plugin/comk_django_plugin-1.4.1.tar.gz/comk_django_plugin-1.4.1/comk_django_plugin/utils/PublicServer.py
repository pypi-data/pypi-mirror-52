import json

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout

from comk_django_plugin import general_resolve_request_data
from .BaseMoudel import BaseMoudel


class PublicServer(BaseMoudel):
    '''
    服务公共类，作为基础服务使用

    '''

    def __init__(self, request: HttpRequest):
        '''
        默认构建一个请求数据体和返回数据体

        :param request:
        '''
        super().__init__()
        self.request = request
        self.request_data = general_resolve_request_data(request)

    def return_json_response(self, data):
        '''
        传入数据，返回 JsonResponse

        如果直接用 JsonResponse 返回中文，则返回给前端后，中文会转义为Unicode码。
        这时，可以用 json_dumps_params 参数，设置 {'ensure_ascii': False} 即可正常显示中文。

        原理：
        JsonResponse()在初始化的时候使用了json.dumps()把字典转换成了json格式，具体方法如下：

            data = json.dumps(data, cls=encoder, **json_dumps_params)

        当ensure_ascii为True的时候，对于非ASCII码的值，会被JSON转义，这样，中文=就被转义为Unicode码。
        当ensure_ascii为False的时候，对于非ASCII码的值，不会被JSON转义，直接返回真实值。

        所以含有中文的字典转json字符串时，使用 json.dumps() 方法要把ensure_ascii参数改成false，
        即 json.dumps(dict，ensure_ascii=False)。

        JsonResponse()接收参数有关键词参数，json_dumps_params=None ，用来给 json.dumps() 传参，
        所以 要在关键字参数后面拼个字典来传另一组关键字参数 ensure_ascii=False，即：json_dumps_params={'ensure_ascii':False}

        :param data:
        :return:
        '''
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

    def return_self_json_response(self):
        '''
        使用当前服务公共类的response_data，返回 JsonResponse

        :return:
        '''
        return self.return_json_response(self.response_data)

    def return_build_success_response(self, response_data=None, timestamp_now=False):
        '''
        业务成功返回，JsonResponse格式

        :param response_data:
        :param timestamp_now:
        :return:
        '''

        return self.return_json_response(
            self.build_success_response_data(response_data=response_data, timestamp_now=timestamp_now))

    def return_build_error_response(self, code='1000', msg=None, timestamp_now=False):
        '''
        业务失败返回，JsonResponse格式

        :param code:
        :param msg:
        :param timestamp_now:
        :return:
        '''

        return self.return_json_response(
            self.build_error_response_data(code=code, msg=msg, timestamp_now=timestamp_now))

    def login_user(self, username, password):
        '''
        登录一个用户

        :param username:
        :param password:
        :return:
        '''
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return True

    def logout_user(self):
        '''
        登出一个用户

        :param username:
        :param password:
        :return:
        '''
        if self.check_login_user():
            logout(self.request)

    def check_login_user(self, request=None):
        '''
        检验用户是否登录
        True 为已登录

        :param request:
        :return:
        '''
        request = request if request else self.request
        return hasattr(request, 'user') and request.user.is_authenticated()
