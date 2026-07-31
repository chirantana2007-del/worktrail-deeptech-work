from fastapi import FastAPI
from sqlmodel import Session, select
from db import engine
from models import Contractor, Worker, Site, AttendanceLog
from models import Contractor, Worker, Site, AttendanceLog  # already imported, just confirming

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for hackathon simplicity — allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Create a contractor ---
@app.post("/contractors")
def create_contractor(contractor: Contractor):
    with Session(engine) as session:
        session.add(contractor)
        session.commit()
        session.refresh(contractor)
        return contractor

# --- Get all contractors ---
@app.get("/contractors")
def get_contractors():
    with Session(engine) as session:
        return session.exec(select(Contractor)).all()

# --- Create a site ---
@app.post("/sites")
def create_site(site: Site):
    with Session(engine) as session:
        session.add(site)
        session.commit()
        session.refresh(site)
        return site

# --- Get all sites ---
@app.get("/sites")
def get_sites():
    with Session(engine) as session:
        return session.exec(select(Site)).all()

# --- Create a worker ---
from datetime import date as date_type

@app.post("/workers")
def create_worker(worker: Worker):
    if isinstance(worker.registered_date, str):
        worker.registered_date = date_type.fromisoformat(worker.registered_date)
    with Session(engine) as session:
        session.add(worker)
        session.commit()
        session.refresh(worker)
        return worker

# --- Get all workers ---
@app.get("/workers")
def get_workers():
    with Session(engine) as session:
        workers = session.exec(select(Worker)).all()
        return workers

# --- Log attendance ---
@app.post("/attendance")
def log_attendance(log: AttendanceLog):
    if isinstance(log.date, str):
        log.date = date_type.fromisoformat(log.date)
    with Session(engine) as session:
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

# --- Get attendance for a specific worker ---
@app.get("/attendance/{worker_id}")
def get_attendance(worker_id: int):
    with Session(engine) as session:
        logs = session.exec(
            select(AttendanceLog).where(AttendanceLog.worker_id == worker_id)
        ).all()
        return logs
import joblib
import pandas as pd
from datetime import date as date_type

model = joblib.load("reliability_model.pkl")
@app.get("/reliability/all")
def get_all_reliability():
    with Session(engine) as session:
        all_workers = session.exec(select(Worker)).all()
        results = []

        for worker in all_workers:
            logs = session.exec(
                select(AttendanceLog).where(AttendanceLog.worker_id == worker.id)
            ).all()

            if len(logs) == 0:
                continue  # skip workers with no attendance history yet

            total_days_logged = len(logs)
            present_count = sum(1 for log in logs if log.status == "present")
            attendance_rate = present_count / total_days_logged

            dates = [log.date for log in logs]
            tenure_days = (max(dates) - min(dates)).days

            num_sites = len(set(log.site_id for log in logs))

            features = pd.DataFrame([{
                "attendance_rate": attendance_rate,
                "tenure_days": tenure_days,
                "num_sites": num_sites,
                "total_days_logged": total_days_logged
            }])
            predicted_score = model.predict(features)[0]

            results.append({
                "worker_id": worker.id,
                "worker_name": worker.name,
                "phone": worker.phone,
                "reliability_score": round(float(predicted_score), 1),
                "attendance_rate": round(attendance_rate, 2),
                "tenure_days": tenure_days,
                "num_sites": num_sites,
                "total_days_logged": total_days_logged
            })

        # Sort by score, highest first - most useful default for a contractor browsing
        results.sort(key=lambda x: x["reliability_score"], reverse=True)
        return results
@app.get("/reliability/{phone}")
def get_reliability(phone: str):
    with Session(engine) as session:
        # Step 1: find the worker by phone number
        worker = session.exec(select(Worker).where(Worker.phone == phone)).first()
        if not worker:
            return {"error": "No worker found with this phone number."}

        # Step 2: get all their attendance logs
        logs = session.exec(
            select(AttendanceLog).where(AttendanceLog.worker_id == worker.id)
        ).all()

        if len(logs) == 0:
            return {"error": "No attendance history yet for this worker."}

        # Step 3: compute the same 4 features used in training
        total_days_logged = len(logs)
        present_count = sum(1 for log in logs if log.status == "present")
        attendance_rate = present_count / total_days_logged

        dates = [log.date for log in logs]
        tenure_days = (max(dates) - min(dates)).days

        num_sites = len(set(log.site_id for log in logs))

        # Step 4: predict using the loaded model
        features = pd.DataFrame([{
            "attendance_rate": attendance_rate,
            "tenure_days": tenure_days,
            "num_sites": num_sites,
            "total_days_logged": total_days_logged
        }])
        predicted_score = model.predict(features)[0]

        return {
            "worker_name": worker.name,
            "reliability_score": round(float(predicted_score), 1),
            "attendance_rate": round(attendance_rate, 2),
            "tenure_days": tenure_days,
            "num_sites": num_sites,
            "total_days_logged": total_days_logged
        }
