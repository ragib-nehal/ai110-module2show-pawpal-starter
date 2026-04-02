import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, OwnerScheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Owner Setup ---
st.subheader("Owner")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_time = st.number_input("Available minutes/day", min_value=10, max_value=480, value=120)

if st.button("Save Owner"):
    st.session_state.owner = Owner(name=owner_name, available_time_per_day=int(available_time))
    st.success(f"Owner '{owner_name}' saved!")

if "owner" in st.session_state:
    st.caption(f"Owner: **{st.session_state.owner.name}** | {st.session_state.owner.get_available_time()} min/day")

st.divider()

# --- Add Pet ---
st.subheader("Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    energy_level = st.selectbox("Energy level", ["low", "medium", "high"])

if st.button("Add Pet"):
    if "owner" not in st.session_state:
        st.error("Please save an owner first.")
    else:
        new_pet = Pet(name=pet_name, species=species, age=0, energy_level=energy_level)
        st.session_state.owner.add_pet(new_pet)
        if "tasks_per_pet" not in st.session_state:
            st.session_state.tasks_per_pet = {}
        st.session_state.tasks_per_pet[new_pet.name] = []
        st.success(f"Added {pet_name} to {st.session_state.owner.name}'s pets!")

if "owner" in st.session_state and st.session_state.owner.pets:
    pets = ", ".join(p.name for p in st.session_state.owner.pets)
    st.caption(f"Pets: **{pets}**")

st.divider()

# --- Task Input ---
st.subheader("Add a Task")

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

def priority_badge(priority: str) -> str:
    colors = {"high": "🔴", "medium": "🟠", "low": "🟢"}
    return colors.get(priority, "⚪")

if "owner" in st.session_state and st.session_state.owner.pets:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Assign task to", pet_names)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly:Monday", "weekly:Wednesday", "weekly:Friday", "once"])

    if st.button("Add Task"):
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            frequency=frequency,
            description="",
        )
        selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        selected_pet.add_task(task)
        st.session_state.tasks_per_pet[selected_pet_name].append(task)
        st.success(f"Task '{task_title}' added to {selected_pet_name}.")

    # show tasks per pet, sorted by priority
    if "tasks_per_pet" in st.session_state:
        for pname, ptasks in st.session_state.tasks_per_pet.items():
            if ptasks:
                st.markdown(f"**{pname}**")
                sorted_tasks = sorted(ptasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 99))
                st.table([
                    {
                        "priority": f"{priority_badge(t.priority)} {t.priority}",
                        "title": t.title,
                        "duration (min)": t.duration_minutes,
                        "frequency": t.frequency,
                    }
                    for t in sorted_tasks
                ])
