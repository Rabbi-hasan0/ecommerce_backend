from django.urls import path, include
from .views import RegisterView, ProductViewSet, CartViewSet, OrderViewSet
from rest_framework import routers, viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Router theke product er sob URL include hobe
    path('', include(router.urls)), 
    
    # Auth Endpoints
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Cart Endpoints
    path('cart/', CartViewSet.as_view({'get': 'list'}), name='cart-detail'),
    path('cart/add/', CartViewSet.as_view({'post': 'add_to_cart'}), name='cart-add'),
    path('order/place/', OrderViewSet.as_view({'post': 'place_order'}), name='order-place'),
    
    #tracking path
    path('order/<int:pk>/cancel/', OrderViewSet.as_view({'post': 'cancel_order'}), name='order-cancel'),
    path('order/<int:pk>/status/', OrderViewSet.as_view({'patch': 'update_status'}), name='order-status-update'),
]