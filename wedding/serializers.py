from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, Hall, Service, Category, Food, \
    DateOfOrganization, User, Customer, \
    Order, Comment, Menu
from django.contrib.auth.models import Group


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }, 'avatar': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.is_customer = True
        group = Group.objects.get(pk=1)
        user.save()
        user.groups.add(group)
        customer = Customer(user=user)
        customer.save()
        return user

    # def create(self, validated_data):
    # password = make_password(validated_data['password'])
    # is_customer = True
    # is_employee = False
    # is_staff = False
    # # groups = ['Customer']
    # user = User.objects.create_user(validated_data['username'], password, is_customer=is_customer,
    #                                 is_employee=is_employee, is_staff=is_staff)
    # return user


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'name', 'capacity', 'free', 'image', 'created_date', 'morning_price', 'noon_price', 'night_price']
        extra_kwargs = {
            'free': {
                'read_only': True
            }
        }


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'price', 'image', 'category']


class MenuSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True)

    class Meta:
        model = Menu
        fields = ['id', 'name', 'foods', 'image']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_date']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ['active']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'hall', 'menu', 'time_organize', 'number_of_table', 'groom_name', 'bride_name']


class CommentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'customer']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'wedding', 'customer']