else:
    st.info("Add an owner and at least one pet before adding tasks.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    if "owner" not in st.session_state or not st.session_state.owner.pets:
        st.error("Please save an owner and add at least one pet first.")
    elif "tasks_per_pet" not in st.session_state or not any(st.session_state.tasks_per_pet.values()):
        st.warning("Add at least one task before generating a schedule.")
    else:
        tasks_per_pet = {
            pet_name: tasks
            for pet_name, tasks in st.session_state.tasks_per_pet.items()
        }
        owner_scheduler = OwnerScheduler(
            st.session_state.owner,
            st.session_state.owner.pets,
            tasks_per_pet,
        )
        owner_scheduler.generate_consolidated_schedule()
        st.session_state.owner_scheduler = owner_scheduler
        st.success("Schedule generated!")

if "owner_scheduler" in st.session_state:
    os_ = st.session_state.owner_scheduler
    today = datetime.now().strftime("%A")
    daily_limit = st.session_state.owner.get_available_time()

    # --- Today's Plan ---
    st.markdown(f"### Today's Plan ({today})")

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        pet_options = ["All pets"] + [p.name for p in st.session_state.owner.pets]
        filter_pet = st.selectbox("Filter by pet", pet_options, key="filter_pet")
    with filter_col2:
        filter_status = st.selectbox("Filter by status", ["All", "Incomplete only", "Completed only"], key="filter_status")

    filter_pet_arg = None if filter_pet == "All pets" else filter_pet
    filter_completed_arg = None if filter_status == "All" else (filter_status == "Completed only")

    daily_summary = os_.filter_tasks(today, pet_name=filter_pet_arg, completed=filter_completed_arg)
    any_tasks = False
    today_total = 0

    for pet_name, entries in daily_summary.items():
        if entries:
            any_tasks = True
            pet_total = sum(e["task"].duration_minutes for e in entries)
            today_total += pet_total
            st.markdown(f"**{pet_name}** — {pet_total} min")
            for i, entry in enumerate(entries):
                task = entry["task"]
                badge = priority_badge(task.priority)
                col_task, col_btn = st.columns([5, 1])
                with col_task:
                    title_fmt = f"~~{task.title}~~" if task.completed else f"**{task.title}**"
                    st.markdown(
                        f"&nbsp;&nbsp;&nbsp;`{entry['time']}` &nbsp; {badge} {title_fmt} — {task.duration_minutes} min"
                    )
                with col_btn:
                    if task.completed:
                        st.markdown("✓ Done")
                    else:
                        if st.button("✓ Done", key=f"complete_{pet_name}_{i}_{entry['time']}"):
                            pet_tasks = st.session_state.tasks_per_pet[pet_name]
                            task_idx = next((j for j, t in enumerate(pet_tasks) if t is task), None)
                            if task_idx is not None:
                                next_task = pet_tasks[task_idx].mark_complete()
                                if next_task is not None:
                                    pet_tasks.append(next_task)
                            new_scheduler = OwnerScheduler(
                                st.session_state.owner,
                                st.session_state.owner.pets,
                                st.session_state.tasks_per_pet,
                            )
                            new_scheduler.generate_consolidated_schedule()
                            st.session_state.owner_scheduler = new_scheduler
                            st.rerun()

    if any_tasks:
        if today_total > daily_limit:
            st.warning(f"Total today: **{today_total} min** — over your {daily_limit} min/day limit by {today_total - daily_limit} min")
        else:
            st.success(f"Total today: **{today_total} min** of {daily_limit} min available")
    else:
        st.info("No tasks scheduled for today.")

    st.divider()

    # --- Consolidated task tip ---
    shared = os_.suggest_consolidated_tasks()
    if shared:
        st.info(f"Tip: these tasks appear across multiple pets and could be done together: **{', '.join(shared)}**")

    # --- Dropped Tasks ---
    st.markdown("### Skipped Tasks")

    dropped = os_.get_dropped_tasks()
    if dropped:
        for day, entries in dropped.items():
            total_dropped_min = sum(e["task"].duration_minutes for e in entries)
            st.warning(
                f"**{day}:** {len(entries)} task(s) couldn't fit "
                f"({total_dropped_min} min over your {daily_limit} min/day limit)"
            )
            for e in entries:
                badge = priority_badge(e["task"].priority)
                st.markdown(
                    f"&nbsp;&nbsp;&nbsp;{badge} **{e['task'].title}** "
                    f"({e['pet']}) — {e['task'].duration_minutes} min `{e['task'].priority} priority`"
                )
    else:
        st.success("All tasks fit within your daily time budget.")

    st.divider()

    # --- Full Weekly Schedule ---
    with st.expander("Full Weekly Schedule"):
        from pawpal_system import DAYS
        for pet_name, schedule in os_._schedules.items():
            st.markdown(f"**{pet_name}**")
            rows = []
            for day in DAYS:
                entries = schedule.get_day_plan(day)
                if entries:
                    tasks_str = ", ".join(
                        f"{e['time']} {priority_badge(e['task'].priority)} {e['task'].title} ({e['task'].duration_minutes}m)"
                        for e in entries
                    )
                    day_total = schedule.total_time_for_day(day)
                    rows.append({"day": day, "tasks": tasks_str, "total min": day_total})
                else:
                    rows.append({"day": day, "tasks": "—", "total min": 0})
            st.table(rows)

    # --- Scheduling Log ---
    with st.expander("Scheduling Log"):
        for pet_name, schedule in os_._schedules.items():
            st.markdown(f"**{pet_name}**")
            st.text(schedule.get_explanation())
