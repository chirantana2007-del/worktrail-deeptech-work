from sqlmodel import SQLModel, create_engine
from models import Contractor, Worker, Site, AttendanceLog

engine = create_engine("sqlite:///worktrail.db")

def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()