from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Contractor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str
    company_name: str

class Worker(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str
    registered_date: date

class Site(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    site_name: str
    location: str
    contractor_id: int = Field(foreign_key="contractor.id")

class AttendanceLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    worker_id: int = Field(foreign_key="worker.id")
    site_id: int = Field(foreign_key="site.id")
    date: date
    status: str