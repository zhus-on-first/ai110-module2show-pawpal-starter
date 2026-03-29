from pawpal_system import Owner, Pet, Scheduler, Task

# Set up owner
owner = Owner("Alex")

# Create pets
buddy = Pet(name="Buddy", species="Dog")
whiskers = Pet(name="Whiskers", species="Cat")

# Add tasks OUT OF ORDER to demonstrate sorting
buddy.add_task(Task(name="Evening Walk",    time="18:00", duration=30, frequency="daily",   priority="high"))
buddy.add_task(Task(name="Flea Medication", time="09:00", duration=5,  frequency="monthly", priority="medium"))
buddy.add_task(Task(name="Morning Walk",    time="07:00", duration=30, frequency="daily",   priority="high"))

# Add tasks to Whiskers — including a conflict with Buddy's Flea Medication (09:00)
whiskers.add_task(Task(name="Vet Appointment", time="14:30", duration=60, frequency="weekly", priority="high"))
whiskers.add_task(Task(name="Breakfast",        time="08:00", duration=10, frequency="daily",  priority="high"))
whiskers.add_task(Task(name="Playtime",         time="19:00", duration=20, frequency="daily",  priority="low"))
whiskers.add_task(Task(name="Morning Grooming", time="09:00", duration=15, frequency="daily",  priority="medium"))

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Create scheduler
scheduler = Scheduler(owner)

# --- Today's Schedule ---
print(f"=== Today's Schedule for {owner.name} ===\n")

sorted_tasks = scheduler.sort_by_time()
for task in sorted_tasks:
    status = "[x]" if task.completed else "[ ]"
    print(f"  {status} {task.time}  {task.name:<20} ({task.duration} min | {task.frequency} | priority: {task.priority})")

# Conflict warnings
print()
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("--- Scheduling Conflicts Detected ---")
    for conflict in conflicts:
        print(f"  ! {conflict}")
else:
    print("No scheduling conflicts detected.")

# Pending vs completed summary
pending   = scheduler.filter_by_status(completed=False)
completed = scheduler.filter_by_status(completed=True)
print(f"\nSummary: {len(pending)} pending, {len(completed)} completed out of {len(sorted_tasks)} total tasks.")
