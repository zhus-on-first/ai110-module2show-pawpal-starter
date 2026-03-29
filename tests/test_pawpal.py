from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    task = Task(name="Morning Walk", time="07:00", duration=30, frequency="daily", priority="high")
    assert not task.completed

    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task(name="Walk", time="07:00", duration=30, frequency="daily", priority="high"))
    assert len(pet.tasks) == 1
