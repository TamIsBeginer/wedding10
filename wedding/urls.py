from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='customers', viewset=views.CustomerViewSet, basename='customer')
router.register(prefix='halls', viewset=views.HallViewSet, basename='hall')
router.register(prefix='categories', viewset=views.CategoryViewSet, basename='category')
router.register(prefix='services', viewset=views.ServiceViewSet, basename='service')
router.register(prefix='order', viewset=views.OrderViewSet, basename='order')
router.register(prefix='comment', viewset=views.CommentViewSet)
router.register(prefix='menus', viewset=views.MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view())
]
