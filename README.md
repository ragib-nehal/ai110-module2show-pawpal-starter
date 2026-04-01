# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Three features were added to `pawpal_system.py` to make the scheduler more intelligent:

**Automatic task recurrence**: when `task.mark_complete()` is called on a `daily` or `weekly` task, it now returns a new `Task` instance due on the next occurrence (today + 1 day for daily, today + 7 days for weekly). One-time tasks return `None`. Callers add the returned task back to the pet to keep the schedule rolling forward.

**Due-date awareness**: `Task` has a new optional `due_date` field. `is_due_today()` respects it: a task with a future `due_date` is silently skipped by the scheduler until that date arrives. This prevents a just-completed recurring task from being re-scheduled the same day its successor is created.

**Time-slot conflict detection**: `OwnerScheduler.detect_time_slot_conflicts()` scans every day's plan across all pets and reports any time slot where two or more tasks overlap. It returns plain warning strings rather than raising exceptions, so the app stays running and the owner can decide how to resolve the clash. `get_time_slot_conflict_report()` formats those warnings into a single printable string.

## Testing PawPal+

### Running the tests

```bash
python -m pytest test/
```

To run a single test by name:

```bash
python -m pytest test/test_pawpal.py::test_mark_complete_changes_status
```

### What the tests cover

| Area | Tests |
|---|---|
| **Sorting correctness** | Tasks with `preferred_time` are sorted chronologically; timed tasks always schedule before untimed ones; untimed tasks sort high → medium → low priority |
| **Recurrence logic** | Daily tasks produce a next task due +1 day; weekly tasks produce one due +7 days; one-time tasks return `None`; recurred tasks preserve title, duration, and priority |
| **Conflict detection** | Daily time-budget conflicts are reported when combined pet tasks exceed `available_time_per_day`; time-slot conflicts are flagged when two tasks share the same start time; no false positives for a single pet with one task |
| **Task basics** | Tasks start incomplete; `mark_complete` sets the flag; pets track task counts correctly |

### Confidence Level

★★★★☆ (4/5)

The core scheduling behaviors — priority sorting, recurrence, and conflict detection — are all verified and passing. Confidence is held back from 5 stars because the time-slot conflict check assumes a fixed 08:00 start with no overlap handling across a real wall-clock range, and the UI layer (`app.py`) has no automated test coverage.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
