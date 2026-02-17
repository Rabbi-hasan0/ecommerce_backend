from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Product, Cart, CartItem
from rest_framework import generics, viewsets, status
from .serializers import UserSerializer, ProductSerializer, CartSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .permissions import IsAdminUser, IsCustomerUser  # Amra age jeta baniyechi


## Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


## For only admin accessable
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        # Read-only permission sobai pabe (Customer-ra product dekhte parbe)
        # Kintu Create, Update, Delete sudhu Admin korte parbe
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]


#Cart view
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsCustomerUser]
    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def add_to_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        product = Product.objects.get(id=product_id)
        
        # Check stock before adding to cart
        if product.stock < quantity:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
            
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            
        cart_item.save()
        return Response({"message": "Added to cart"}, status=status.HTTP_200_OK)



from django.db import transaction
from .models import Order, OrderItem, Cart

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsCustomerUser]

    @transaction.atomic
    def place_order(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()
            
            if not cart_items:
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            total_amount = 0
            order_items_to_create = []

            # 1. Validation & Calculation
            for item in cart_items:
                if item.product.stock < item.quantity:
                    return Response({
                        "error": f"Not enough stock for {item.product.name}"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                total_amount += item.product.price * item.quantity
            
            # 2. Create Order
            order = Order.objects.create(user=user, total_amount=total_amount)

            # 3. Process items and Update Stock
            for item in cart_items:
                # Deduct Stock
                product = item.product
                product.stock -= item.quantity
                product.save()

                # Prepare OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    unit_price=product.price
                )

            # 4. Clear Cart
            cart_items.delete()

            return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({"error": "No cart found"}, status=status.HTTP_404_NOT_FOUND)


from django.utils import timezone
from datetime import timedelta

# OrderViewSet-er bhetore add koro
def cancel_order(self, request, pk=None):
    user = request.user
    try:
        order = Order.objects.get(pk=pk, user=user)
        
        # logic: 24 ghontay 3 barer beshi cancel korle block
        one_day_ago = timezone.now() - timedelta(days=1)
        cancel_count = Order.objects.filter(
            user=user, 
            status='Cancelled', 
            created_at__gte=one_day_ago
        ).count()

        if cancel_count >= 3:
            return Response(
                {"error": "Too many cancellations. Please contact support."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        if order.status == 'Pending':
            with transaction.atomic():
                order.status = 'Cancelled'
                order.save()
                
                # Stock refund koro
                for item in order.items.all():
                    product = item.product
                    product.stock += item.quantity
                    product.save()
                    
            return Response({"message": "Order cancelled and stock refunded"})
        else:
            return Response({"error": "Only pending orders can be cancelled"}, status=400)
            
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)
    

# OrderViewSet-er bhetore
def update_status(self, request, pk=None):
    if request.user.role != 'admin':
        return Response({"detail": "Not allowed"}, status=403)
        
    order = Order.objects.get(pk=pk)
    new_status = request.data.get('status') # Shipped/Delivered
    if new_status in ['Shipped', 'Delivered']:
        order.status = new_status
        order.save()
        return Response({"message": f"Order status updated to {new_status}"})
    return Response({"error": "Invalid status"}, status=400)



