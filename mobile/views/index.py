from django.shortcuts import render, redirect, HttpResponse
from myadmin.models import Shop, Category, Product, Member
from django.db.models import Q
from django.urls import reverse
from datetime import datetime


def index(request):
    sid = request.GET.get("sid", 1)
    # print("sid", sid)
    sob = Shop.objects.get(id=sid)
    status = sob.status  # 获取店铺状态
    cob = Category.objects.all()  # 获取所有菜品类型
    # print("cob", cob)
    plist = []  # 用于存放菜品信息

    for c in cob:  # 遍历当前店铺的每个菜品类型
        pob = Product.objects.filter(Q(shop_id=sid) & Q(category_id=c.id)).values("name", "price", "shop_id", "status",
                                                                                  "cover_pic")  # 从所有菜品中获取当前类型的菜品
        for p in pob:  # 遍历每个菜品
            p['shop_id'] = Shop.objects.get(id=sid).name  # 根据菜品中的shop_id获取店铺名称
        plist.append(pob)  # 将包含各自菜品的菜品类型加入列表

    print("plist", plist)
    context = {"category": cob, "product": plist}
    if status == 2:
        return redirect(reverse("mobile_shop_rest"))
    return render(request, "mobile/index.html", context)


def register(request):
    return render(request, "mobile/register.html")


def do_register(request):
    vcode = '1234'
    mobile = request.POST['mobile']
    code = request.POST['code']
    print(mobile, code)

    if vcode != code:
        context = {"info": "验证码错误"}
        return render(request, "mobile/register.html", context)
    # 根据手机号码获取当前会员信息
    try:
        member = Member.objects.get(mobile=mobile)
        # 检验当前会员状态
        if member.status == 1:
            request.session['mobileuser'] = member.toDict()
            print("登录成功")
            return redirect(reverse('mobile_index'))
        else:
            context = {"info": "该用户被冻结"}
    except Exception as e:
        print(e)
        # context = {"info": "该用户不存在"}
        ob = Member()
        ob.nickname = "顾客"
        ob.avatar = "moren.png"
        ob.status = 1
        ob.mobile = mobile
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        return render(request, "mobile/register.html")


def shop(request):
    slist = Shop.objects.values("id", "name", "phone", "address", "cover_pic", "status")
    context = {"shoplist": slist}
    return render(request, "mobile/shop.html", context)


def select_shop(request):
    pass
    # return render(request, "mobile/index.html",)


def add_orders(request):
    pass
    # return render(request, "mobile/add_orders.html")


def shop_rest(request):
    return render(request, "mobile/shop_rest.html")
