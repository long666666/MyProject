"""
后台管理子路由配置
"""
from django.urls import path
from test001.views import index

urlpatterns = [
    path("", index.index, name="test_index"),  # 后台首页
]
