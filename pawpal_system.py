from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Pet:
    name: str
    species: str
    age: int
    energy_level: str
    special_needs: list = field(default_factory=list)
    tasks: list = field(default_factory=list)
    owner: Optional['Owner'] = field(default=None, repr=False)

    def get_energy_level(self) -> str:
        """Return the pet's energy level."""
        return self.energy_level

    def add_special_need(self, need: str) -> None:
        """Append a special need to the pet's special needs list."""
        self.special_needs.append(need)

    def add_task(self, task: 'Task') -> None:
        """Append a task to the pet's task list."""
        self.tasks.append(task)

    def display_info(self) -> str:
        """Return a formatted string with the pet's details."""
        needs = ", ".join(self.special_needs) if self.special_needs else "None"
        return (
            f"Name: {self.name}\n"
            f"Species: {self.species}\n"
            f"Age: {self.age}\n"
            f"Energy Level: {self.energy_level}\n"
            f"Special Needs: {needs}"
        )


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferences: dict = None, constraints: list = None):
        self._name = name
        self._pets: list[Pet] = []
        self._available_time_per_day = available_time_per_day
        self._preferences = preferences if preferences is not None else {}
        self._constraints = constraints if constraints is not None else []

    @property
    def name(self) -> str:
        """Return the owner's name."""
        return self._name

    @property
    def pets(self) -> list[Pet]:
        """Return the list of pets owned."""
        return self._pets

    @property
    def preferences(self) -> dict:
        """Return the owner's scheduling preferences."""
        return self._preferences

    @property
    def constraints(self) -> list:
        """Return the owner's time slot constraints."""
        return self._constraints

    def get_available_time(self) -> int:
        """Return the owner's available minutes per day."""
        return self._available_time_per_day

    def set_preference(self, key: str, value) -> None:
        """Set a scheduling preference by key."""
        self._preferences[key] = value

    def is_available(self, time_slot: str) -> bool:
        """Return True if the given time slot is not in the owner's constraints."""
        return time_slot not in self._constraints

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list and link the owner back to the pet."""
        self._pets.append(pet)
        pet.owner = self


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    frequency: str
    description: str
    preferred_time: str | list = ""
    pet_requirements: list = field(default_factory=list)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def get_priority_score(self) -> int:
        """Return a numeric priority score: high=3, medium=2, low=1."""
        scores = {"high": 3, "medium": 2, "low": 1}
        return scores.get(self.priority.lower(), 0)

    def can_fit(self, available_minutes: int) -> bool:
        """Return True if the task duration fits within the available minutes."""
        return self.duration_minutes <= available_minutes

    def is_due_today(self, day: str) -> bool:
        """Return True if the task should be scheduled on the given day."""
        if self.frequency == "daily":
            return True
        if self.frequency == "once":
            return True
        # supports "weekly:Monday" or a list of days like ["Monday", "Wednesday"]
        if isinstance(self.frequency, list):
            return day in self.frequency
        if self.frequency.startswith("weekly:"):
            return day == self.frequency.split(":")[1]
        return False


class Schedule:
    def __init__(self, pet: Pet, owner: Owner):
        self._pet = pet
        self._owner = owner
        self._weekly_plan: dict[str, list[Task]] = {}
        self._generated_at: datetime = None
        self._explanation: str = ""
        self._conflicts: list = []

    def get_day_plan(self, day: str) -> list[Task]:
        """Return the list of scheduled task entries for the given day."""
        return self._weekly_plan.get(day, [])

    def total_time_for_day(self, day: str) -> int:
        """Return the total scheduled minutes for the given day."""
        return sum(entry["task"].duration_minutes for entry in self.get_day_plan(day))

    def add_scheduled_task(self, day: str, task: Task, time: str) -> None:
        """Add a task entry with a time slot to the given day's plan."""
        if day not in self._weekly_plan:
            self._weekly_plan[day] = []
        self._weekly_plan[day].append({"task": task, "time": time})

    def is_feasible(self) -> bool:
        """Return True if no day exceeds the owner's available daily time."""
        available = self._owner.get_available_time()
        return all(self.total_time_for_day(day) <= available for day in self._weekly_plan)

    def get_explanation(self) -> str:
        """Return the scheduling explanation log."""
        return self._explanation

    def set_explanation(self, explanation: str) -> None:
        """Set the scheduling explanation log."""
        self._explanation = explanation

    def get_conflicts(self) -> list:
        """Return the list of detected scheduling conflicts."""
        return self._conflicts


