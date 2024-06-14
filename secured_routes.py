from fastapi import APIRouter, Request, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import schemas, crud, models
from middleware import get_current_user

secured_router = APIRouter()

# test protected route
@secured_router.get("/protected-route")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "You are authenticated", "user": user["sub"]}

# Batches
@secured_router.post("/batches/", response_model=schemas.ProcessedLeaves)
def create_new_batch(batch: schemas.ProcessedLeavesCreate, db: Session = Depends(get_db)):
    return crud.create_batch(db=db, batch=batch)

@secured_router.get("/batches/", response_model=List[schemas.ProcessedLeaves])
def read_batches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    batches = crud.get_all_batches(db=db, skip=skip, limit=limit)
    return batches

@secured_router.get("/batches/{batch_id}", response_model=schemas.ProcessedLeaves)
def read_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = crud.get_batch_by_id(db=db, batch_id=batch_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@secured_router.put("/batches/{batch_id}", response_model=schemas.ProcessedLeaves)
def update_existing_batch(batch_id: int, update_data: schemas.ProcessedLeavesUpdate, db: Session = Depends(get_db)):
    batch = crud.update_batch(db=db, batch_id=batch_id, update_data=update_data)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@secured_router.delete("/batches/{batch_id}", response_model=schemas.ProcessedLeaves)
def delete_existing_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = crud.delete_batch(db=db, batch_id=batch_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

#DRYING
@secured_router.post("/drying-machine/create/")
def add_drying_machine(drying_machine: schemas.DryingMachineCreate, db: Session = Depends(get_db)):
    new_machine = crud.create_drying_machine(db, drying_machine)
    if new_machine:
        return {"message": "Drying machine created successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Drying machine with the same ID already exists!")

@secured_router.post("/drying_machines/{machine_id}/start", response_model=schemas.DryingMachine)
def start_machine(machine_id: str, db: Session = Depends(get_db)):
    success = crud.start_drying_machine(db, machine_id)
    if not success:
        raise HTTPException(status_code=400, detail="Machine could not be started")
    machine = db.query(models.DryingMachine).filter(models.DryingMachine.MachineID == machine_id).first()
    return machine

@secured_router.post("/drying_machines/{machine_id}/stop", response_model=schemas.DryingMachine)
def stop_machine(machine_id: str, db: Session = Depends(get_db)):
    success = crud.stop_drying_machine(db, machine_id)
    if not success:
        raise HTTPException(status_code=400, detail="Machine could not be stopped")
    machine = db.query(models.DryingMachine).filter(models.DryingMachine.MachineID == machine_id).first()
    return machine

@secured_router.get("/drying_machines/{machine_id}/status", response_model=str)
def read_machine_status(machine_id: int, db: Session = Depends(get_db)):
    status = crud.get_drying_machine_status(db, machine_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return status


 #drying activity  
@secured_router.post("/drying_activity/create")
def create_drying_activity(drying_activity: schemas.DryingActivityCreate, db: Session = Depends(get_db)):
    dry_activity = crud.add_new_drying_activity(db, drying_activity)
    if dry_activity:
        return {"message": "Drying activity created successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Drying machine with the same ID already exists!")

@secured_router.get("/drying-activities/{drying_id}")
def show_drying_activity(drying_id: int, db: Session = Depends(get_db)):
    drying = crud.get_drying_activity(db, drying_id)
    return drying

@secured_router.put("/drying-activities/{drying_id}")
def update_drying_activity(drying_id: int, drying_activity: schemas.DryingActivityUpdate, db: Session = Depends(get_db)):
    db_drying_activity = crud.update_drying_activity(db, drying_id, drying_activity)
    if db_drying_activity is None:
        raise HTTPException(status_code=404, detail="Drying activity not found")
    return db_drying_activity

@secured_router.delete("/drying-activities/{drying_id}")
def delete_drying_activity(drying_id: int, db: Session = Depends(get_db)):
    db_drying_activity = crud.delete_drying_activity(db, drying_id)
    if db_drying_activity is None:
        raise HTTPException(status_code=404, detail="Drying activity not found")
    return db_drying_activity

#FLOURING
@secured_router.post("/flouring-machine/create/")
def add_flouring_machine(flouring_machine: schemas.FlouringMachineCreate, db: Session = Depends(get_db)):
    new_machine = crud.add_new_flouring_machine(db, flouring_machine)
    if new_machine:
        return {"message": "Flouring machine created successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Flouring machine with the same ID already exists!")

@secured_router.get("/flouring_machines/{machine_id}/status", response_model=str)
def read_flouring_machine_status(machine_id: str, db: Session = Depends(get_db)):
    status = crud.get_flouring_machine_status(db, machine_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return status

@secured_router.post("/flouring_machines/{machine_id}/start")
def start_flouring_machine(machine_id: str, db: Session = Depends(get_db)):
    success = crud.start_flouring_machine(db, machine_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to start the machine or machine already running")
    return {"message": "Machine started successfully"}

@secured_router.post("/flouring_machines/{machine_id}/stop")
def stop_flouring_machine(machine_id: str, db: Session = Depends(get_db)):
    success = crud.stop_flouring_machine(db, machine_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to stop the machine or machine already idle")
    return {"message": "Machine stopped successfully"}


#flouring activity
@secured_router.post("/flouring_activity/create")
def create_flouring_activity(flouring_activity: schemas.FlouringActivityCreate, db: Session = Depends(get_db)):
    flour_activity = crud.add_new_flouring_activity(db, flouring_activity)
    if flour_activity:
        return {"message": "Flouring activity created successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Flouring machine with the same ID already exists!")

    
@secured_router.get("/flouring_activities", response_model=List[schemas.FlouringActivity])
def read_flouring_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flouring_activities = crud.get_all_flouring_activity(db=db, skip=skip, limit=limit)
    return flouring_activities

@secured_router.get("/flouring_activity/{flouring_id}", response_model=schemas.FlouringActivity)
def get_flouring_activity(flouring_id: int, db: Session = Depends(get_db)):
    flouring_activity = crud.get_flouring_activity(db=db, flouring_id=flouring_id)
    if not flouring_activity:
        raise HTTPException(status_code=404, detail="Flouring activity not found")
    return flouring_activity

@secured_router.put("/flouring_activity/update/{flouring_id}", response_model=schemas.FlouringActivity)
def update_flouring_activity(flouring_id: int, flouring_activity: schemas.FlouringActivityUpdate, db: Session = Depends(get_db)):
    updated_flouring = crud.update_flouring_activity(db, flouring_id, flouring_activity)
    if not updated_flouring:
        raise HTTPException(status_code=404, detail="Flouring activity not found")
    return updated_flouring

@secured_router.delete("/flouring_activity/delete/{flouring_id}", response_model=schemas.FlouringActivity)
def delete_flouring_activity(flouring_id: int, db: Session = Depends(get_db)):
    deleted_flouring_activity = crud.delete_flouring_activity(db=db, flouring_id=flouring_id)
    if not deleted_flouring_activity:
        raise HTTPException(status_code=404, detail="Flouring activity not found")
    return deleted_flouring_activity



#WET LEAVES COLLECTIONS
@secured_router.post("/wet-leaves-collections/create")
def create_wet_leaves_collection(wet_leaves_collection: schemas.WetLeavesCollectionCreate, db: Session = Depends(get_db)):
    return crud.add_new_wet_leaves_collection(db, wet_leaves_collection)

@secured_router.get("/wet-leaves-collections/", response_model=list[schemas.WetLeavesCollection])
def read_wet_leaves_collections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_wet_leaves_collections(db=db, skip=skip, limit=limit)

@secured_router.get("/wet-leaves-collections/{wet_leaves_batch_id}", response_model=schemas.WetLeavesCollection)
def read_wet_leaves_collection(wet_leaves_batch_id: str, db: Session = Depends(get_db)):
    db_wet_leaves_collection = crud.get_wet_leaves_collection(db=db, wet_leaves_batch_id=wet_leaves_batch_id)
    if db_wet_leaves_collection is None:
        raise HTTPException(status_code=404, detail="WetLeavesCollection not found")
    return db_wet_leaves_collection

@secured_router.put("/wet-leaves-collections/{wet_leaves_batch_id}", response_model=schemas.WetLeavesCollection)
def update_wet_leaves_collection(wet_leaves_batch_id: str, update_data: schemas.WetLeavesCollectionUpdate, db: Session = Depends(get_db)):
    db_wet_leaves_collection = crud.update_wet_leaves_collection(db=db, wet_leaves_batch_id=wet_leaves_batch_id, update_data=update_data)
    if db_wet_leaves_collection is None:
        raise HTTPException(status_code=404, detail="WetLeavesCollection not found")
    return db_wet_leaves_collection

@secured_router.delete("/wet-leaves-collections/{wet_leaves_batch_id}", response_model=schemas.WetLeavesCollection)
def delete_wet_leaves_collection(wet_leaves_batch_id: str, db: Session = Depends(get_db)):
    db_wet_leaves_collection = crud.delete_wet_leaves_collection(db=db, wet_leaves_batch_id=wet_leaves_batch_id)
    if db_wet_leaves_collection is None:
        raise HTTPException(status_code=404, detail="WetLeavesCollection not found")
    return db_wet_leaves_collection

# Shipments (Centra)
@secured_router.post("/shipments")
async def add_shipment(shipment_data: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    added_shipment = crud.add_shipment(db, shipment_data)
    return added_shipment

@secured_router.put("/shipments/{shipment_id}")
async def update_shipment(shipment_id: int, shipment_update: schemas.ShipmentUpdate, db: Session = Depends(get_db)):
    updated_shipment = crud.update_shipment(db, shipment_id, shipment_update)
    if updated_shipment:
        return updated_shipment
    raise HTTPException(status_code=404, detail="Shipment not found")

@secured_router.get("/notifications")
async def show_notifications(db: Session = Depends(get_db)):
    notifications = crud.get_notifications(db)
    return {"notifications": notifications}

@secured_router.get("/shipments", response_model=List[schemas.Shipment])
def read_shipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shipments = crud.get_all_shipments(db=db, skip=skip, limit=limit)
    return shipments

@secured_router.get("/shipments/{shipment_id}")
async def get_shipment_details(shipment_id: str, db: Session = Depends(get_db)):
    shipment = crud.get_shipment_details(db, shipment_id)
    if shipment:
        return shipment
    raise HTTPException(status_code=404, detail="Shipment not found")

@secured_router.delete("/shipments/{shipment_id}")
async def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    if crud.delete_shipment(db, shipment_id):
        return {"message": "Shipment deleted"}
    raise HTTPException(status_code=404, detail="Shipment not found")

@secured_router.post("/shipments/{shipment_id}/confirm")
async def confirm_shipment(shipment_id: int, confirmation: schemas.ShipmentConfirmation, db: Session = Depends(get_db)):
    if crud.confirm_shipment(db, shipment_id, confirmation.weight):
        return {"message": "Shipment confirmed"}
    raise HTTPException(status_code=404, detail="Shipment not found")

@secured_router.post("/shipments/{shipment_id}/report")
async def report_shipment_issue(shipment_id: int, issue: schemas.ShipmentIssue, db: Session = Depends(get_db)):
    if crud.report_shipment_issue(db, shipment_id, issue.description):
        return {"message": "Issue reported successfully"}
    raise HTTPException(status_code=404, detail="Shipment not found")

@secured_router.post("/shipments/{shipment_id}/confirm")
async def confirm_shipment_arrival(shipment_id: int, confirmation: schemas.ShipmentConfirmation, db: Session = Depends(get_db)):
    if crud.confirm_shipment(db, shipment_id, confirmation.weight):
        return {"message": "Shipment confirmed"}
    raise HTTPException(status_code=404, detail="Shipment not found")

@secured_router.put("/shipments/{shipment_id}/rescale")
async def rescale_shipment(shipment_id: int, rescale: schemas.ShipmentRescale, db: Session = Depends(get_db)):
    if crud.rescale_shipment(db, shipment_id, rescale.new_weight):
        return {"message": "Shipment weight updated"}
    raise HTTPException(status_code=404, detail="Shipment not found")


# Stocks
@secured_router.get("/stocks")
async def show_all_stock_details(db: Session = Depends(get_db)):
    stocks = crud.get_all_stocks(db)
    return stocks

@secured_router.get("/stocks/{location_id}")
async def show_stock_detail(location_id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock_detail(db, location_id)
    if stock:
        return stock
    raise HTTPException(status_code=404, detail="Location not found")


# Locations
@secured_router.get("/location/{location_id}")
async def show_location_details(location_id: int, db: Session = Depends(get_db)):
    location = crud.get_location_details(db, location_id)
    if location:
        return location
    raise HTTPException(status_code=404, detail="Location not found")

# Shipment History
@secured_router.get("/shipments/{location_id}/history")
async def show_shipment_history(location_id: int, db: Session = Depends(get_db)):
    shipment_history = crud.get_shipment_history(db, location_id)
    if shipment_history:
        return shipment_history
    raise HTTPException(status_code=404, detail="Location not found")

@secured_router.post("/shipments/schedule-pickup")
async def schedule_pickup(pickup_data: schemas.ShipmentPickupSchedule, db: Session = Depends(get_db)):
    is_valid = crud.validate_shipment_id(db, pickup_data.shipment_id)
    if is_valid:
        result = crud.schedule_pickup(db, pickup_data)
        if result:
            return {"message": "Pickup scheduled successfully"}
        return {"error": "Failed to schedule pickup"}
    raise HTTPException(status_code=404, detail="Shipment not found")

# Centra
@secured_router.get("/centras")
async def show_all_centras(db: Session = Depends(get_db)):
    centras = crud.get_all_centras(db)
    return centras

@secured_router.get("/centras/{centra_id}", response_model=schemas.Centra)
def read_centra(CentralID: int, db: Session = Depends(get_db)):
    centra = crud.get_centra_by_id(db, CentralID)
    return centra

@secured_router.post("/centras", response_model=schemas.CentraDetails)
async def create_new_centra(centra_data: schemas.CentraCreate, db: Session = Depends(get_db)):
    new_centra = crud.add_new_centra(db, centra_data)
    return new_centra

@secured_router.put("/centras/{centra_id}", response_model=schemas.Centra)
def update_centra(CentralID: int, centra_update: schemas.CentraUpdate, db: Session = Depends(get_db)):
    return crud.update_centra(db, CentralID, centra_update)

@secured_router.delete("/centras/{centra_id}", response_model=dict)
def delete_centra(CentralID: int, db: Session = Depends(get_db)):
    return crud.delete_centra(db, CentralID)

# Shipment (XYZ)

# @secured_router.put("/shipments/{shipment_id}")
# async def update_shipment_details(shipment_id: str, shipment_update: ShipmentUpdate, db: Session = Depends(get_db)):
#     updated = update_shipment(db, shipment_id, shipment_update)
#     if updated:
#         return updated
#     raise HTTPException(status_code=404, detail="Shipment not found")


@secured_router.delete("/shipments/{shipment_id}")
async def remove_shipment(shipment_id: str, db: Session = Depends(get_db)):
    deleted = delete_shipment(db, shipment_id)
    if deleted:
        return {"message": "Shipment deleted successfully"}
    raise HTTPException(status_code=404, detail="Shipment not found")

# Harborguards
@secured_router.get("/harborguards")
async def show_all_harbor_guards(db: Session = Depends(get_db)):
    guards = crud.get_all_harbor_guards(db)
    return guards

@secured_router.get("/harborguards/{guard_id}")
async def show_harbor_guard(HarborID: int, db: Session = Depends(get_db)):
    guard = crud.get_harbor_guard(db, HarborID)
    return guard

@secured_router.post("/harborguards", response_model=schemas.HarborGuardCreate)
async def add_harbor_guard(guard_data: schemas.HarborGuardCreate, db: Session = Depends(get_db)):
    new_guard = crud.create_harbor_guard(db, guard_data)
    return new_guard

@secured_router.put("/harborguards/{guard_id}", response_model=schemas.HarborGuardUpdate)
async def modify_harbor_guard(HarborID: int, guard_data: schemas.HarborGuardUpdate, db: Session = Depends(get_db)):
    updated_guard = crud.update_harbor_guard(db, HarborID, guard_data)
    return updated_guard

@secured_router.delete("/harborguards/{guard_id}")
async def remove_harbor_guard(guard_id: int, db: Session = Depends(get_db)):
    result = crud.delete_harbor_guard(db, guard_id)
    return result

# Warehouses
@secured_router.get("/warehouses", response_model=List[schemas.Warehouse])
async def show_all_warehouses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    warehouses = crud.get_all_warehouses(db, skip=skip, limit=limit)
    return warehouses

@secured_router.get("/warehouses/{warehouse_id}", response_model=schemas.Warehouse)
async def get_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    warehouse = crud.get_warehouse(db, warehouse_id=warehouse_id)
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

@secured_router.post("/warehouses", response_model=schemas.Warehouse)
async def create_warehouse(warehouse_data: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return crud.create_warehouse(db=db, warehouse_data=warehouse_data)

@secured_router.put("/warehouses/{warehouse_id}", response_model=schemas.Warehouse)
async def update_warehouse(warehouse_id: str, warehouse_data: schemas.WarehouseUpdate, db: Session = Depends(get_db)):
    updated_warehouse = crud.update_warehouse(db, warehouse_id=warehouse_id, update_data=warehouse_data)
    if updated_warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return updated_warehouse

@secured_router.delete("/warehouses/{warehouse_id}")
async def delete_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    deleted_warehouse = crud.delete_warehouse(db, warehouse_id=warehouse_id)
    if deleted_warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return {"message": "Warehouse deleted successfully"}

# User (Admin)
# @secured_router.post("/admins/", response_model=schemas.Admin)
# def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
#     db_admin = crud.get_admin_by_email(db, email=admin.email)
#     if db_admin:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_admin(db=db, admin=admin)

# @secured_router.get("/admins/", response_model=List[schemas.Admin])
# def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     admins = crud.get_admins(db, skip=skip, limit=limit)
#     return admins

# @secured_router.get("/admins/{admin_id}", response_model=schemas.Admin)
# def read_admin(admin_id: int, db: Session = Depends(get_db)):
#     db_admin = crud.get_admin(db, admin_id=admin_id)
#     if db_admin is None:
#         raise HTTPException(status_code=404, detail="Admin not found")
#     return db_admin

# @secured_router.put("/admins/{admin_id}", response_model=schemas.Admin)
# def update_admin(admin_id: int, admin: schemas.AdminUpdate, db: Session = Depends(get_db)):
#     db_admin = crud.update_admin(db, admin_id=admin_id, admin=admin)
#     if db_admin is None:
#         raise HTTPException(status_code=404, detail="Admin not found")
#     return db_admin

# @secured_router.delete("/admins/{admin_id}", response_model=schemas.Admin)
# def delete_admin(admin_id: int, db: Session = Depends(get_db)):
#     db_admin = crud.delete_admin(db, admin_id=admin_id)
#     if db_admin is None:
#         raise HTTPException(status_code=404, detail="Admin not found")
#     return db_admin


#expedition
@secured_router.post("/expeditions/", response_model=schemas.Expedition)
def create_expedition(expedition: schemas.ExpeditionCreate, db: Session = Depends(get_db)):
    return crud.create_expedition(db, expedition)

@secured_router.get("/expeditions/", response_model=List[schemas.Expedition])
def read_expeditions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    expeditions = crud.get_expeditions(db=db, skip=skip, limit=limit)
    return expeditions

@secured_router.get("/expeditions/{expedition_id}", response_model=schemas.Expedition)
def read_expedition(expedition_id: int, db: Session = Depends(get_db)):
    expedition = crud.get_expedition(db=db, expedition_id=expedition_id)
    if expedition is None:
        raise HTTPException(status_code=404, detail="Expedition not found")
    return expedition

@secured_router.put("/expeditions/{expedition_id}", response_model=schemas.Expedition)
def update_expedition(expedition_id: int, expedition: schemas.ExpeditionUpdate, db: Session = Depends(get_db)):
    db_expedition = crud.update_expedition(db=db, expedition_id=expedition_id, expedition=expedition)
    if db_expedition is None:
        raise HTTPException(status_code=404, detail="Expedition not found")
    return db_expedition

@secured_router.delete("/expeditions/{expedition_id}", response_model=schemas.Expedition)
def delete_expedition(expedition_id: int, db: Session = Depends(get_db)):
    db_expedition = crud.delete_expedition(db, expedition_id)
    if db_expedition is None:
        raise HTTPException(status_code=404, detail="Expedition not found")
    return db_expedition

#received package
@secured_router.post("/received_packages/", response_model=schemas.ReceivedPackage)
def create_received_package(received_package: schemas.ReceivedPackageCreate, db: Session = Depends(get_db)):
    return crud.create_received_package(db=db, received_package=received_package)

@secured_router.get("/received_packages/", response_model=List[schemas.ReceivedPackage])
def read_received_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    received_packages = crud.get_received_packages(db=db, skip=skip, limit=limit)
    return received_packages

@secured_router.get("/received_packages/{package_id}", response_model=schemas.ReceivedPackage)
def read_received_package(package_id: int, db: Session = Depends(get_db)):
    received_package = crud.get_received_package(db=db, package_id=package_id)
    if received_package is None:
        raise HTTPException(status_code=404, detail="Received package not found")
    return received_package

@secured_router.put("/received_packages/{package_id}", response_model=schemas.ReceivedPackage)
def update_received_package(package_id: int, received_package: schemas.ReceivedPackageUpdate, db: Session = Depends(get_db)):
    db_received_package = crud.update_received_package(db=db, package_id=package_id, received_package=received_package)
    if db_received_package is None:
        raise HTTPException(status_code=404, detail="Received package not found")
    return db_received_package

@secured_router.delete("/received_packages/{package_id}", response_model=schemas.ReceivedPackage)
def delete_received_package(package_id: int, db: Session = Depends(get_db)):
    db_received_package = crud.delete_received_package(db=db, package_id=package_id)
    if db_received_package is None:
        raise HTTPException(status_code=404, detail="Received package not found")
    return db_received_package

#package receipt
@secured_router.post("/package_receipts/", response_model=schemas.PackageReceipt)
def create_package_receipt(package_receipt: schemas.PackageReceiptCreate, db: Session = Depends(get_db)):
    return crud.create_package_receipt(db, package_receipt)

@secured_router.get("/package_receipts/{receipt_id}", response_model=schemas.PackageReceipt)
def read_package_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_package_receipt = crud.get_package_receipt(db, receipt_id)
    if db_package_receipt is None:
        raise HTTPException(status_code=404, detail="Package receipt not found")
    return db_package_receipt

@secured_router.get("/package_receipts/", response_model=List[schemas.PackageReceipt])
def read_package_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    package_receipts = crud.get_package_receipts(db, skip=skip, limit=limit)
    return package_receipts

@secured_router.put("/package_receipts/{receipt_id}", response_model=schemas.PackageReceipt)
def update_package_receipt(receipt_id: int, package_receipt: schemas.PackageReceiptUpdate, db: Session = Depends(get_db)):
    db_package_receipt = crud.update_package_receipt(db, receipt_id, package_receipt)
    if db_package_receipt is None:
        raise HTTPException(status_code=404, detail="Package receipt not found")
    return db_package_receipt

@secured_router.delete("/package_receipts/{receipt_id}", response_model=schemas.PackageReceipt)
def delete_package_receipt(receipt_id: int, db: Session = Depends(get_db)):
    db_package_receipt = crud.delete_package_receipt(db, receipt_id)
    if db_package_receipt is None:
        raise HTTPException(status_code=404, detail="Package receipt not found")
    return db_package_receipt

#product receipt
@secured_router.post("/product_receipts/", response_model=schemas.ProductReceipt)
def create_product_receipt(product_receipt: schemas.ProductReceiptCreate, db: Session = Depends(get_db)):
    return crud.create_product_receipt(db, product_receipt)

@secured_router.get("/product_receipts/{product_receipt_id}", response_model=schemas.ProductReceipt)
def read_product_receipt(product_receipt_id: int, db: Session = Depends(get_db)):
    db_product_receipt = crud.get_product_receipt(db, product_receipt_id)
    if db_product_receipt is None:
        raise HTTPException(status_code=404, detail="Product receipt not found")
    return db_product_receipt

@secured_router.get("/product_receipts/", response_model=List[schemas.ProductReceipt])
def read_product_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product_receipts = crud.get_product_receipts(db, skip=skip, limit=limit)
    return product_receipts

@secured_router.put("/product_receipts/{product_receipt_id}", response_model=schemas.ProductReceipt)
def update_product_receipt(product_receipt_id: int, product_receipt: schemas.ProductReceiptUpdate, db: Session = Depends(get_db)):
    db_product_receipt = crud.update_product_receipt(db, product_receipt_id, product_receipt)
    if db_product_receipt is None:
        raise HTTPException(status_code=404, detail="Product receipt not found")
    return db_product_receipt

@secured_router.delete("/product_receipts/{product_receipt_id}", response_model=schemas.ProductReceipt)
def delete_product_receipt(product_receipt_id: int, db: Session = Depends(get_db)):
    db_product_receipt = crud.delete_product_receipt(db, product_receipt_id)
    if db_product_receipt is None:
        raise HTTPException(status_code=404, detail="Product receipt not found")
    return db_product_receipt