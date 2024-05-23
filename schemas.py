from typing import Optional
from pydantic import BaseModel, EmailStr, constr, ValidationError, Field
from datetime import datetime
from typing_extensions import Annotated
import re

# class PhoneStr(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not (v.startswith('+') or v.startswith('1') or v.isdigit()):
#             raise ValueError("Phone number must start with '+' or '1' or be all digits")
#         if not (9 <= len(v) <= 15):
#             raise ValueError("Phone number length must be between 9 and 15 digits")
#         return v

#     @classmethod
#     def __get_pydantic_json_schema__(cls, core_schema, handler):
#         json_schema = handler(core_schema)
#         json_schema.update(
#             type="string",
#             pattern=r"^\+?[1-9]\d{8,14}$",
#             examples=["+123456789", "123456789", "19876543210"]
#         )
#         return json_schema


# # Define a custom validator for phone numbers
# def validate_phone_number(cls, v):
#     if not v.startswith('+'):
#         raise ValueError('Phone number must start with +')
#     if not 9 <= len(v) <= 15:
#         raise ValueError('Phone number length must be between 9 and 15')
#     if not v[1:].isdigit():
#         raise ValueError('Phone number must contain only digits after +')
#     return v

# # Create a type alias for the constrained string
# class PhoneStr(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield validate_phone_number

# User schemas
class UserBase(BaseModel):
    IDORole: int
    Email: str
    FullName: str
    Role: str
    Phone: str

class UserCreate(UserBase):
    pass

class UserSetPassword(BaseModel):
    Password: str

class UserUpdate(BaseModel):
    IDORole: Optional[str] = None
    Password: Optional[str] = None
    Email: Optional[str] = None
    FullName: Optional[str] = None
    Role: Optional[str] = None
    Phone: Optional[str] = None

class User(UserBase):
    UserID: int

    class Config:
        from_attributes = True

class UserRegistration(BaseModel):
    Email: str
    Password: str

class UserLogin(BaseModel):
    Email: str
    Password: str

class UserVerification(BaseModel):
    Code: int

# ProcessedLeaves schemas
class ProcessedLeavesBase(BaseModel):
    ProductID: int
    Description: str
    DryingID: Optional[str]
    FlouringID: Optional[str]
    DriedDate: Optional[datetime]
    FlouredDate: Optional[datetime]

class ProcessedLeavesCreate(ProcessedLeavesBase):
    Description: str
    DryingID: Optional[str]
    FlouringID: Optional[str]

class ProcessedLeavesUpdate(BaseModel):
    Description: Optional[str] = None
    FlouringID: Optional[str] = None
    DryingID: Optional[str] = None

class ProcessedLeaves(ProcessedLeavesBase):
    ProductID: int

    class Config:
        from_attributes = True

# WetLeavesCollection schemas
class WetLeavesCollectionBase(BaseModel):
    UserID: int
    CentralID: int
    Date: str
    Time: str
    Weight: int
    Expired: bool
    ExpirationTime: str

class WetLeavesCollectionCreate(WetLeavesCollectionBase):
    pass

class WetLeavesCollectionUpdate(BaseModel):
    UserID: Optional[int] = None
    CentralID: Optional[int] = None
    Date: Optional[str] = None
    Time: Optional[str] = None
    Weight: Optional[int] = None
    Expired: Optional[bool] = None
    ExpirationTime: Optional[str] = None

class WetLeavesCollection(WetLeavesCollectionBase):
    WetLeavesBatchID: str

    class Config:
        from_attributes = True

# Centra Details
class CentraDetails(BaseModel):
    PIC_name: str
    location: str
    email: str
    phone: int
    drying_machine_status: str = None
    flouring_machine_status: str = None
    action: str = None

# DryingMachine schemas
class DryingMachineBase(BaseModel):
    Capacity: str

class DryingMachineCreate(DryingMachineBase):
    pass

class DryingMachineUpdate(BaseModel):
    Capacity: Optional[str] = None

class DryingMachine(DryingMachineBase):
    MachineID: str

    class Config:
        from_attributes = True

# DryingActivity schemas
class DryingActivityBase(BaseModel):
    UserID: int
    CentralID: int
    Date: str
    Weight: int
    DryingMachineID: str
    Time: str

class DryingActivityCreate(DryingActivityBase):
    pass

class DryingActivityUpdate(BaseModel):
    UserID: Optional[int] = None
    CentralID: Optional[int] = None
    Date: Optional[str] = None
    Weight: Optional[int] = None
    DryingMachineID: Optional[str] = None
    Time: Optional[str] = None

class DryingActivity(DryingActivityBase):
    DryingID: str

    class Config:
        from_attributes = True

# FlouringMachine schemas
class FlouringMachineBase(BaseModel):
    Capacity: str

class FlouringMachineCreate(FlouringMachineBase):
    pass

class FlouringMachineUpdate(BaseModel):
    Capacity: Optional[str] = None

class FlouringMachine(FlouringMachineBase):
    MachineID: str

    class Config:
        from_attributes = True

# FlouringActivity schemas
class FlouringActivityBase(BaseModel):
    UserID: int
    CentralID: int
    Date: str
    Weight: int
    FlouringMachineID: str
    DryingID: str

class FlouringActivityCreate(FlouringActivityBase):
    pass

class FlouringActivityUpdate(BaseModel):
    UserID: Optional[int] = None
    CentralID: Optional[int] = None
    Date: Optional[str] = None
    Weight: Optional[int] = None
    FlouringMachineID: Optional[str] = None
    DryingID: Optional[str] = None

