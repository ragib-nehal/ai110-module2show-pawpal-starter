import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


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