class Scheduler:
    def __init__(self, pet: Pet, owner: Owner, all_tasks: list[Task]):
        self._pet = pet
        self._owner = owner
        self._all_tasks = all_tasks

    def generate_schedule(self) -> Schedule:
        """Build and return a weekly Schedule for the pet by fitting tasks into each day."""
        schedule = Schedule(self._pet, self._owner)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            due_today = [t for t in self._all_tasks if t.is_due_today(day)]
            fitted = self.fit_tasks_in_day(day, due_today)
            time_cursor = "08:00"
            for task in fitted:
                schedule.add_scheduled_task(day, task, time_cursor)
                explanation = self.explain_scheduling_decision(task, day, time_cursor)
                schedule.set_explanation(schedule.get_explanation() + explanation + "\n")
        schedule._generated_at = datetime.now()
        return schedule

    def calculate_task_priority(self, task: Task) -> int:
        """Return the task's priority score, boosted if it matches a pet special need."""
        score = task.get_priority_score()
        if task.title.lower() in [need.lower() for need in self._pet.special_needs]:
            score += 1
        return score

    def fit_tasks_in_day(self, day: str, available_tasks: list[Task]) -> list[Task]:
        """Return a greedy list of tasks that fit within the owner's daily time limit."""
        sorted_tasks = sorted(available_tasks, key=lambda t: self.calculate_task_priority(t), reverse=True)
        fitted = []
        remaining = self._owner.get_available_time()
        for task in sorted_tasks:
            if task.can_fit(remaining):
                fitted.append(task)
                remaining -= task.duration_minutes
        return fitted

    def explain_scheduling_decision(self, task: Task, day: str, time: str) -> str:
        """Return a human-readable string explaining why a task was placed on a given day and time."""
        return (
            f"[{day} {time}] '{task.title}' scheduled "
            f"(priority={task.get_priority_score()}, duration={task.duration_minutes}min)"
        )


class OwnerScheduler:
    def __init__(self, owner: Owner, pets: list[Pet], tasks_per_pet: dict[str, list[Task]]):
        self._owner = owner
        self._pets = pets
        self._tasks_per_pet = tasks_per_pet  # {pet.name: [Task, ...]}
        self._schedules: dict[str, Schedule] = {}

    def generate_consolidated_schedule(self) -> dict[str, Schedule]:
        """Generate and store a Schedule for each pet, returning all schedules by pet name."""
        for pet in self._pets:
            tasks = self._tasks_per_pet.get(pet.name, [])
            scheduler = Scheduler(pet, self._owner, tasks)
            self._schedules[pet.name] = scheduler.generate_schedule()
        return self._schedules

    def detect_time_conflicts(self) -> list[dict]:
        """Return a list of days where total scheduled time across all pets exceeds the owner's limit."""
        conflicts = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        available = self._owner.get_available_time()
        for day in days:
            total = sum(
                schedule.total_time_for_day(day)
                for schedule in self._schedules.values()
            )
            if total > available:
                conflicts.append({"day": day, "total_minutes": total, "limit": available})
        return conflicts

    def resolve_conflict(self, conflict: dict) -> None:
        """Bump the lowest-priority task from the conflicted day to the next day."""
        day = conflict["day"]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        next_day = days[(days.index(day) + 1) % len(days)]
        for schedule in self._schedules.values():
            plan = schedule.get_day_plan(day)
            if not plan:
                continue
            # bump the lowest-priority task to the next day
            lowest = min(plan, key=lambda e: e["task"].get_priority_score())
            plan.remove(lowest)
            schedule.add_scheduled_task(next_day, lowest["task"], lowest["time"])
            schedule._conflicts.append(conflict)
            break

    def get_daily_summary(self, day: str) -> dict[str, list[Task]]:
        """Return a dict of pet name to scheduled task entries for the given day."""
        return {
            pet_name: schedule.get_day_plan(day)
            for pet_name, schedule in self._schedules.items()
        }

    def is_overbooked(self) -> bool:
        """Return True if any day has more scheduled time than the owner allows."""
        return len(self.detect_time_conflicts()) > 0

    def suggest_consolidated_tasks(self) -> list[str]:
        """Return task titles that appear in more than one pet's schedule."""
        from collections import Counter
        all_titles = [
            entry["task"].title
            for schedule in self._schedules.values()
            for entries in schedule._weekly_plan.values()
            for entry in entries
        ]
        counts = Counter(all_titles)
        return [title for title, count in counts.items() if count > 1]

    def get_conflict_report(self) -> str:
        """Return a formatted string summarizing all scheduling conflicts."""
        conflicts = self.detect_time_conflicts()
        if not conflicts:
            return "No conflicts detected."
        lines = []
        for c in conflicts:
            lines.append(
                f"{c['day']}: {c['total_minutes']} min scheduled, limit is {c['limit']} min "
                f"(over by {c['total_minutes'] - c['limit']} min)"
            )
        return "\n".join(lines)
