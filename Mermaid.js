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
        + get_energy_level() str
        + add_special_need(need: str) void
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
        + get_priority_score() int
        + can_fit(available_minutes: int) bool
        + is_due_today(day: str) bool
    }

    class Schedule {
        - pet: Pet
        - owner: Owner
        - weekly_plan: dict~str, list~Task~~
        - generated_at: datetime
        - explanation: str
        + get_day_plan(day: str) list~Task~
        + total_time_for_day(day: str) int
        + add_scheduled_task(day: str, task: Task, time: str) void
        + is_feasible() bool
        + get_explanation() str
    }

    class Scheduler {
        - pet: Pet
        - owner: Owner
        - all_tasks: list~Task~
        + generate_schedule() Schedule
        + calculate_task_priority(task: Task) int
        + fit_tasks_in_day(day: str, available_tasks: list~Task~) list~Task~
        + explain_scheduling_decision(task: Task, day: str, time: str) str
    }

    %% Relationships
    Owner "1" --> "*" Pet : owns
    Schedule --> Pet : has
    Schedule --> Owner : has
    Schedule *-- Task : contains
    Scheduler --> Pet : uses
    Scheduler --> Owner : uses
    Scheduler o-- Task : aggregates
    Scheduler --> Schedule : creates
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
