import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

# --- Owner Info ---
st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value="Jordan")
st.session_state.owner.name = owner_name

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    existing_names = [p.name for p in st.session_state.owner.pets]
    if pet_name in existing_names:
        st.warning(f"A pet named '{pet_name}' already exists.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added pet: {pet_name}")

# Show current pets
if st.session_state.owner.pets:
    st.caption("Current pets: " + ", ".join(p.name for p in st.session_state.owner.pets))

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

pet_names = [p.name for p in st.session_state.owner.pets]
if not pet_names:
    st.info("Add a pet first before scheduling tasks.")
else:
    selected_pet_name = st.selectbox("Assign to pet", pet_names)

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
        selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        selected_pet.add_task(Task(
            name=task_title,
            time=task_time,
            duration=int(duration),
            frequency=frequency,
            priority=priority,
        ))
        st.success(f"Added '{task_title}' to {selected_pet_name}")

st.divider()

# --- Schedule ---
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    sorted_tasks = st.session_state.scheduler.sort_by_time()
    conflicts = st.session_state.scheduler.detect_conflicts()

    if sorted_tasks:
        for task in sorted_tasks:
            col1, col2 = st.columns([4, 1])
            with col1:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.priority, "⚪")
                status = "✅" if task.completed else "⬜"
                st.markdown(
                    f"{status} **{task.time}** — {task.name} "
                    f"({task.duration} min | {task.frequency} | {priority_emoji} {task.priority})"
                )
            with col2:
                if not task.completed:
                    if st.button("Mark done", key=f"done_{task.name}_{task.time}"):
                        task.mark_complete()
                        st.session_state.scheduler.handle_recurring_tasks()
                        st.rerun()

        st.divider()
        if conflicts:
            st.subheader("⚠️ Conflicts Detected")
            for c in conflicts:
                st.warning(c)
        else:
            st.success("No scheduling conflicts detected.")

        pending = st.session_state.scheduler.filter_by_status(completed=False)
        completed = st.session_state.scheduler.filter_by_status(completed=True)
        st.caption(f"{len(pending)} pending, {len(completed)} completed out of {len(sorted_tasks)} total tasks.")
    else:
        st.info("No tasks scheduled yet. Add some tasks above.")