class FlouringActivity(FlouringActivityBase):
    FlouringID: str

    class Config:
        from_attributes = True

#stocks
class StockBase(BaseModel):
    product_id: int
    weight: int

class StockCreate(StockBase):
    pass

class StockUpdate(StockBase):
    pass

class Stock(StockBase):
    id: int
    location_id: Optional[int] = None

    class Config:
        from_attributes = True

# Centra schemas
class CentraBase(BaseModel):
    Address: str

class CentraCreate(CentraBase):
    pass

class CentraUpdate(BaseModel):
    Address: Optional[str] = None

class Centra(CentraBase):
    CentralID: int

    class Config:
        from_attributes = True

# Expedition schemas
class ExpeditionBase(BaseModel):
    EstimatedArrival: str
    TotalPackages: int
    ExpeditionDate: str
    ExpeditionServiceDetails: str
    Destination: str
    CentralID: int

class ExpeditionCreate(ExpeditionBase):
    pass

class ExpeditionUpdate(BaseModel):
    EstimatedArrival: Optional[str] = None
    TotalPackages: Optional[int] = None
    ExpeditionDate: Optional[str] = None
    ExpeditionServiceDetails: Optional[str] = None
    Destination: Optional[str] = None
    CentralID: Optional[int] = None

class Expedition(ExpeditionBase):
    ExpeditionID: int

    class Config:
        from_attributes = True

# ReceivedPackage schemas
class ReceivedPackageBase(BaseModel):
    ExpeditionID: int
    UserID: int
    PackageType: str
    ReceivedDate: str
    WarehouseDestination: str

class ReceivedPackageCreate(ReceivedPackageBase):
    pass

class ReceivedPackageUpdate(BaseModel):
    ExpeditionID: Optional[int] = None
    UserID: Optional[int] = None
    PackageType: Optional[str] = None
    ReceivedDate: Optional[str] = None
    WarehouseDestination: Optional[str] = None

class ReceivedPackage(ReceivedPackageBase):
    PackageID: int

    class Config:
        from_attributes = True

# PackageReceipt schemas
class PackageReceiptBase(BaseModel):
    UserID: int
    PackageID: int
    TotalWeight: int
    TimeAccepted: str
    Note: str
    Date: str

class PackageReceiptCreate(PackageReceiptBase):
    pass

class PackageReceiptUpdate(BaseModel):
    UserID: Optional[int] = None
    PackageID: Optional[int] = None
    TotalWeight: Optional[int] = None
    TimeAccepted: Optional[str] = None
    Note: Optional[str] = None
    Date: Optional[str] = None

class PackageReceipt(PackageReceiptBase):
    ReceiptID: int

    class Config:
        from_attributes = True

# Shipment
class ShipmentPickupSchedule(BaseModel):
    shipment_id: int
    pickup_time: datetime
    location: str

class ShipmentBase(BaseModel):
    batch_id: str
    description: Optional[str] = None
    status: Optional[str] = None
    weight: Optional[float] = None
    issue_description: Optional[str] = None

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(BaseModel):
    batch_id: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    weight: Optional[float] = None
    issue_description: Optional[str] = None

class Shipment(ShipmentBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShipmentIssue(BaseModel):
    description: str

class ShipmentRescale(BaseModel):
    new_weight: float

class ShipmentConfirmation(BaseModel):
    weight: float

# ProductReceipt schemas
class ProductReceiptBase(BaseModel):
    ProductID: str
    ReceiptID: int
    RescaledWeight: int

class ProductReceiptCreate(ProductReceiptBase):
    pass

class ProductReceiptUpdate(BaseModel):
    ProductID: Optional[str] = None
    ReceiptID: Optional[int] = None
    RescaledWeight: Optional[int] = None

class ProductReceipt(ProductReceiptBase):
    ProductReceiptID: int

    class Config:
        from_attributes = True

# PackageType schemas
class PackageTypeBase(BaseModel):
    Description: str

class PackageTypeCreate(PackageTypeBase):
    pass

class PackageTypeUpdate(BaseModel):
    Description: Optional[str] = None

class PackageType(PackageTypeBase):
    PackageTypeID: int

    class Config:
        from_attributes = True

class HarborGuardBase(BaseModel):
    PIC_name: str
    email: EmailStr
    phone: Optional[str] = None

class HarborGuardCreate(HarborGuardBase):
    """
    All fields are required when creating a new harbor guard.
    """
    pass

class HarborGuardUpdate(HarborGuardBase):
    """
    All fields are optional for update operations.
    """
    PIC_name: str = None
    email: EmailStr = None
    phone: Optional[str] = None

class HarborGuard(HarborGuardBase):
    """
    This class can be used to represent the harbor guard with additional fields if necessary,
    such as an internal ID or other attributes that are generated by the database.
    """
    id: int  # Assuming an 'id' field is automatically generated by the database

    class Config:
        from_attributes = True  # This setting is crucial for compatibility with ORMs like SQLAlchemy

# WAREHOUSE LOCATION
class WarehouseBase(BaseModel):
    PIC_name: str
    email: EmailStr
    phone: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(BaseModel):
    PIC_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class Warehouse(WarehouseBase):
    id: int  # Assuming an 'id' field is automatically generated by the database

    class Config:
        from_attributes = True  # This setting is crucial for compatibility with ORMs like SQLAlchemy

# User (Admin)
class UserBase(BaseModel):
    PIC_name: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    PIC_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class User(UserBase):
    id: int  # Assuming an 'id' field is automatically generated by the database

    class Config:
        from_attributes = True  # This setting is crucial for compatibility with ORMs like SQLAlchemy