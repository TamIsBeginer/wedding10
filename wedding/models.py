from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to="static/users/%Y/%m")


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(ModelBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Hall(ModelBase):  # Sanh Cuoi
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="static/halls/%Y/%m")
    morning_price = models.FloatField(null=True, blank=True)
    noon_price = models.FloatField(null=True, blank=True)
    night_price = models.FloatField(null=True, blank=True)
    free = models.BooleanField(default=True)
    time_organize = models.ManyToManyField('DateOfOrganization', through='HallOrganize')

    def __str__(self):
        return self.name


class HallOrganize(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    time_organize = models.ForeignKey('DateOfOrganization', on_delete=models.CASCADE)
    price = models.FloatField()

    class Meta:
        unique_together = ('hall', 'time_organize')

    def __str__(self):
        return f'{self.hall} - {self.time_organize}'


class Category(ModelBase):  # Loai mon an
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Food(ModelBase):  # Mon An
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name="foods", null=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=True, blank=True, upload_to="static/foods/%Y/%m")

    def __str__(self):
        return self.name


class Menu(ModelBase):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="static/menu/%Y/%m")
    foods = models.ManyToManyField(Food)

    def __str__(self):
        return self.name


class Service(ModelBase):  # Dich vu
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True, upload_to="static/services/%Y/%m")

    def __str__(self):
        return self.name


# class TimeFrame(ModelBase):  # Khung giờ
#     hour = models.IntegerField()
#     minute = models.IntegerField()
#     second = models.IntegerField()
#     price = models.FloatField()
#
#     def __str__(self):
#         return f'{self.hour}:{self.minute}:{self.second}'
#
#     class Meta:
#         unique_together = ('hour', 'minute', 'second')

class Regulation(ModelBase):
    name = models.CharField(max_length=20, null=True)
    morning_price = models.FloatField(null=True)
    noon_price = models.FloatField(null=True)
    night_price = models.FloatField(null=True)
    weekend_price = models.FloatField(null=True)

    def __str__(self):
        return self.name


class DateOfOrganization(models.Model):  # Ngay to chuc
    date = models.DateField(null=True)
    morning, noon, night = range(3)
    shift_choices = [
        (morning, 'Buổi sáng'),
        (noon, 'Buổi trưa'),
        (night, 'Buổi tối'),
    ]
    shift = models.PositiveSmallIntegerField(choices=shift_choices, default=morning)
    regulation = models.ForeignKey(Regulation, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('date', 'shift')

    def __str__(self):
        return f'{self.date} Shift: {self.shift}'


class Order(ModelBase):  # Phieu dat tiec
    customer = models.ForeignKey(Customer, related_name="receipts", on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(User, related_name="receipts", on_delete=models.CASCADE, null=True)
    hall = models.ForeignKey(Hall, related_name="receipts", null=True, on_delete=models.SET_NULL)
    service = models.ManyToManyField(Service, related_name="receipts")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, null=True)
    time_organize = models.ForeignKey(DateOfOrganization, related_name="receipts",
                                      on_delete=models.CASCADE)  # Ngày tổ chức
    # time_frame = models.ForeignKey(TimeFrame, related_name="receipts", null=True, on_delete=models.SET_NULL)
    number_of_table = models.IntegerField(null=True)  # Số lượng bàn
    groom_name = models.CharField(max_length=100, null=True)  # Tên chú rể
    bride_name = models.CharField(max_length=100, null=True)  # Tên cô dâu

    # regulation = models.ForeignKey('Regulation', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.date_of_organization}-{self.customer}-{self.hall}'


# class OrderFood(models.Model):  # Chi tiet combo
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     food = models.ForeignKey(Food, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#
#     def __str__(self):
#         return f'{self.order} - {self.food}'
#
#     class Meta:
#         ordering = ['order', 'food']


class Comment(ModelBase):
    content = models.TextField()
    wedding = models.ForeignKey(Order, related_name='comments', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
