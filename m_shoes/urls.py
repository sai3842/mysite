from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.mshoes_view,name='mshoes'),
    path('<str:name>',views.mshoes_view,name='views'),
     path("/product<int:no>", views.product_list, name="product_list"),
     path('/mshoes_view',views.show,name='show'),
     path('/view',views.brand_view,name='view'),
     path('/cart',views.cart_view,name='cart'),
     path('/del<int:num>',views.del_cart,name='del'),
     path('/logout',views.logout_view,name='logout'),
     path('/status',views.status,name='status'),
     path('/del',views.payment,name='pays')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)