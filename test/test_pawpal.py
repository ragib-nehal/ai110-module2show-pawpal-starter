import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler, OwnerScheduler


def make_task(**kwargs):
    defaults = dict(
        title="Test Task",
        duration_minutes=30,
        priority="medium",
        frequency="daily",
        description="A test task",
    )
    defaults.update(kwargs)
    return Task(**defaults)


# --- Task Completion Tests ---

def test_task_starts_incomplete():
    task = make_task()
    assert task.completed is False


def test_mark_complete_changes_status():
    task = make_task()
    task.mark_complete()
    assert task.completed is True


def test_mark_complete_is_idempotent():
    task = make_task()
    task.mark_complete()
    task.mark_complete()
    assert task.completed is True


# --- Pet Task Addition Tests ---

def test_pet_starts_with_no_tasks():
    pet = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
    assert len(pet.tasks) == 0


def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
    task = make_task(title="Walk")
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_add_multiple_tasks_increases_count():
    pet = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
    pet.add_task(make_task(title="Walk"))
    pet.add_task(make_task(title="Feed"))
    pet.add_task(make_task(title="Play"))
    assert len(pet.tasks) == 3


def test_added_task_is_retrievable():
    pet = Pet(name="Whiskers", species="Cat", age=5, energy_level="low")
    task = make_task(title="Grooming")
    pet.add_task(task)
    assert pet.tasks[0].title == "Grooming"


# --- Sorting Correctness Tests ---

def make_owner(minutes=120):
    return Owner(name="Alex", available_time_per_day=minutes)


def test_sort_by_time_returns_chronological_order():
    """Tasks with preferred_time are sorted earliest-first."""
    owner = make_owner()
    pet = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
    tasks = [
        make_task(title="Afternoon Walk", preferred_time="14:00"),
        make_task(title="Morning Feed",   preferred_time="07:00"),
        make_task(title="Midday Play",    preferred_time="12:00"),
    ]
    scheduler = Scheduler(pet, owner, tasks)
    sorted_tasks = scheduler.sort_by_time(tasks)
    times = [t.preferred_time for t in sorted_tasks]
    assert times == sorted(times)


def test_fit_tasks_schedules_timed_before_untimed():
    """Timed tasks always appear before untimed tasks in the fitted list."""
    owner = make_owner(minutes=120)
    pet = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
    tasks = [
        make_task(title="Untimed High", priority="high", preferred_time=""),
        make_task(title="Timed Low",    priority="low",  preferred_time="09:00"),
    ]
    scheduler = Scheduler(pet, owner, tasks)
    fitted = scheduler.fit_tasks_in_day("Monday", tasks)
    assert fitted[0].title == "Timed Low"
    assert fitted[1].title == "Untimed High"


def test_fit_tasks_sorts_untimed_by_priority():
    """Among untimed tasks, higher priority comes first."""
    owner = make_owner(minutes=120)
    pet = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
    tasks = [
        make_task(title="Low Task",    priority="low",    preferred_time=""),
        make_task(title="High Task",   priority="high",   preferred_time=""),
        make_task(title="Medium Task", priority="medium", preferred_time=""),
    ]
    scheduler = Scheduler(pet, owner, tasks)
    fitted = scheduler.fit_tasks_in_day("Monday", tasks)
    titles = [t.title for t in fitted]
    assert titles == ["High Task", "Medium Task", "Low Task"]


# --- Recurrence Logic Tests ---

def test_daily_task_recurs_next_day():
    """mark_complete on a daily task returns a new task due the following day."""
    today = date.today()
    task = make_task(frequency="daily", due_date=today)
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_weekly_task_recurs_seven_days_later():
    """mark_complete on a weekly task returns a new task due 7 days later."""
    today = date.today()
    task = make_task(frequency="weekly:Monday", due_date=today)
    next_task = task.mark_complete()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)
    assert next_task.completed is False


def test_once_task_does_not_recur():
    """mark_complete on a one-time task returns None."""
    task = make_task(frequency="once")
    assert task.mark_complete() is None


def test_recurrence_preserves_task_metadata():
    """The recurred task keeps the same title, duration, and priority."""
    today = date.today()
    task = make_task(title="Bath", duration_minutes=45, priority="high",
                     frequency="daily", due_date=today)
    next_task = task.mark_complete()
    assert next_task.title == "Bath"
    assert next_task.duration_minutes == 45
    assert next_task.priority == "high"


# --- Conflict Detection Tests ---

def test_no_conflict_when_pets_fit_within_daily_limit():
    """Two pets whose combined tasks stay within the daily limit → no conflicts."""
    owner = make_owner(minutes=60)
    pet1 = Pet(name="Buddy",    species="Dog", age=3, energy_level="high")
    pet2 = Pet(name="Whiskers", species="Cat", age=5, energy_level="low")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    tasks_per_pet = {
        "Buddy":    [make_task(title="Walk", duration_minutes=20)],
        "Whiskers": [make_task(title="Feed", duration_minutes=10)],
    }
    os_ = OwnerScheduler(owner, [pet1, pet2], tasks_per_pet)
    os_.generate_consolidated_schedule()
    assert os_.detect_time_conflicts() == []


def test_conflict_detected_when_pets_exceed_daily_limit():
    """Two pets whose combined tasks exceed the daily limit → conflict reported."""
    owner = make_owner(minutes=60)
    pet1 = Pet(name="Buddy",    species="Dog", age=3, energy_level="high")
    pet2 = Pet(name="Whiskers", species="Cat", age=5, energy_level="low")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    tasks_per_pet = {
        "Buddy":    [make_task(title="Walk", duration_minutes=40)],
        "Whiskers": [make_task(title="Feed", duration_minutes=40)],
    }
    os_ = OwnerScheduler(owner, [pet1, pet2], tasks_per_pet)
    os_.generate_consolidated_schedule()
    conflicts = os_.detect_time_conflicts()
    assert len(conflicts) > 0
    assert conflicts[0]["total_minutes"] > conflicts[0]["limit"]


def test_time_slot_conflict_detected_for_same_start_time():
    """Two tasks scheduled at the exact same time slot triggers a slot-level warning."""
    owner = make_owner(minutes=120)
    pet1 = Pet(name="Buddy",    species="Dog", age=3, energy_level="high")
    pet2 = Pet(name="Whiskers", species="Cat", age=5, energy_level="low")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    # Both tasks have the same preferred_time so the Scheduler places them at 08:00
    tasks_per_pet = {
        "Buddy":    [make_task(title="Walk", preferred_time="08:00", duration_minutes=30)],
        "Whiskers": [make_task(title="Feed", preferred_time="08:00", duration_minutes=30)],
    }
    os_ = OwnerScheduler(owner, [pet1, pet2], tasks_per_pet)
    os_.generate_consolidated_schedule()
    warnings = os_.detect_time_slot_conflicts()
    assert len(warnings) > 0
    assert "08:00" in warnings[0]


def test_no_time_slot_conflict_single_pet():
    """A single pet with one task per day produces no slot-level warnings."""
    owner = make_owner(minutes=120)
    pet = Pet(name="Buddy", species="Dog", age=3, energy_level="high")
    owner.add_pet(pet)
    tasks_per_pet = {
        "Buddy": [make_task(title="Walk", preferred_time="08:00", duration_minutes=30)],
    }
    os_ = OwnerScheduler(owner, [pet], tasks_per_pet)
    os_.generate_consolidated_schedule()
    assert os_.detect_time_slot_conflicts() == []
