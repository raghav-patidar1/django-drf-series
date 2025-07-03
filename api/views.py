from django.db.models import Max
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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


class UserOrderListAPIView(ListAPIView):
    queryset = Order.objects.prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    

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


    
