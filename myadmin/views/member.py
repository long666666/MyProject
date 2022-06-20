"""
会员信息管理：展示浏览

"""
from django.shortcuts import render, redirect, HttpResponse
from myadmin.models import Member
from django.core.paginator import Paginator


def index(request, pIndex=1):
    mmod = Member.objects
    mlist = mmod.filter(status__lt=9)  # 排除状态为9（已注销）

    # 获取并判断搜索条件
    mywhere = []  # 用于维持搜索,用于存放搜索值条件
    kw = request.GET.get("keyword", None)
    if kw:
        mlist = mlist.filter(nickname__contains=kw)  # 模糊查询
        mywhere.append("keyword=" + kw)
    # 还可以加入其他条件，如状态等，方法一致，条件加入mywhere[]即可

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(mlist, 5)  # 以每页五条数据分页
    maxpages = page.num_pages  # 获取最大页数
    print(maxpages)
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list = page.page(pIndex)  # 获取当前页信息
    plist = page.page_range  # 获取页面列表信息

    context = {"memberlist": list, "plist": plist, "pIndex": pIndex, "maxpages": maxpages, "mywhere": mywhere}

    return render(request, "myadmin/member/index.html", context)
