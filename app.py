import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

if "pet" not in st.session_state:
    st.session_state.pet = Pet(name="", species="")

# --- Owner & Pet Info ---
st.subheader("Owner & Pet Info")

owner_name = st.text_input("Owner name", value="Jordan")
st.session_state.owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
st.session_state.pet.name = pet_name
st.session_state.pet.species = species

# Register pet with owner if not already added
if st.session_state.pet not in st.session_state.owner.pets:
    st.session_state.owner.add_pet(st.session_state.pet)

# --- Add Tasks ---
st.subheader("Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    task_time = st.text_input("Time (HH:MM)", value="09:00")
with col3:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])

if st.button("Add task"):
    task = Task(
        name=task_title,
        time=task_time,
        duration=int(duration),
        frequency=frequency,
        priority=priority,
    )
    st.session_state.pet.add_task(task)
    st.success(f"Added task: {task_title}")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    sorted_tasks = st.session_state.scheduler.sort_by_time()
    conflicts = st.session_state.scheduler.detect_conflicts()

    if sorted_tasks:
        st.subheader("Today's Schedule")
        st.table([{
            "Task": t.name,
            "Time": t.time,
            "Duration": f"{t.duration} min",
            "Frequency": t.frequency,
            "Priority": t.priority,
            "Done": "✅" if t.completed else "⬜",
        } for t in sorted_tasks])
    else:
        st.info("No tasks scheduled yet. Add some tasks above.")

    if conflicts:
        st.subheader("⚠️ Conflicts Detected")
        for c in conflicts:
            st.warning(c)
    else:
        st.success("No scheduling conflicts detected.")

    pending = st.session_state.scheduler.filter_by_status(completed=False)
    completed = st.session_state.scheduler.filter_by_status(completed=True)
    st.caption(f"{len(pending)} pending, {len(completed)} completed out of {len(sorted_tasks)} total tasks.")