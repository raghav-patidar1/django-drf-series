from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock')

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return price


class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price',
    )

    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')


class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'order_id', 
            'user', 
            'created_at',
            'status', 
            'items', 
            'total_price'
        )

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)


class ProductInfoSerializer(serializers.Serializer):
    # Serialize all products with total product count and max_price as aggregated fields
    products = ProductSerializer(many=True)
    total_product_count = serializers.IntegerField()
    max_product_price = serializers.FloatField()
