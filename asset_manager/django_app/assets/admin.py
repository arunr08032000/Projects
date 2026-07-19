from django.contrib import admin
from .models import Category, Asset, Checkout, MaintenanceLog


class CheckoutInline(admin.TabularInline):
    model = Checkout
    extra = 0
    readonly_fields = ("checkout_date",)


class MaintenanceLogInline(admin.TabularInline):
    model = MaintenanceLog
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "serial_number",
        "category",
        "status",
        "purchase_date",
        "price",
        "updated_at",
    )
    list_filter = ("status", "category", "purchase_date")
    search_fields = ("name", "serial_number", "description")
    inlines = [CheckoutInline, MaintenanceLogInline]
    date_hierarchy = "purchase_date"


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "employee_name",
        "employee_email",
        "checkout_date",
        "expected_return_date",
        "actual_return_date",
    )
    list_filter = ("checkout_date", "actual_return_date")
    search_fields = (
        "employee_name",
        "employee_email",
        "asset__name",
        "asset__serial_number",
    )
    date_hierarchy = "checkout_date"


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ("asset", "description", "cost", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("description", "asset__name", "asset__serial_number")
    date_hierarchy = "start_date"
