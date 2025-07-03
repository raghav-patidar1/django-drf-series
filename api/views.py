from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Order, Product
from .serializers import (OrderSerializer, ProductInfoSerializer,
                          ProductSerializer)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related('items', 'items__product')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    
    data = {
        'products': products,
        'total_product_count': len(products),
        'max_product_price': products.aggregate(
            max_price=Max('price')
        )['max_price']
    }

    serializer = ProductInfoSerializer(data)
    return Response(serializer.data)