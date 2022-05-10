from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from rest_framework.views import APIView

from .models import User, Hall, Category, Food, Service, \
    User, Order, Comment, Customer, Regulation, Menu
from rest_framework import viewsets, generics, status, permissions
from .serializers import CustomerSerializer, HallSerializer, CategorySerializer, \
    OrderSerializer, ServiceSerializer, CommentSerializer, FoodSerializer, \
    MenuSerializer, CreateCommentSerializer
from .paginators import BasePaginator
from .change_price_halls import *
from .perms import CommentOwnerPermission

price_hall_now()


class CustomerViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)

    # @action(methods=['post'], detail=True, url_path='add-add-cus')
    # def add_in_cus(self, request, pk):
    #     user = self.get_object()
    #     customer = Customer.objects.create(phone_number="13214", user=user)
    #     customer.save()


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    pagination_class = BasePaginator

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(name__icontains=kw)

        return query

    @action(methods=['get'], detail=True, url_path='foods')
    def get_foods(self, request, pk):
        category = Category.objects.get(pk=pk)
        foods = category.foods.filter(active=True)

        kw = request.query_params.get('kw')
        if kw is not None:
            foods = foods.filter(name__icontains=kw)

        price = request.query_params.get('price')
        if price is not None:
            foods = foods.filter(price=price)

        return Response(data=FoodSerializer(foods, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class HallViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Hall.objects.filter(active=True)
    serializer_class = HallSerializer
    pagination_class = BasePaginator

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(name__icontains=kw)
            return query

        qty = self.request.query_params.get('qty')
        if qty:
            query = query.filter(capacity=qty)
            return query

        return query


# class FoodViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
#     queryset = Food.objects.filter(active=True)
#     serializer_class = FoodSerializer
#     pagination_class = BasePaginator
#
#     def get_queryset(self):
#         query = self.queryset
#
#         kw = self.request.query_params.get('kw')
#         if kw:
#             query = query.filter(name__icontains=kw)
#             return query
#
#         price = self.request.query_params.get('price')
#         if price:
#             query = query.filter(price=price)
#             return query
#
#         return query


class ServiceViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Service.objects.filter(active=True)
    serializer_class = ServiceSerializer
    pagination_class = BasePaginator

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(name__icontains=kw)
            return query

        price = self.request.query_params.get('price')
        if price:
            query = query.filter(price=price)
            return query

        return query


class MenuViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Menu.objects.filter(active=True)
    serializer_class = MenuSerializer


class OrderViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=True, url_path='time_organize')
    def choose_time_organize(self, request, pk):
        order = Order.objects.get(pk=pk)
        date = request.data.get('date')
        shift = int(request.data.get('shift'))

        if date and shift is not None:
            time_organize, _ = DateOfOrganization.objects.get_or_create(date=date, shift=shift)
            order.time_organize = time_organize
            order.save()

        return Response(self.serializer_class(order).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='choose-menu')
    def choose_menu(self, request, pk):
        order = Order.objects.get(pk=pk)
        m = request.data.get('menu')
        menu = Menu.objects.get(pk=m)

        if menu is not None:
            order.menu = menu
            order.save()
        return Response(self.serializer_class(order).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content, wedding=self.get_object(), customer=request.user)

            return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet, generics.CreateAPIView,
                     generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CreateCommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [CommentOwnerPermission()]

        return [permissions.AllowAny()]


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)
