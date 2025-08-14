from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'shops', views.ShopViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'parts', views.PartViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'repair-orders', views.RepairOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
