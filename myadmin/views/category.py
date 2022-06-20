"""
菜品类别信息管理：增、删、改、查

"""
from django.shortcuts import render, redirect, HttpResponse
from myadmin.models import Category, Shop
from django.core.paginator import Paginator
from django.urls import reverse
from _datetime import datetime
from django.http import JsonResponse


def index(request, pIndex=1):
    """首页菜品类别列表展示"""
    cmod = Category.objects
    clist = cmod.filter(status__lt=9)  # 排除状态为9（已注销）

    # 获取并判断搜索条件
    mywhere = []  # 用于维持搜索,用于存放搜索值条件
    kw = request.GET.get("keyword")
    if kw:
        clist = clist.filter(name__contains=kw)  # 模糊查询
        mywhere.append("keyword=" + kw)
    # 还可以加入其他条件，如状态等，方法一致，条件加入mywhere[]即可

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(clist, 10)  # 以每页五条数据分页
    maxpages = page.num_pages  # 获取最大页数
    print(maxpages)
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list = page.page(pIndex)  # 获取当前页信息
    plist = page.page_range  # 获取页面列表信息

    # 遍历当前菜品分类信息并封装对应的店铺信息
    for vo in list:
        print("店铺id:", vo.shop_id)
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name

    context = {"category_list": list, "plist": plist, "pIndex": pIndex, "maxpages": maxpages, "mywhere": mywhere}

    return render(request, "myadmin/category/index.html", context)


def loadCategory(request, sid):
    clist = Category.objects.filter(status__lt=9, shop_id=sid).values("id", "name")
    # 返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data': list(clist)})


def add(request):
    """加载信息添加表单"""
    slist = Shop.objects.values("id", "name")
    context = {"shoplist": slist}
    return render(request, "myadmin/category/add.html", context)


def insert(request):
    """执行信息添加"""
    try:
        ob = Category()
        ob.shop_id = request.POST["shop_id"]
        ob.name = request.POST["name"]
        ob.status = 1

        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        ob.save()
        context = {'info': "添加成功"}
    except Exception as e:
        print(e)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, cid=0):
    """执行信息删除"""
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        context = {'info': "删除成功"}
    except Exception as e:
        print(e)
        context = {'info': "删除失败"}
    return render(request, "myadmin/info.html", context)


def edit(request, cid=0):
    """执行信息编辑表单"""
    try:
        ob = Category.objects.get(id=cid)
        context = {'category': ob}
        slist = Shop.objects.values("id", "name")
        context['shoplist'] = slist
        return render(request, "myadmin/category/edit.html", context)
    except Exception as e:
        print(e)
        context = {'info': "没有找到要修改的信息"}
        return render(request, "myadmin/info.html", context)


def update(request, cid=0):
    """执行信息修改表单"""
    try:
        ob = Category.objects.get(id=cid)
        ob.shop_id = request.POST["shop_id"]
        ob.name = request.POST["name"]
        ob.status = request.POST["status"]
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "修改成功"}
    except Exception as e:
        print(e)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)
