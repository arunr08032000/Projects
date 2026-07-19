from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship
from .database import Base
import datetime


class Category(Base):
    __tablename__ = "assets_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    assets = relationship("Asset", back_populates="category")


class Asset(Base):
    __tablename__ = "assets_asset"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey("assets_category.id"), nullable=False)
    status = Column(String(20), default="AVAILABLE")
    purchase_date = Column(Date, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    category = relationship("Category", back_populates="assets")
    checkouts = relationship("Checkout", back_populates="asset")
    maintenance_logs = relationship("MaintenanceLog", back_populates="asset")


class Checkout(Base):
    __tablename__ = "assets_checkout"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets_asset.id"), nullable=False)
    employee_name = Column(String(150), nullable=False)
    employee_email = Column(String(254), nullable=False)
    checkout_date = Column(Date, default=datetime.date.today)
    expected_return_date = Column(Date, nullable=False)
    actual_return_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    asset = relationship("Asset", back_populates="checkouts")


class MaintenanceLog(Base):
    __tablename__ = "assets_maintenancelog"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets_asset.id"), nullable=False)
    description = Column(Text, nullable=False)
    cost = Column(Numeric(10, 2), default=0.00)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    asset = relationship("Asset", back_populates="maintenance_logs")
