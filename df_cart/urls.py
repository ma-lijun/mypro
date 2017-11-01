
from django.conf.urls import url
from df_cart import views

urlpatterns = [
    url(r'^$', views.cart_show),
    url(r'^add/$', views.cart_add),
    url(r'^count/$', views.cart_count),  # 獲取購物車中商品的總數
    url(r'^update/$', views.cart_update),  # 更新购物车中商品的总数

    url(r'^del/$', views.cart_del),  # 删除购物车记录

]
