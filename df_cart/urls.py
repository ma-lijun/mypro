
from django.conf.urls import url
from df_cart import views

urlpatterns = [
    url(r'^add/$', views.cart_add),
    url(r'^count/$', views.cart_count),  # 獲取購物車中商品的總數
]
