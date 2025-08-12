from django.db import models
from django.conf import settings
from decimal import Decimal

class Shop(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shops"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    subscription_plan = models.CharField(max_length=50, default="basic")  # basic, pro, enterprise
    subscription_expiry = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # External authentication reference
    provider_name = models.CharField(max_length=255, blank=True, null=True)
    provider_id = models.CharField(max_length=255, unique=True, blank=True, null=True)


    class Meta:
        unique_together = ("provider_name", "provider_id")
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        return self.name


class Service(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Labor only
    taxable = models.BooleanField(default=True)
    warranty_months = models.PositiveIntegerField(default=0)  # Default warranty

    def __str__(self):
        return f"{self.name} - {self.shop.name}"


class Part(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="parts")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # e.g., used, new, refurbished
    part_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    taxable = models.BooleanField(default=True)
    warranty_months = models.PositiveIntegerField(default=0)  # Default warranty
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.shop.name}"


class Employee(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="employees")
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)  # mechanic, receptionist, etc.
    phone_number = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='employee_pics/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # External authentication reference
    provider_name = models.CharField(max_length=255, blank=True, null=True)
    provider_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    # Optional link to Django's user model (if needed later)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ("provider_name", "provider_id")
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f"{self.name} - {self.shop.name}"


class Customer(models.Model):
    shop = models.ForeignKey(
        'Shop', 
        on_delete=models.CASCADE, 
        related_name="customers"
    )

    # External authentication reference
    provider_name = models.CharField(max_length=255, blank=True, null=True)
    provider_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    # Optional link to Django's user model (if needed later)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        blank=True,
        null=True
    )

    # Customer info
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ("provider_name", "provider_id")
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

class Appointment(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="appointments")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ], default="pending")

    def __str__(self):
        service_name = self.service.name if self.service else "No Service"
        return f"{self.customer.name} - {service_name}"


class RepairOrder(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="repair_orders")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="repair_orders")
    services = models.ManyToManyField(Service, through="RepairOrderService")
    parts = models.ManyToManyField(Part, through="RepairOrderPart")

    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))

    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    date_created = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(blank=True, null=True)

    def calculate_total_cost(self):
        # Labor cost
        labor_total = sum(s.labor_cost for s in self.services.all())

        # Parts cost
        parts_total = sum(item.part.unit_price * item.quantity for item in self.repair_order_parts.all())

        subtotal = labor_total + parts_total

        # Discounts
        discount_value = Decimal("0.00")
        if self.discount_percent > 0:
            discount_value = (subtotal * self.discount_percent) / Decimal("100")
        elif self.discount_amount > 0:
            discount_value = self.discount_amount

        # Taxable portion
        taxable_services_total = sum(s.labor_cost for s in self.services.all() if s.taxable)
        taxable_parts_total = sum(item.part.unit_price * item.quantity for item in self.repair_order_parts.all() if item.part.taxable)
        taxable_amount = (taxable_services_total + taxable_parts_total) - discount_value

        # Tax
        tax_value = (taxable_amount * self.tax_percent) / Decimal("100") if self.tax_percent > 0 else Decimal("0.00")

        return subtotal - discount_value + tax_value

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total_cost()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Repair Order #{self.pk} - {self.customer.name}"


class RepairOrderService(models.Model):
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="repair_order_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    warranty_override_months = models.PositiveIntegerField(null=True, blank=True)


class RepairOrderPart(models.Model):
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="repair_order_parts")
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    warranty_override_months = models.PositiveIntegerField(null=True, blank=True)

    @property
    def total_price(self):
        return self.part.unit_price * self.quantity
