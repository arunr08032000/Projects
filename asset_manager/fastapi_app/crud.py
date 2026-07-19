from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
import datetime
from decimal import Decimal


# Categories
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Assets
def get_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()


def get_asset_by_serial(db: Session, serial_number: str):
    return (
        db.query(models.Asset)
        .filter(models.Asset.serial_number == serial_number)
        .first()
    )


def get_assets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    category_id: int = None,
    status: str = None,
):
    query = db.query(models.Asset)
    if search:
        query = query.filter(
            models.Asset.name.ilike(f"%{search}%")
            | models.Asset.serial_number.ilike(f"%{search}%")
        )
    if category_id:
        query = query.filter(models.Asset.category_id == category_id)
    if status:
        query = query.filter(models.Asset.status == status)
    return query.offset(skip).limit(limit).all()


def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(
        name=asset.name,
        serial_number=asset.serial_number,
        category_id=asset.category_id,
        status=asset.status,
        purchase_date=asset.purchase_date,
        price=asset.price,
        description=asset.description,
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def update_asset(db: Session, asset_id: int, asset_update: schemas.AssetCreate):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        return None
    for key, value in asset_update.model_dump().items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset


# Checkout / Returns
def checkout_asset(db: Session, asset_id: int, checkout_data: schemas.CheckoutCreate):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset or db_asset.status != "AVAILABLE":
        return None

    # Update asset status
    db_asset.status = "CHECKED_OUT"

    # Create checkout record
    db_checkout = models.Checkout(
        asset_id=asset_id,
        employee_name=checkout_data.employee_name,
        employee_email=checkout_data.employee_email,
        expected_return_date=checkout_data.expected_return_date,
        notes=checkout_data.notes,
    )
    db.add(db_checkout)
    db.commit()
    db.refresh(db_checkout)
    return db_checkout


def return_asset(db: Session, asset_id: int, notes: str = None):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset or db_asset.status != "CHECKED_OUT":
        return None

    # Find the active checkout (where actual_return_date is null)
    db_checkout = (
        db.query(models.Checkout)
        .filter(
            models.Checkout.asset_id == asset_id,
            models.Checkout.actual_return_date == None,
        )
        .order_by(models.Checkout.checkout_date.desc())
        .first()
    )

    # Update asset status
    db_asset.status = "AVAILABLE"

    if db_checkout:
        db_checkout.actual_return_date = datetime.date.today()
        if notes:
            db_checkout.notes = (
                f"{db_checkout.notes or ''} | Return Notes: {notes}".strip(" | ")
            )

    db.commit()
    if db_checkout:
        db.refresh(db_checkout)
    return db_asset


# Maintenance Log
def start_maintenance(
    db: Session, asset_id: int, log_data: schemas.MaintenanceLogCreate
):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset or db_asset.status in ["MAINTENANCE", "RETIRED"]:
        return None

    db_asset.status = "MAINTENANCE"
    db_log = models.MaintenanceLog(
        asset_id=asset_id,
        description=log_data.description,
        cost=log_data.cost,
        start_date=log_data.start_date,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def end_maintenance(
    db: Session, asset_id: int, cost: Decimal = None, end_date: datetime.date = None
):
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset or db_asset.status != "MAINTENANCE":
        return None

    db_asset.status = "AVAILABLE"
    db_log = (
        db.query(models.MaintenanceLog)
        .filter(
            models.MaintenanceLog.asset_id == asset_id,
            models.MaintenanceLog.end_date == None,
        )
        .order_by(models.MaintenanceLog.start_date.desc())
        .first()
    )

    if db_log:
        db_log.end_date = end_date or datetime.date.today()
        if cost is not None:
            db_log.cost = cost

    db.commit()
    return db_asset


# Stats
def get_stats(db: Session):
    total = db.query(models.Asset).count()
    available = (
        db.query(models.Asset).filter(models.Asset.status == "AVAILABLE").count()
    )
    checked_out = (
        db.query(models.Asset).filter(models.Asset.status == "CHECKED_OUT").count()
    )
    maintenance = (
        db.query(models.Asset).filter(models.Asset.status == "MAINTENANCE").count()
    )
    retired = db.query(models.Asset).filter(models.Asset.status == "RETIRED").count()

    total_val_query = db.query(func.sum(models.Asset.price)).first()
    total_val = (
        total_val_query[0] if total_val_query[0] is not None else Decimal("0.00")
    )

    active_checkouts = (
        db.query(models.Checkout)
        .filter(models.Checkout.actual_return_date == None)
        .count()
    )
    active_maintenance = (
        db.query(models.MaintenanceLog)
        .filter(models.MaintenanceLog.end_date == None)
        .count()
    )

    return {
        "total_assets": total,
        "available_assets": available,
        "checked_out_assets": checked_out,
        "maintenance_assets": maintenance,
        "retired_assets": retired,
        "total_value": Decimal(total_val),
        "active_checkouts_count": active_checkouts,
        "active_maintenance_count": active_maintenance,
    }
