"""
前台子路由配置
"""
from django.contrib import admin
from django.urls import path, include
from web.views import index, cart, orders

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", index.index, name="index"),

    path("log_in/", index.log_in, name="web_log_in"),
    path("do_login/", index.do_login, name="web_do_login"),
    path("log_out/", index.log_out, name="web_log_out"),
    path("verify/", index.verify, name="web_verify"),

    # 为url路由提娜佳请求前缀,凡是带此前缀的url地址必须登陆后才可以访问
    path('web/', include([
        path('', index.webindex, name="web_index"),  # 前台大堂点餐首页
    ])),

    # 购物车信息管理路由
    path("cart/add/<str:pid>", cart.add, name="web_cart_add"),
    path("cart/delete/<str:pid>", cart.delete, name="web_cart_delete"),
    path("cart/clear", cart.clear, name="web_cart_clear"),
    path("cart/change", cart.change, name="web_cart_change"),

    # 订单信息管理路由
    path("orders/<int:pIndex>", orders.index, name="web_orders_index"),
    path("orders/insert", orders.insert, name="web_orders_insert"),
    path("orders/detail", orders.detail, name="web_orders_detail"),
    path("orders/status", orders.status, name="web_orders_status"),
]
