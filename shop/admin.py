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
    list_display = ('name', 'category', 'part_number', 'unit_price', 'stock_quantity')
    search_fields = ('name', 'part_number')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'shop', 'phone_number')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'shop')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'date', 'status')

@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'shop', 'total_cost', 'date_created')
