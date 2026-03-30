from pawpal_system import Owner, Pet, Scheduler, Task


# --- Helpers ---
def make_scheduler(*pets):
    owner = Owner(name="Alex")

    for pet in pets:
        owner.add_pet(pet)

    return Scheduler(owner=owner)


# --- Task ---
def test_mark_complete_changes_status():
    task = Task(name="Morning Walk", time="07:00", duration=30, frequency="daily", priority="high")
    assert not task.completed

    task.mark_complete()
    assert task.completed


# --- Pet ---
def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task(name="Walk", time="07:00", duration=30, frequency="daily", priority="high"))
    assert len(pet.tasks) == 1


def test_remove_task_decreases_count():
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(Task(name="Walk", time="07:00", duration=30, frequency="daily", priority="high"))

    removed = pet.remove_task("Walk")

    assert removed
    assert len(pet.tasks) == 0


def test_remove_task_returns_false_when_not_found():
    pet = Pet(name="Buddy", species="Dog")

    assert not pet.remove_task("Nonexistent")


def test_pet_with_no_tasks():
    pet = Pet(name="Buddy", species="Dog")
    scheduler = make_scheduler(pet)

    assert scheduler.get_all_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []


# --- Sorting ---
def test_sort_by_time_returns_chronological_order():
    pet = Pet(name="Buddy", species="Dog")

    pet.add_task(Task(name="Evening Walk", time="18:00", duration=30, frequency="daily", priority="high"))
    pet.add_task(Task(name="Morning Walk", time="07:00", duration=30, frequency="daily", priority="high"))
    pet.add_task(Task(name="Breakfast",    time="08:00", duration=10, frequency="daily", priority="high"))

    scheduler = make_scheduler(pet)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]

    assert times == ["07:00", "08:00", "18:00"]


# --- Filtering ---
def test_filter_by_status_pending():
    pet = Pet(name="Buddy", species="Dog")

    t1 = Task(name="Walk",      time="07:00", duration=30, frequency="daily", priority="high")
    t2 = Task(name="Breakfast", time="08:00", duration=10, frequency="daily", priority="high")

    t2.mark_complete()

    pet.add_task(t1)
    pet.add_task(t2)

    scheduler = make_scheduler(pet)

    pending = scheduler.filter_by_status(completed=False)

    assert len(pending) == 1
    assert pending[0].name == "Walk"


# --- Conflict Detection ---
def test_detect_conflicts_flags_overlapping_tasks():
    pet = Pet(name="Buddy", species="Dog")

    pet.add_task(Task(name="Task A", time="09:00", duration=30, frequency="daily", priority="high"))
    pet.add_task(Task(name="Task B", time="09:15", duration=30, frequency="daily", priority="high"))

    scheduler = make_scheduler(pet)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Task A" in conflicts[0]
    assert "Task B" in conflicts[0]


def test_detect_conflicts_no_overlap():
    pet = Pet(name="Buddy", species="Dog")

    pet.add_task(Task(name="Task A", time="09:00", duration=30, frequency="daily", priority="high"))
    pet.add_task(Task(name="Task B", time="10:00", duration=30, frequency="daily", priority="high"))

    scheduler = make_scheduler(pet)

    assert scheduler.detect_conflicts() == []


# --- Recurring Tasks ---
def test_recurring_daily_task_creates_new_instance():
    pet = Pet(name="Buddy", species="Dog")

    task = Task(name="Walk", time="07:00", duration=30, frequency="daily", priority="high")
    pet.add_task(task)

    scheduler = make_scheduler(pet)
    task.mark_complete()

    before = len(pet.tasks)
    scheduler.handle_recurring_tasks()

    assert len(pet.tasks) == before + 1
    new_task = pet.tasks[-1]

    assert not new_task.completed
    assert new_task.name == "Walk"


def test_recurring_monthly_task_does_not_create_new_instance():
    pet = Pet(name="Buddy", species="Dog")

    task = Task(name="Flea Med", time="09:00", duration=5, frequency="monthly", priority="medium")
    pet.add_task(task)

    task.mark_complete()

    scheduler = make_scheduler(pet)
    before = len(pet.tasks)
    scheduler.handle_recurring_tasks()

    assert len(pet.tasks) == before
