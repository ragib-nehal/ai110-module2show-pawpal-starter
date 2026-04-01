# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

# Run all tests
pytest test/

# Run a single test
pytest test/test_pawpal.py::test_mark_complete_changes_status
```

## Architecture

All core logic lives in `pawpal_system.py`. The Streamlit UI in `app.py` imports from it directly — there is no separate API layer.

**Data model:**
- `Pet` (dataclass) — holds name, species, age, energy level, tasks list, and a back-reference to its `Owner`
- `Task` (dataclass) — holds scheduling metadata; `frequency` is either `"daily"`, `"once"`, or `"weekly:<DayName>"` (e.g. `"weekly:Monday"`)
- `Owner` — tracks available minutes per day and owns a list of `Pet` objects

**Scheduling pipeline:**
1. `Scheduler` — generates a `Schedule` for a single pet by iterating over days, filtering tasks by `is_due_today`, then greedily fitting them in priority order via `fit_tasks_in_day`
2. `Schedule` — stores the weekly plan as `{day: [{task, time}, ...]}` and records an explanation log
3. `OwnerScheduler` — coordinates across all pets; detects cross-pet time conflicts by summing all pets' daily minutes against `owner.available_time_per_day`; `resolve_conflict` bumps the lowest-priority task to the next day

**UI flow (`app.py`):** Owner → Add Pets → Add Tasks → Generate Schedule. State is kept in `st.session_state`. Tasks are stored in both `pet.tasks` (on the `Pet` object) and `st.session_state.tasks_per_pet` (keyed by pet name) — both must stay in sync when adding tasks.

`main.py` is a standalone script version of the same flow, useful for quick testing without the UI.
