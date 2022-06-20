"""
员工信息管理：增、删、改、查

"""
from django.shortcuts import render, redirect, HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from _datetime import datetime


def index(request, pIndex=1):
    """首页用户列表展示"""
    umod = User.objects
    ulist = umod.filter(status__lt=9)  # 排除状态为9（已注销）

    # 获取并判断搜索条件
    mywhere = []  # 用于维持搜索,用于存放搜索值条件
    kw = request.GET.get("keyword")
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))  # 模糊查询
        mywhere.append("keyword=" + kw)
    # 还可以加入其他条件，如状态等，方法一致，条件加入mywhere[]即可

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 5)  # 以每页五条数据分页
    maxpages = page.num_pages  # 获取最大页数
    print(maxpages)
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list = page.page(pIndex)  # 获取当前页信息
    plist = page.page_range  # 获取页面列表信息

    context = {"user_list": list, "plist": plist, "pIndex": pIndex, "maxpages": maxpages, "mywhere": mywhere}

    return render(request, "myadmin/user/index.html", context)


def add(request):
    """加载信息添加表单"""
    return render(request, "myadmin/user/add.html")


def insert(request):
    """执行信息添加"""
    try:
        ob = User()
        ob.username = request.POST["username"]
        ob.nickname = request.POST["nickname"]
        print(ob.username, ob.nickname)

        # md5加密操作
        import hashlib
        import random

        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST["password"] + str(n)  # 从表单获取密码并加入干扰值
        md5.update(s.encode('utf-8'))  # 将要产生md5的字符串放进去
        ob.password_hash = md5.hexdigest()  # 获取md5值
        ob.password_salt = n

        ob.status = request.POST["status"]
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        ob.save()
        context = {'info': "添加成功"}
    except Exception as e:
        print(e)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    """执行信息删除"""
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        context = {'info': "删除成功"}
    except Exception as e:
        print(e)
        context = {'info': "删除失败"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    """执行信息编辑表单"""
    try:
        ob = User.objects.get(id=uid)
        context = {'user': ob}
        return render(request, "myadmin/user/edit.html", context)
    except Exception as e:
        print(e)
        context = {'info': "没有找到要修改的信息"}
        return render(request, "myadmin/info.html", context)


def update(request, uid=0):
    """执行信息修改表单"""
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST["nickname"]
        ob.status = request.POST["status"]
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功"}
    except Exception as e:
        print(e)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)
