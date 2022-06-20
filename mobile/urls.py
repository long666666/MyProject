"""
移动端子路由配置
"""
from django.contrib import admin
from django.urls import path, include
from mobile.views import index, member

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", index.index, name="mobile_index"),  # 移动端首页

    # 会员注册或登录
    path("register/", index.register, name="mobile_register"),  # 移动端会员注册登录表单页
    path("do_register/", index.do_register, name="mobile_do_register"),  # 执行注册或登录

    # 店铺选择
    path("shop/", index.shop, name="mobile_shop"),  # 移动端店铺选项页
    path("shop/select", index.select_shop, name="mobile_select_shop"),  # 执行移动端店铺选择
    path("shop/shop_rest", index.shop_rest, name="mobile_shop_rest"),  # 执行移动端店铺选择

    # 订单处理
    path("orders/add", index.add_orders, name="mobile_add_orders"),  # 执行移动端店铺选择

    # 会员中心
    path('member/', member.index, name="mobile_member_index"),  # 会员中心首页
    path('member/orders', member.orders, name="mobile_member_orders"),  # 加载会员中心订单
    path('member/detail', member.detail, name="mobile_member_detail"),  # 加载会员订单详情
    path('member/log_out', member.log_out, name="mobile_member_log_out"),  # 执行退出

]
