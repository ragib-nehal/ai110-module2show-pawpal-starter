from pawpal_system import Owner, Pet, Task, Scheduler, OwnerScheduler
from datetime import datetime

# --- Setup ---
owner = Owner(name="Alex", available_time_per_day=120)

buddy = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
whiskers = Pet(name="Whiskers", species="Cat", age=5, energy_level="low")

owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Tasks for Buddy ---
buddy_tasks = [
    Task(title="Morning Walk", duration_minutes=30, priority="high",
         frequency="daily", description="Walk around the block"),
    Task(title="Fetch Training", duration_minutes=20, priority="medium",
         frequency="daily", description="Practice fetch in the yard"),
    Task(title="Vet Checkup", duration_minutes=60, priority="low",
         frequency="weekly:Monday", description="Monthly health check"),
]

# --- Tasks for Whiskers ---
whiskers_tasks = [
    Task(title="Feeding", duration_minutes=10, priority="high",
         frequency="daily", description="Wet food in the morning"),
    Task(title="Grooming", duration_minutes=15, priority="medium",
         frequency="weekly:Wednesday", description="Brush coat"),
    Task(title="Playtime", duration_minutes=20, priority="low",
         frequency="daily", description="Feather wand play session"),
]

# --- Generate Consolidated Schedule ---
tasks_per_pet = {
    buddy.name: buddy_tasks,
    whiskers.name: whiskers_tasks,
}

owner_scheduler = OwnerScheduler(owner, [buddy, whiskers], tasks_per_pet)
owner_scheduler.generate_consolidated_schedule()

# --- Print Today's Schedule ---
today = datetime.now().strftime("%A")
print(f"=== Today's Schedule ({today}) ===\n")

daily_summary = owner_scheduler.get_daily_summary(today)

for pet_name, entries in daily_summary.items():
    print(f"  [{pet_name}]")
    if not entries:
        print("    No tasks scheduled today.")
    for entry in entries:
        task = entry["task"]
        time = entry["time"]
        print(f"    {time} - {task.title} ({task.duration_minutes} min) [{task.priority} priority]")
    print()

# --- Conflict Report ---
print("=== Conflict Report ===")
print(owner_scheduler.get_conflict_report())
