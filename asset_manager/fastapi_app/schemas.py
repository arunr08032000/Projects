from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal


# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# Checkout schemas
class CheckoutBase(BaseModel):
    employee_name: str = Field(..., max_length=150)
    employee_email: EmailStr
    expected_return_date: date
    notes: Optional[str] = None


class CheckoutCreate(CheckoutBase):
    pass


class Checkout(CheckoutBase):
    id: int
    asset_id: int
    checkout_date: date
    actual_return_date: Optional[date] = None

    class Config:
        from_attributes = True


# MaintenanceLog schemas
class MaintenanceLogBase(BaseModel):
    description: str
    cost: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    start_date: date
    end_date: Optional[date] = None


class MaintenanceLogCreate(MaintenanceLogBase):
    pass


class MaintenanceLog(MaintenanceLogBase):
    id: int
    asset_id: int

    class Config:
        from_attributes = True


# Asset schemas
class AssetBase(BaseModel):
    name: str = Field(..., max_length=200)
    serial_number: str = Field(..., max_length=100)
    category_id: int
    status: str = Field(
        default="AVAILABLE", pattern="^(AVAILABLE|CHECKED_OUT|MAINTENANCE|RETIRED)$"
    )
    purchase_date: date
    price: Decimal = Field(..., max_digits=10, decimal_places=2)
    description: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class Asset(AssetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Category
    checkouts: List[Checkout] = []
    maintenance_logs: List[MaintenanceLog] = []

    class Config:
        from_attributes = True


# Summary Statistics
class StatsSummary(BaseModel):
    total_assets: int
    available_assets: int
    checked_out_assets: int
    maintenance_assets: int
    retired_assets: int
    total_value: Decimal
    active_checkouts_count: int
    active_maintenance_count: int
