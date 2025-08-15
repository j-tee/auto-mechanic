from django.contrib import admin
from typing import Type
# Register your models here.
from .models import Shop, Service, Part, Employee, Customer, Appointment, RepairOrder


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'subscription_plan', 'created_at')
    search_fields = ('name', 'owner__username')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'labor_cost', 'taxable')


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'part_number',
                    'unit_price', 'stock_quantity')
    search_fields = ('name', 'part_number')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'shop', 'phone_number')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Removed 'shop' because Customer is no longer linked directly to a shop
    list_display = ("name", "phone_number", "email", "total_vehicles")


@admin.display(description="Vehicles", ordering='vehicles')
def total_vehicles(self, obj):
    return obj.vehicles.count()


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "get_customer_name",
                    "reported_problem", "date", "status")

    @admin.display(description="Customer")
    def get_customer_name(self, obj):
        return obj.vehicle.customer.name


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "get_customer_name", "get_shop",
                    "vehicle", "total_cost", "date_created")

    @admin.display(description="Customer")
    def get_customer_name(self, obj):
        return obj.vehicle.customer.name

    @admin.display(description="Shop")
    def get_shop(self, obj):
        # Assumes at least one service exists; otherwise returns None
        first_service = obj.services.first()
        return first_service.shop if first_service else None
