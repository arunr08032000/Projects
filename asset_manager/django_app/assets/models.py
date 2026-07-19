from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Asset(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("CHECKED_OUT", "Checked Out"),
        ("MAINTENANCE", "Maintenance"),
        ("RETIRED", "Retired"),
    ]

    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="assets"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="AVAILABLE"
    )
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"


class Checkout(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="checkouts")
    employee_name = models.CharField(max_length=150)
    employee_email = models.EmailField()
    checkout_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.asset.name} checked out by {self.employee_name}"


class MaintenanceLog(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="maintenance_logs"
    )
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Maintenance for {self.asset.name} on {self.start_date}"
