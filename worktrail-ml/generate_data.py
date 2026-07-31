import random
from datetime import date, timedelta
from faker import Faker
import pandas as pd

fake = Faker('en_IN')  # Indian names/locale
random.seed(42)  # makes results reproducible - same fake data every run

NUM_WORKERS = 200
SITES = [f"Site_{i}" for i in range(1, 11)]  # 10 fake site names for now

ARCHETYPES = {
    "reliable":   {"weight": 0.25, "attendance_prob": (0.90, 0.98), "tenure_days": (120, 180), "num_sites": (2, 4)},
    "moderate":   {"weight": 0.40, "attendance_prob": (0.70, 0.85), "tenure_days": (60, 120),  "num_sites": (1, 2)},
    "unreliable": {"weight": 0.25, "attendance_prob": (0.40, 0.65), "tenure_days": (14, 45),   "num_sites": (1, 1)},
    "new":        {"weight": 0.10, "attendance_prob": (0.60, 1.00), "tenure_days": (3, 14),    "num_sites": (1, 1)},
}

def pick_archetype():
    names = list(ARCHETYPES.keys())
    weights = [ARCHETYPES[n]["weight"] for n in names]
    return random.choices(names, weights=weights, k=1)[0]

records = []
today = date.today()

for worker_id in range(1, NUM_WORKERS + 1):
    archetype = pick_archetype()
    config = ARCHETYPES[archetype]
    worker_name = fake.name()

    attendance_prob = random.uniform(*config["attendance_prob"])
    tenure_days = random.randint(*config["tenure_days"])
    num_sites = random.randint(*config["num_sites"])
    worker_sites = random.sample(SITES, num_sites)

    start_date = today - timedelta(days=tenure_days)

    for day_offset in range(tenure_days):
        current_date = start_date + timedelta(days=day_offset)
        if current_date.weekday() == 6:  # skip Sundays
            continue
        status = "present" if random.random() < attendance_prob else "absent"
        site = random.choice(worker_sites)
        records.append({
            "worker_id": worker_id,
            "worker_name": worker_name,
            "archetype": archetype,  # keep this for now, so we can sanity-check later
            "site": site,
            "date": current_date.isoformat(),
            "status": status
        })

df = pd.DataFrame(records)
df.to_csv("synthetic_attendance.csv", index=False)
print(f"Generated {len(df)} attendance records for {NUM_WORKERS} workers.")
print(df['archetype'].value_counts())