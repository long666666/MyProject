"""
店铺信息管理：增、删、改、查

"""
from django.shortcuts import render, redirect, HttpResponse
from myadmin.models import Shop
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
import time
from _datetime import datetime


def index(request, pIndex=1):
    """首页店铺列表展示"""
    smod = Shop.objects
    slist = smod.filter(status__lt=9)  # 排除状态为9（已注销）

    # 获取并判断搜索条件
    mywhere = []  # 用于维持搜索,用于存放搜索值条件
    kw = request.GET.get("keyword")
    if kw:
        slist = slist.filter(name__contains=kw)  # 模糊查询
        mywhere.append("keyword=" + kw)
    # 还可以加入其他条件，如状态等，方法一致，条件加入mywhere[]即可

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(slist, 5)  # 以每页五条数据分页
    maxpages = page.num_pages  # 获取最大页数
    print(maxpages)
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list = page.page(pIndex)  # 获取当前页信息
    plist = page.page_range  # 获取页面列表信息

    context = {"shop_list": list, "plist": plist, "pIndex": pIndex, "maxpages": maxpages, "mywhere": mywhere}

    return render(request, "myadmin/shop/index.html", context)


def add(request):
    """加载信息添加表单"""
    return render(request, "myadmin/shop/add.html")


def insert(request):
    """执行信息添加"""
    try:
        # 店铺封面图片上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, "wb+")
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        # 店铺logo图片上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        # 实例化model,并执行添加操作
        ob = Shop()
        ob.name = request.POST["name"]
        ob.address = request.POST["address"]
        ob.phone = request.POST["phone"]
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.status = request.POST["status"]
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        ob.save()
        context = {'info': "添加成功"}
    except Exception as e:
        print(e)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, sid=0):
    """执行信息删除"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        context = {'info': "删除成功"}
    except Exception as e:
        print(e)
        context = {'info': "删除失败"}
    return render(request, "myadmin/info.html", context)


def edit(request, sid=0):
    """执行信息编辑表单"""
    try:
        ob = Shop.objects.get(id=sid)
        context = {'shop': ob}
        return render(request, "myadmin/shop/edit.html", context)
    except Exception as e:
        print(e)
        context = {'info': "没有找到要修改的信息"}
        return render(request, "myadmin/info.html", context)


def update(request, sid=0):
    """执行信息修改表单"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST["name"]
        ob.phone = request.POST["phone"]
        ob.address = request.POST["address"]
        ob.status = request.POST["status"]
        # ob.cover_pic = request.POST["cover_pic"]
        # ob.banner_pic = request.POST["banner_pic"]
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功"}
    except Exception as e:
        print(e)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)
