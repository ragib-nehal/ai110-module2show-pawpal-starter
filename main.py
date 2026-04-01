from pawpal_system import Owner, Pet, Task, Scheduler, OwnerScheduler
from datetime import datetime

# --- Setup ---
owner = Owner(name="Alex", available_time_per_day=120)

buddy = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
whiskers = Pet(name="Whiskers", species="Cat", age=5, energy_level="low")

owner.add_pet(buddy)
owner.add_pet(whiskers)

# --- Tasks for Buddy (added out of order by preferred_time) ---
buddy_tasks = [
    Task(title="Fetch Training", duration_minutes=20, priority="medium",
         frequency="daily", description="Practice fetch in the yard",
         preferred_time="14:00"),
    Task(title="Morning Walk", duration_minutes=30, priority="high",
         frequency="daily", description="Walk around the block",
         preferred_time="08:00"),
    Task(title="Vet Checkup", duration_minutes=60, priority="low",
         frequency="weekly:Monday", description="Monthly health check",
         preferred_time="10:30"),
    # Intentional conflict: same time slot as Whiskers' "Feeding" task (08:00)
    Task(title="Morning Meds", duration_minutes=5, priority="high",
         frequency="daily", description="Give Buddy his joint supplement",
         preferred_time="08:00"),
]

# --- Tasks for Whiskers (added out of order by preferred_time) ---
whiskers_tasks = [
    Task(title="Grooming", duration_minutes=15, priority="medium",
         frequency="weekly:Wednesday", description="Brush coat",
         preferred_time="14:00"),
    Task(title="Feeding", duration_minutes=10, priority="high",
         frequency="daily", description="Wet food in the morning",
         preferred_time="08:00"),
    Task(title="Playtime", duration_minutes=20, priority="low",
         frequency="daily", description="Feather wand play session",
         preferred_time=""),
]

# Mark one task complete to test filtering
whiskers_tasks[2].mark_complete()  # Playtime is done

# --- Generate Consolidated Schedule ---
tasks_per_pet = {
    buddy.name: buddy_tasks,
    whiskers.name: whiskers_tasks,
}

owner_scheduler = OwnerScheduler(owner, [buddy, whiskers], tasks_per_pet)
owner_scheduler.generate_consolidated_schedule()

today = datetime.now().strftime("%A")

# --- 1. Default daily summary (unfiltered) ---
print(f"=== Today's Schedule ({today}) — Unfiltered ===\n")
daily_summary = owner_scheduler.get_daily_summary(today)
for pet_name, entries in daily_summary.items():
    print(f"  [{pet_name}]")
    if not entries:
        print("    No tasks scheduled today.")
    for entry in entries:
        task = entry["task"]
        print(f"    {entry['time']} - {task.title} ({task.duration_minutes} min) "
              f"[{task.priority} priority] [completed={task.completed}]")
    print()

# --- 2. sort_by_time demo: sort raw task lists before scheduling ---
print("=== Tasks Sorted by preferred_time ===\n")
for pet, tasks in [(buddy, buddy_tasks), (whiskers, whiskers_tasks)]:
    scheduler = Scheduler(pet, owner, tasks)
    sorted_tasks = scheduler.sort_by_time(tasks)
    print(f"  [{pet.name}]")
    for t in sorted_tasks:
        time_label = t.preferred_time if t.preferred_time else "(no time set)"
        print(f"    {time_label} - {t.title} [{t.priority} priority]")
    print()

# --- 3. filter_tasks: single pet ---
print(f"=== filter_tasks: Buddy Only ({today}) ===\n")
filtered = owner_scheduler.filter_tasks(today, pet_name="Buddy")
for pet_name, entries in filtered.items():
    print(f"  [{pet_name}]")
    if not entries:
        print("    No tasks.")
    for entry in entries:
        print(f"    {entry['time']} - {entry['task'].title} [completed={entry['task'].completed}]")
print()

# --- 4. filter_tasks: incomplete tasks only ---
print(f"=== filter_tasks: Incomplete Tasks Only ({today}) ===\n")
filtered = owner_scheduler.filter_tasks(today, completed=False)
for pet_name, entries in filtered.items():
    print(f"  [{pet_name}]")
    if not entries:
        print("    No incomplete tasks.")
    for entry in entries:
        print(f"    {entry['time']} - {entry['task'].title}")
print()

# --- 5. filter_tasks: completed tasks only ---
print(f"=== filter_tasks: Completed Tasks Only ({today}) ===\n")
filtered = owner_scheduler.filter_tasks(today, completed=True)
for pet_name, entries in filtered.items():
    print(f"  [{pet_name}]")
    if not entries:
        print("    No completed tasks.")
    for entry in entries:
        print(f"    {entry['time']} - {entry['task'].title}")
print()

# --- Conflict Report (time budget) ---
print("=== Conflict Report ===")
print(owner_scheduler.get_conflict_report())

# --- Time-Slot Conflict Report ---
print("\n=== Time-Slot Conflict Report ===")
print(owner_scheduler.get_time_slot_conflict_report())
