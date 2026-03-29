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
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list["Task"] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, name: str):
        pass


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def remove_pet(self, name: str):
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        pass

    def sort_by_time(self) -> list[Task]:
        pass

    def filter_by_status(self, completed: bool) -> list[Task]:
        pass

    def detect_conflicts(self) -> list[str]:
        pass

    def handle_recurring_tasks(self):
        pass