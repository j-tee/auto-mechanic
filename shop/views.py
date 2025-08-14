from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Shop, Service, Part, Employee, Customer, Appointment, RepairOrder
from .serializers import (
    ShopSerializer, ServiceSerializer, PartSerializer,
    EmployeeSerializer, CustomerSerializer, AppointmentSerializer,
    RepairOrderSerializer
)


class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset with filtering, searching, and ordering."""
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'   # Allow filtering on all fields unless overridden
    search_fields = '__all__'      # Allow searching on all fields unless overridden
    ordering_fields = '__all__'    # Allow ordering on all fields unless overridden
    ordering = ['id']              # Default ordering


class ShopViewSet(BaseViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    search_fields = ['name', 'owner__username']


class ServiceViewSet(BaseViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    search_fields = ['name', 'shop__name']


class PartViewSet(BaseViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    search_fields = ['name', 'category', 'part_number']


class EmployeeViewSet(BaseViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    search_fields = ['name', 'role', 'shop__name']


class CustomerViewSet(BaseViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ['name', 'phone_number', 'email', 'shop__name']


class AppointmentViewSet(BaseViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    search_fields = ['customer__name', 'service__name', 'status']


class RepairOrderViewSet(BaseViewSet):
    queryset = RepairOrder.objects.all()
    serializer_class = RepairOrderSerializer
    search_fields = ['customer__name', 'shop__name']
