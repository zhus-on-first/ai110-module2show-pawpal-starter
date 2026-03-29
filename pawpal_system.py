from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    time: str
    duration: int
    frequency: str
    priority: str
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, name: str):
        """Remove the first task with the matching name and return whether one was removed."""

        for i, task in enumerate(self.tasks):
            if task.name == name:
                del self.tasks[i]
                return True
        return False


class Owner:
    """
    Represents an owner of pets with associated functionalities.

    The Owner class is used to manage pets and tasks associated with them. An instance
    of Owner holds a collection of pets and provides methods to add new pets, remove
    them by name, and retrieve all tasks assigned to those pets.
    """

    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, name: str):
        """Remove the first pet with the matching name and return whether one was removed."""

        for i, pet in enumerate(self.pets):
            if pet.name == name:
                del self.pets[i]
                return True
        return False

    def get_all_tasks(self) -> list[Task]:
        """Return a flattened list of all tasks assigned to the owner's pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def _time_to_minutes(self, time_str: str) -> int:
        """
        Convert 'HH:MM' (24-hour) to minutes after midnight.
        Raises ValueError for invalid format/range.
        """
        parts = time_str.strip().split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid time format: {time_str}")

        hour = int(parts[0])
        minute = int(parts[1])

        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError(f"Invalid time value: {time_str}")

        return hour * 60 + minute

    def get_all_tasks(self) -> list[Task]:
        # Delegate to Owner to avoid duplicated flattening logic
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> list[Task]:
        """Return all tasks sorted by valid start time, with invalid times placed last."""
        tasks = self.get_all_tasks()

        # Valid times first, invalid times last (stable ordering within each group)
        def sort_key(task: Task):
            try:
                return (0, self._time_to_minutes(task.time))
            except ValueError:
                return (1, float("inf"))

        return sorted(tasks, key=sort_key)

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return all tasks whose completion status matches the requested value."""
        return [task for task in self.get_all_tasks() if task.completed == completed]

    def detect_conflicts(self) -> list[str]:
        """
        Detect overlapping tasks across all pets.
        Conflict if startA < endB and startB < endA.
        """
        conflicts: list[str] = []

        # Build list with parsed times; skip invalid-time tasks
        timed_tasks: list[tuple[Task, int, int]] = []
        for task in self.get_all_tasks():
            try:
                start = self._time_to_minutes(task.time)
                end = start + max(0, task.duration)
                timed_tasks.append((task, start, end))
            except ValueError:
                # Could optionally report malformed times as conflicts/warnings
                continue

        # Sort by start time for efficient overlap checks
        timed_tasks.sort(key=lambda item: item[1])

        # Sweep: compare each task only with subsequent tasks that might overlap
        n = len(timed_tasks)
        for i in range(n):
            current_task, current_start, current_end = timed_tasks[i]

            j = i + 1
            while j < n and timed_tasks[j][1] < current_end:
                next_task, next_start, next_end = timed_tasks[j]
                if current_start < next_end and next_start < current_end:
                    conflicts.append(
                        f"Conflict: '{current_task.name}' ({current_task.time}, {current_task.duration}m) "
                        f"overlaps with '{next_task.name}' ({next_task.time}, {next_task.duration}m)"
                    )
                j += 1

        return conflicts

    def handle_recurring_tasks(self):
        """Reset completed daily tasks to incomplete while leaving other recurring tasks unchanged.

        Basic recurring behavior:
        - Daily tasks reset to incomplete after completion.
        - Weekly/monthly tasks are left as-is (could be date-driven in a fuller version).
        """
        for task in self.get_all_tasks():
            if task.frequency.lower() == "daily" and task.completed:
                task.completed = False
