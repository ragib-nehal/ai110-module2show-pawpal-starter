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
        # add to the selected pet object
        selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        selected_pet.add_task(task)
        # store in tasks_per_pet for the scheduler
        st.session_state.tasks_per_pet[selected_pet_name].append(task)
        st.success(f"Task '{task_title}' added to {selected_pet_name}.")

    # show tasks per pet
    if "tasks_per_pet" in st.session_state:
        for pname, ptasks in st.session_state.tasks_per_pet.items():
            if ptasks:
                st.markdown(f"**{pname}**")
                st.table([
                    {"title": t.title, "duration_minutes": t.duration_minutes,
                     "priority": t.priority, "frequency": t.frequency}
                    for t in ptasks
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
    today = datetime.now().strftime("%A")
    st.markdown(f"### Today's Plan ({today})")

    daily_summary = st.session_state.owner_scheduler.get_daily_summary(today)
    any_tasks = False
    for pet_name, entries in daily_summary.items():
        if entries:
            any_tasks = True
            st.markdown(f"**{pet_name}**")
            for entry in entries:
                task = entry["task"]
                st.markdown(f"- {task.title} — {task.duration_minutes} min `{task.priority} priority`")

    if not any_tasks:
        st.info("No tasks scheduled for today.")

    st.divider()
    conflict_report = st.session_state.owner_scheduler.get_conflict_report()
    if conflict_report != "No conflicts detected.":
        st.error(conflict_report)
    else:
        st.success(conflict_report)

    with st.expander("Scheduling Log"):
        for pet_name, schedule in st.session_state.owner_scheduler._schedules.items():
            st.markdown(f"**{pet_name}**")
            st.text(schedule.get_explanation())
