from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel

from . import crud, models, schemas
from .database import get_db

app = FastAPI(
    title="Asset Management System API",
    description="High-performance backend service for tracking assets, checkouts, and maintenance.",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Helper schemas
class ReturnAssetRequest(BaseModel):
    notes: Optional[str] = None


class EndMaintenanceRequest(BaseModel):
    cost: Optional[Decimal] = None


# Stats endpoint
@app.get("/api/stats", response_model=schemas.StatsSummary)
def read_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)


# Categories Router
@app.get("/api/categories", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip=skip, limit=limit)


@app.post(
    "/api/categories",
    response_model=schemas.Category,
    status_code=status.HTTP_201_CREATED,
)
def create_new_category(
    category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(
            status_code=400, detail="Category with this name already exists"
        )
    return crud.create_category(db, category=category)


# Assets Router
@app.get("/api/assets", response_model=List[schemas.Asset])
def read_assets(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_assets(
        db,
        skip=skip,
        limit=limit,
        search=search,
        category_id=category_id,
        status=status,
    )


@app.post(
    "/api/assets", response_model=schemas.Asset, status_code=status.HTTP_201_CREATED
)
def create_new_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = crud.get_asset_by_serial(db, serial_number=asset.serial_number)
    if db_asset:
        raise HTTPException(
            status_code=400, detail="Asset with this serial number already exists"
        )
    # Verify category exists
    db_category = crud.get_category(db, category_id=asset.category_id)
    if not db_category:
        raise HTTPException(
            status_code=400, detail=f"Category ID {asset.category_id} not found"
        )
    return crud.create_asset(db, asset=asset)


@app.get("/api/assets/{asset_id}", response_model=schemas.Asset)
def read_asset_detail(asset_id: int, db: Session = Depends(get_db)):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset


@app.put("/api/assets/{asset_id}", response_model=schemas.Asset)
def update_existing_asset(
    asset_id: int, asset_update: schemas.AssetCreate, db: Session = Depends(get_db)
):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Check if serial number conflicts
    db_serial = crud.get_asset_by_serial(db, serial_number=asset_update.serial_number)
    if db_serial and db_serial.id != asset_id:
        raise HTTPException(
            status_code=400, detail="Serial number belongs to another asset"
        )

    return crud.update_asset(db, asset_id=asset_id, asset_update=asset_update)


# Actions
@app.post("/api/assets/{asset_id}/checkout", response_model=schemas.Checkout)
def checkout_asset_api(
    asset_id: int, checkout_data: schemas.CheckoutCreate, db: Session = Depends(get_db)
):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if db_asset.status != "AVAILABLE":
        raise HTTPException(
            status_code=400,
            detail=f"Asset is not available for checkout. Current status: {db_asset.status}",
        )

    return crud.checkout_asset(db, asset_id=asset_id, checkout_data=checkout_data)


@app.post("/api/assets/{asset_id}/return", response_model=schemas.Asset)
def return_asset_api(
    asset_id: int, request: ReturnAssetRequest, db: Session = Depends(get_db)
):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if db_asset.status != "CHECKED_OUT":
        raise HTTPException(
            status_code=400,
            detail=f"Asset is not currently checked out. Current status: {db_asset.status}",
        )

    return crud.return_asset(db, asset_id=asset_id, notes=request.notes)


@app.post(
    "/api/assets/{asset_id}/maintenance/start", response_model=schemas.MaintenanceLog
)
def start_maintenance_api(
    asset_id: int, log_data: schemas.MaintenanceLogCreate, db: Session = Depends(get_db)
):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if db_asset.status in ["MAINTENANCE", "RETIRED"]:
        raise HTTPException(
            status_code=400,
            detail=f"Asset cannot be placed in maintenance. Current status: {db_asset.status}",
        )

    return crud.start_maintenance(db, asset_id=asset_id, log_data=log_data)


@app.post("/api/assets/{asset_id}/maintenance/end", response_model=schemas.Asset)
def end_maintenance_api(
    asset_id: int, request: EndMaintenanceRequest, db: Session = Depends(get_db)
):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if db_asset.status != "MAINTENANCE":
        raise HTTPException(
            status_code=400,
            detail=f"Asset is not in maintenance. Current status: {db_asset.status}",
        )

    return crud.end_maintenance(db, asset_id=asset_id, cost=request.cost)
