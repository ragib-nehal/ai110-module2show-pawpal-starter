from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Pet:
    name: str
    species: str
    age: int
    energy_level: str
    special_needs: list = field(default_factory=list)

    def get_energy_level(self) -> str:
        pass

    def add_special_need(self, need: str) -> None:
        pass

    def display_info(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferences: dict = None, constraints: list = None):
        self._name = name
        self._pets: list[Pet] = []
        self._available_time_per_day = available_time_per_day
        self._preferences = preferences if preferences is not None else {}
        self._constraints = constraints if constraints is not None else []

    def get_available_time(self) -> int:
        pass

    def set_preference(self, key: str, value) -> None:
        pass

    def is_available(self, time_slot: str) -> bool:
        pass

    def add_pet(self, pet: Pet) -> None:
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    frequency: str
    description: str
    preferred_time: str | list = ""

    def get_priority_score(self) -> int:
        pass

    def can_fit(self, available_minutes: int) -> bool:
        pass

    def is_due_today(self, day: str) -> bool:
        pass


class Schedule:
    def __init__(self, pet: Pet, owner: Owner):
        self._pet = pet
        self._owner = owner
        self._weekly_plan: dict[str, list[Task]] = {}
        self._generated_at: datetime = None
        self._explanation: str = ""

    def get_day_plan(self, day: str) -> list[Task]:
        pass

    def total_time_for_day(self, day: str) -> int:
        pass

    def add_scheduled_task(self, day: str, task: Task, time: str) -> None:
        pass

    def is_feasible(self) -> bool:
        pass

    def get_explanation(self) -> str:
        pass


class Scheduler:
    def __init__(self, pet: Pet, owner: Owner, all_tasks: list[Task]):
        self._pet = pet
        self._owner = owner
        self._all_tasks = all_tasks

    def generate_schedule(self) -> Schedule:
        pass

    def calculate_task_priority(self, task: Task) -> int:
        pass

    def fit_tasks_in_day(self, day: str, available_tasks: list[Task]) -> list[Task]:
        pass

    def explain_scheduling_decision(self, task: Task, day: str, time: str) -> str:
        pass
