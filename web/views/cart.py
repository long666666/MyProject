"""购物车信息管理视图文件"""
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from myadmin.models import User, Shop, Category, Product


# Create your views here.
def add(request, pid):
    """购物车添加商品操作"""
    # 从session中获取当前店铺的所有菜品信息，并从中获取要放入购物车的菜品
    product = request.session['productlist'][pid]  # 菜品信息
    product['num'] = 1  # 初始化当前菜品的购买量，将购买量追加入菜品信息

    # 尝试从session中获取名字为cartlist的购物车信息，若没有则返回{}
    cartlist = request.session.get('cartlist', {})

    # 判断当前购物车中是否存在要放入购物车的菜品
    if pid in cartlist:
        cartlist[pid]['num'] += product['num']  # 增加购买量
    else:
        cartlist[pid] = product  # 放进购物车

    # 将cartlist放进session
    request.session['cartlist'] = cartlist

    # 跳转到点餐首页
    return redirect(reverse('web_index'))


def delete(request, pid):
    """删除购物车中商品操作"""
    # 尝试从session中获取名字为cartlist的购物车信息，若没有则返回{}
    cartlist = request.session.get('cartlist', {})
    del cartlist[pid]

    # 将cartlist放进session
    request.session['cartlist'] = cartlist

    # 跳转到点餐首页
    return redirect(reverse('web_index'))


def clear(request):
    """清空购物车商品操作"""
    # 将cartlist放进session
    request.session['cartlist'] = {}

    # 跳转到点餐首页
    return redirect(reverse('web_index'))


def change(request):
    """更改购物车商品操作"""
    cartlist = request.session.get('cartlist', {})
    pid = request.GET.get("pid", 0)  # 获取要修改的菜品id
    m = int(request.GET.get("num", 1))  # 要修改的数量
    if m < 1:
        m = 1
    cartlist[pid]['num'] = m  # 修改购物车数量

    # 将cartlist放进session
    request.session['cartlist'] = cartlist

    # 跳转到点餐首页
    return redirect(reverse('web_index'))
