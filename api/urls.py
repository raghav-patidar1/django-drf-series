from django.urls import path

from . import views


urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<uuid:product_id>', views.ProductDetailAPIView.as_view()),
    path('products/info', views.product_info),
    path('orders/', views.UserOrderListAPIView.as_view()),
]