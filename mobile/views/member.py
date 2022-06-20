from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth

def index(request):
    """个人中心首页"""
    return render(request, "mobile/member.html")


def orders(request):
    """个人中心浏览订单"""
    return render(request, "mobile/member_order.html")


def detail(request):
    """个人中心中的订单详情"""
    return render(request, "mobile/member_detail.html")


def log_out(request):
    """会员退出"""
    auth.logout(request)
    return render(request, "mobile/register.html")
