"""
菜品信息管理：增、删、改、查

"""
from django.shortcuts import render, redirect, HttpResponse
from myadmin.models import Category, Shop, Product
from django.core.paginator import Paginator
from django.urls import reverse
from _datetime import datetime
import time, os


def index(request, pIndex=1):
    """首页菜品列表展示"""
    pmod = Product.objects
    plist = pmod.filter(status__lt=9)  # 排除状态为9（已注销）

    # 获取并判断搜索条件
    mywhere = []  # 用于维持搜索,用于存放搜索值条件
    kw = request.GET.get("keyword", None)
    if kw:
        plist = plist.filter(name__contains=kw)  # 模糊查询
        mywhere.append("keyword=" + kw)
    # 还可以加入其他条件，如状态等，方法一致，条件加入mywhere[]即可
    # 菜品类别搜索条件
    cid = request.GET.get("category_id", None)
    if cid:
        plist = plist.filter(category_id=cid)  # 模糊查询
        mywhere.append("category_id=" + cid)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(plist, 10)  # 以每页五条数据分页
    maxpages = page.num_pages  # 获取最大页数
    print(maxpages)
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list = page.page(pIndex)  # 获取当前页信息
    plist = page.page_range  # 获取页面列表信息

    # 遍历当前菜品分类信息并封装对应的店铺信息和菜品类别信息
    for vo in list:
        print("店铺id:", vo.shop_id)
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name
        cob = Category.objects.get(id=vo.category_id)
        vo.category = cob.name

    context = {"product_list": list, "plist": plist, "pIndex": pIndex, "maxpages": maxpages, "mywhere": mywhere}

    return render(request, "myadmin/product/index.html", context)


def add(request):
    """加载信息添加表单"""
    # 获取当前店铺信息，菜品种类信息
    slist = Shop.objects.values("id", "name")
    context = {"shoplist": slist}
    clist = Category.objects.values("id", "name")
    context["categorylist"] = clist
    return render(request, "myadmin/product/add.html", context)


def insert(request):
    """执行信息添加"""
    try:
        # 菜品封面图片上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/product/" + cover_pic, "wb+")
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        ob = Product()
        ob.shop_id = request.POST["shop_id"]
        ob.category_id = request.POST["category_id"]
        ob.name = request.POST["name"]
        ob.price = request.POST["price"]
        ob.cover_pic = cover_pic
        ob.status = 1

        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        ob.save()
        context = {'info': "添加成功"}
    except Exception as e:
        print(e)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, pid=0):
    """执行信息删除"""
    try:
        ob = Product.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        context = {'info': "删除成功"}
    except Exception as e:
        print(e)
        context = {'info': "删除失败"}
    return render(request, "myadmin/info.html", context)


def edit(request, pid=0):
    """执行信息编辑表单"""
    try:
        ob = Product.objects.get(id=pid)
        context = {'product': ob}

        slist = Shop.objects.values("id", "name")
        context['shoplist'] = slist
        clist = Category.objects.values("id", "name")
        context['category'] = clist
        return render(request, "myadmin/product/edit.html", context)
    except Exception as e:
        print(e)
        context = {'info': "没有找到要修改的信息"}
        return render(request, "myadmin/info.html", context)


def update(request, pid=0):
    """执行信息修改表单"""
    try:
        # 获取原图片
        oldpicname = request.POST['oldpicname']
        # 图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            cover_pic = oldpicname
        else:
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/product/" + cover_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

        ob = Product.objects.get(id=pid)
        ob.shop_id = request.POST["shop_id"]
        ob.category_id = request.POST["category_id"]
        ob.name = request.POST["name"]
        ob.status = request.POST["status"]
        ob.price = request.POST["price"]
        ob.cover_pic = cover_pic
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功"}

        # 判断并删除老图片
        if myfile:
            os.remove("./static/uploads/product/" + oldpicname)
    except Exception as e:
        print(e)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)
