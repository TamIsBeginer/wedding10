from django.contrib import admin
from .models import User, Hall, Category, Food, Service, \
    DateOfOrganization, Order, Customer,\
    Regulation, HallOrganize, Menu


class WeddingAdmin(admin.ModelAdmin):
    search_fields = ['hall__name', 'hall__id', 'date_of_organization__shift']


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']


admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(HallOrganize)
admin.site.register(Regulation)
admin.site.register(Hall)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Menu)
admin.site.register(Service)
admin.site.register(Order, WeddingAdmin)
admin.site.register(DateOfOrganization)
