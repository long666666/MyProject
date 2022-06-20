from django.shortcuts import redirect
from django.urls import reverse
import re


class Shopmiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        print("url", path)

        # 判断管理后台是否登录
        # 定义后台允许直接访问的url列表
        url_list = ["/myadmin/log_in/", "/ myadmin / log_out / ", "/myadmin/do_login/", "/myadmin/verify/"]

        # 判断当前请求url地址是否是以/myadmin开头
        if re.match(r'^/myadmin', path) and path not in url_list:
            # 判断是否登录（通过session验证）,
            if 'adminuser' not in request.session:
                return redirect(reverse('myadmin_log_in'))

        # 判断大堂点餐请求，是否登录
        if re.match(r'^/web', path):
            # 判断是否登录（通过session验证）,
            if 'webuser' not in request.session:
                return redirect(reverse('web_log_in'))

        # 判断移动端是否登录
        # 定义移动端允许直接访问的url列表
        url_list = ["/mobile/register/", "/mobile/do_register/"]
        if re.match(r'^/mobile', path) and (path not in url_list):
            # 判断是否登录（通过session验证）,
            if 'mobileuser' not in request.session:
                return redirect(reverse('mobile_register'))

        response = self.get_response(request)
        return response
