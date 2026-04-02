// PawPal+ Class Diagram (Mermaid.js)
// This diagram defines the class structure for the PawPal+ pet care planning system

const classDigram = `
classDiagram
    class Pet {
        - name: str
        - species: str
        - age: int
        - energy_level: str
        - special_needs: list
        - tasks: list
        + get_energy_level() str
        + add_special_need(need: str) void
        + add_task(task: Task) void
        + display_info() str
    }

    class Owner {
        - name: str
        - pets: list~Pet~
        - available_time_per_day: int
        - preferences: dict
        - constraints: list
        + get_available_time() int
        + set_preference(key: str, value) void
        + is_available(time_slot: str) bool
        + add_pet(pet: Pet) void
    }

    class Task {
        - title: str
        - duration_minutes: int
        - priority: str
        - frequency: str
        - description: str
        - preferred_time: str|list
        - pet_requirements: list
        - completed: bool
        - due_date: date
        + mark_complete() Task
        + get_priority_score() int
        + can_fit(available_minutes: int) bool
        + is_due_today(day: str) bool
    }

    class Schedule {
        - pet: Pet
        - owner: Owner
        - weekly_plan: dict~str, list~
        - generated_at: datetime
        - explanation: str
        - conflicts: list
        + get_day_plan(day: str) list
        + total_time_for_day(day: str) int
        + add_scheduled_task(day: str, task: Task, time: str) void
        + is_feasible() bool
        + get_explanation() str
        + set_explanation(explanation: str) void
        + get_conflicts() list
    }

    class Scheduler {
        - pet: Pet
        - owner: Owner
        - all_tasks: list~Task~
        + generate_schedule() Schedule
        + calculate_task_priority(task: Task) int
        + fit_tasks_in_day(day: str, available_tasks: list~Task~) list~Task~
        + sort_by_time(tasks: list~Task~) list~Task~
        + explain_scheduling_decision(task: Task, day: str, time: str) str
    }

    class OwnerScheduler {
        - owner: Owner
        - pets: list~Pet~
        - tasks_per_pet: dict~str, list~
        - schedules: dict~str, Schedule~
        - dropped_tasks: dict~str, list~
        + generate_consolidated_schedule() dict
        + detect_time_conflicts() list
        + resolve_conflict(conflict: dict) void
        + get_daily_summary(day: str) dict
        + is_overbooked() bool
        + suggest_consolidated_tasks() list
        + filter_tasks(day: str, pet_name: str, completed: bool) dict
        + get_conflict_report() str
        + get_dropped_tasks() dict
        + detect_time_slot_conflicts() list
        + get_time_slot_conflict_report() str
    }

    %% Relationships
    Owner "1" --> "*" Pet : owns
    Pet --> Owner : back-reference
    Pet "1" --> "*" Task : has
    Schedule --> Pet : for
    Schedule --> Owner : constrained by
    Scheduler --> Pet : schedules for
    Scheduler --> Owner : respects limits
    Scheduler o-- Task : aggregates
    Scheduler --> Schedule : creates
    OwnerScheduler --> Owner : coordinates
    OwnerScheduler --> Pet : iterates
    OwnerScheduler ..> Scheduler : uses per pet
    OwnerScheduler ..> Schedule : stores per pet
`;

/**
 * Class Relationships:
 * - Owner owns one or more Pets (1-to-many)
 * - Schedule has a Pet and Owner reference
 * - Schedule composes a list of Task objects (tasks belong to the schedule)
 * - Scheduler aggregates a Task list (tasks exist independently)
 * - Scheduler receives Pet, Owner, and Task list
 * - Scheduler creates and returns a Schedule object
 */

/**
 * Design Specifications:
 * - Duration: Tasks can be 15, 30, 45, or 60 minutes
 * - Frequency: Simple string (daily, twice_daily, every_2_days, weekly, as_needed)
 * - Schedule Scope: 7-day weekly plan
 * - Architecture: Scheduler (separate from Schedule) generates optimal schedules
 */

module.exports = classDigram;
