import os
import sys
import datetime
from decimal import Decimal

# Add django project to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

import django

django.setup()

from assets.models import Category, Asset, Checkout, MaintenanceLog


def seed_db():
    print("[Seed] Seeding database categories...")

    # 1. Create categories
    cats = {
        "Laptops": "Company-issued workstations and notebooks.",
        "Monitors": "High-resolution desktop displays.",
        "Mobile Devices": "Work phones and tablets.",
        "Peripherals": "Keyboards, mice, dock stations, and accessories.",
    }

    cat_objs = {}
    for name, desc in cats.items():
        obj, created = Category.objects.get_or_create(
            name=name, defaults={"description": desc}
        )
        cat_objs[name] = obj
        if created:
            print(f"  Category '{name}' created.")
        else:
            print(f"  Category '{name}' already exists.")

    # 2. Create assets
    print("[Seed] Seeding database assets...")

    assets_data = [
        {
            "name": 'MacBook Pro 16" (M3 Max)',
            "serial_number": "SNDJ838491823",
            "category": cat_objs["Laptops"],
            "status": "AVAILABLE",
            "purchase_date": datetime.date(2026, 1, 15),
            "price": Decimal("3499.00"),
            "description": "Premium development workstation. 64GB RAM, 1TB SSD.",
        },
        {
            "name": 'Dell UltraSharp 32" 4K Monitor',
            "serial_number": "SNMON92837482",
            "category": cat_objs["Monitors"],
            "status": "CHECKED_OUT",
            "purchase_date": datetime.date(2025, 11, 20),
            "price": Decimal("799.00"),
            "description": "Color-accurate 4K monitor. Connected via USB-C Hub.",
        },
        {
            "name": 'Apple iPad Pro 11"',
            "serial_number": "SNMOB19283745",
            "category": cat_objs["Mobile Devices"],
            "status": "MAINTENANCE",
            "purchase_date": datetime.date(2026, 3, 1),
            "price": Decimal("999.00"),
            "description": "QA Testing tablet. Cracked screen undergoing vendor service.",
        },
        {
            "name": "Keychron K2 Keyboard",
            "serial_number": "SNKB748392019",
            "category": cat_objs["Peripherals"],
            "status": "AVAILABLE",
            "purchase_date": datetime.date(2025, 8, 10),
            "price": Decimal("99.00"),
            "description": "Wireless mechanical keyboard (Brown switches).",
        },
    ]

    asset_objs = []
    for asset_info in assets_data:
        obj, created = Asset.objects.get_or_create(
            serial_number=asset_info["serial_number"], defaults=asset_info
        )
        asset_objs.append(obj)
        if created:
            print(f"  Asset '{obj.name}' created.")
        else:
            # If asset already exists, use it
            print(f"  Asset '{obj.name}' already exists.")

    # 3. Create a Checkout record for the checked-out asset
    checkout_asset = Asset.objects.filter(serial_number="SNMON92837482").first()
    if (
        checkout_asset
        and not checkout_asset.checkouts.filter(actual_return_date=None).exists()
    ):
        Checkout.objects.create(
            asset=checkout_asset,
            employee_name="Alice Vance",
            employee_email="alice@company.com",
            checkout_date=datetime.date(2026, 6, 12),
            expected_return_date=datetime.date(2026, 8, 12),
            notes="Assigned for multi-display workstation setup.",
        )
        print("  Added active checkout record for Dell Monitor.")

    # 4. Create an active Maintenance log for the maintenance asset
    maint_asset = Asset.objects.filter(serial_number="SNMOB19283745").first()
    if maint_asset and not maint_asset.maintenance_logs.filter(end_date=None).exists():
        MaintenanceLog.objects.create(
            asset=maint_asset,
            description="Screen replacements and body diagnostics (authorized service center).",
            cost=Decimal("199.00"),
            start_date=datetime.date(2026, 7, 10),
        )
        print("  Added active maintenance log for Apple iPad Pro.")

    print("[Seed] Seeding completed successfully!")


if __name__ == "__main__":
    seed_db()
