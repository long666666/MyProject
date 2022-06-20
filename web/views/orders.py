"""购物车信息管理视图文件"""
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator

from datetime import datetime
from myadmin.models import Orders, OrderDetail, Payment, User


# Create your views here.
def index(request, pIndex=1):
    """浏览订单信息"""
    """首页用户列表展示"""
    umod = Orders.objects
    # 获取当前店铺id
    sid = request.session['shopinfo']['id']
    ulist = umod.filter(shop_id=sid)  # 排除状态为9（已注销）

    # 获取并判断搜索条件
    mywhere = []  # 用于维持搜索,用于存放搜索值条件
    status = request.GET.get("status", '')
    if status != '':
        ulist = ulist.filter(status=status)  # 模糊查询
        mywhere.append("status=" + status)
    # 还可以加入其他条件，如状态等，方法一致，条件加入mywhere[]即可

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 10)  # 以每页五条数据分页
    maxpages = page.num_pages  # 获取最大页数
    print(maxpages)
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list = page.page(pIndex)  # 获取当前页信息
    plist = page.page_range  # 获取页面列表信息

    for vo in list:
        if vo.user_id == 0:
            vo.nickname = '无'
        else:
            user = User.objects.only('nickname').get(id=vo.user_id)
            vo.nickname = user.nickname

    context = {"orders_list": list, "plist": plist, "pIndex": pIndex, "maxpages": maxpages, "mywhere": mywhere}

    return render(request, "web/list.html", context)


def insert(request):
    """执行订单添加"""
    try:
        # 执行订单信息的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']  # 店铺id号
        od.member_id = 0  # 会员id
        od.user_id = request.session['webuser']['id']  # 操作员id
        od.money = request.session['total_money']  # 金额
        od.status = 1  # 订单状态:1过行中/2无效/3已完成
        od.payment_status = 2  # 支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        od.save()

        # 支付信息添加
        op = Payment()
        op.order_id = od.id  # 订单id号
        op.member_id = 0  # 会员id
        op.type = 2  # 付款方式：1会员付款/2收银收款
        op.bank = request.GET.get("bank", 3)  # 收款银行渠道:1微信/2余额/3现金/4支付宝
        op.money = request.session['total_money']  # 支付金额
        op.status = 1  # 支付状态:1未支付/2已支付/3已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间并格式化
        op.save()

        # 执行订单详情添加
        cartlist = request.session.get('cartlist', {})  # 获取购物车中的菜品信息
        # 遍历购物车中的菜品，并添加到订单详情中
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id  # 订单id
            ov.product_id = item['id']  # 菜品id
            ov.product_name = item['name']  # 菜品名称
            ov.price = item['price']  # 单价
            ov.quantity = item['num']  # 数量
            ov.status = 1  # 状态:1正常/9删除
            ov.save()

        del request.session['cartlist']
        del request.session['total_money']
        return HttpResponse("Y")
    except Exception as e:
        print(e)
        return HttpResponse("N")


def detail(request):
    """加载订单详情"""
    oid = request.GET.get('oid', 0)
    dlist = OrderDetail.objects.filter(order_id=oid)
    context = {"detaillist": dlist}
    return render(request, "web/detail.html", context)


def status(request):
    """更改购物车商品操作"""
    try:
        oid = request.GET.get('oid', 0)
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET.get('status')
        ob.save()
        return HttpResponse("Y")
    except Exception as e:
        print(e)
        return HttpResponse("N")


def log_out(request):
    pass
