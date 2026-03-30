# PawPal+ Project Reflection

## 1. System Design

The three core actions a user can take in the app are:

- Entering owner and pet information
- Adding/editing care tasks with durations and priorities
- Viewing and managing a prioritized daily care schedule based on the entered information and tasks

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

1. `Owner`: Represents the pet owner. Responsible for managing the collection of pets.

    Attributes:
    - `name: str`
    - `pets: list[Pet]`

    Methods:
    - `add_pet(pet: Pet)`
    - `remove_pet(name: str)`
    - `get_all_tasks() -> list[Task]`

2. `Pet`: Represents a pet belonging to an owner. Stores pet details and its associated care tasks.

    Attributes:
    - `name: str`
    - `species: str`
    - `tasks: list[Task]`

    Methods:
    - `add_task(task: Task)`
    - `remove_task(name: str)`

3. `Task`: Represents a single care activity. Uses a dataclass for clean attribute management.

    Attributes:
    - `name: str`
    - `time: str`
    - `duration: int`
    - `frequency: str`
    - `priority: str`
    - `completed: bool`

    Methods: `mark_complete()`

4. `Scheduler`: The system's brain. Retrieves tasks across all pets and applies algorithmic logic to organize them.

    Attributes: `owner: Owner`

    Methods:
    - `get_all_tasks() -> list[Task]`
    - `sort_by_time() -> list[Task]`
    - `filter_by_status(completed: bool) -> list[Task]`
    - `detect_conflicts() -> list[str]`
    - `handle_recurring_tasks()`

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

No structural changes were made to the UML, but the following risks and tradeoffs were identified during skeleton review and will be addressed during implementation:

- **`Scheduler.get_all_tasks()` delegates to `Owner.get_all_tasks()`** to avoid duplicating aggregation logic and prevent drift between the two methods.
- **No unique IDs for `Pet` or `Task`**: Name-based lookup (`remove_pet(name)`, `remove_task(name)`) assumes unique names. Duplicate names may cause ambiguous deletes. Acceptable tradeoff for this project's scope.
- **No format validation on `time`, `frequency`, or `priority`**: These are free-form strings. Downstream sorting and filtering logic will assume a consistent format (e.g., `"HH:MM"` for time, `"daily"`/`"weekly"` for frequency).
- **Conflict detection and recurring task logic** carry known complexity risks (O(n²) and mutation-while-iterating respectively) — to be addressed carefully in Phase 4.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The primary constraint is time. I also included duration, frequency, and priority.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler does not consider travel time between locations or task durations that might extend beyond their original schedules.

In other words, conflict detection only looks at direct inputted times and if there's overlap.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

LLM was used throughout — for brainstorming class responsibilities, drafting the UML,
generating the class skeleton, and reviewing potential logic bottlenecks before
implementation. The most useful prompts were specific and structural, such as asking
about risks in a particular design pattern or syntax.

I explored the settings for LLM/agent/MCP integration in VS Code. I also compared to Pycharm. I explored these settings. Changed some to see what would happen. I looked at some the feature's documentation, but honestly VS Code's documentation is not as good as it should be. Probably because the features are changing so fast.

Both Pycharm and Vs Code's settings page is a hot mess. There is so much, but Pycharm is better organized for my brain.

There are things I like about both. One thing is for certain. The integration and development is fast.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The LLM did not always suggest the best code. There were some surprisingly not Pythonic suggestions - simple ones. Overall, the suggestions kept the context really well as well as my style.

I can understand now why reviewing LLM generated code can be overwhelming. I cannot just take it for granted. I have to make sure it passes human judgement. Plus, I am responsible for the overall performance. I need to process and maintain understanding of what is being implemented. I see challenges to just unleashing agents and all that brute computer to large programming tasks. When LLM ceases to be a partner and I just become a reviewer, I will never compete and I will lose control of the project.

Sure, testing in main and QAing the product helps, but that's not deep enough.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Testing is always important to verify not just behavior but also assumptions.
`main.py` is a good smoke test — it shows the system working end to end — but
unit tests are more precise. They isolate each behavior independently, so when
something breaks you know exactly which method failed and why, rather than having
to trace through the whole system to find the source.

There are 10 tests. These tests matter because they verify the foundation the entire app depends on.
A bug in `mark_complete()` or `sort_by_time()` would silently break the schedule  display and conflict detection.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Moderately confident in happy path behavior — all ten tests pass. Edge cases not
yet covered include: two pets with the same name, tasks with malformed time strings
passed to `sort_by_time()`, an owner with no pets, and recurring task behavior when
a mix of completed and incomplete tasks exist for the same pet. A filter test for
completed tasks (not just pending) would also add confidence.

All tests are unit tests. There are no automated integration tests — `main.py`
serves as a manual integration check, verifying that the full Owner → Pet → Task →
Scheduler chain works end to end in the terminal.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The separation of concerns between `pawpal_system.py`, `app.py`, and `main.py`
worked well. Having a CLI demo script made it easy to verify logic independently
before connecting it to Streamlit.

I enjoyed experimenting with LLM. I pushed myself not to worry too much that it generated code that would take me longer to write myself. I focused on experimenting with the tool and what I felt and learned in the process. I focused on how I want to learn and use the tool. I realize I have no desire to let it program for me and for me to be a reviewer of last resort.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

There are many more dynamic and complex algorithms and setups. Immediate ones are: Add unique IDs to `Pet` and `Task` to avoid ambiguous name-based deletes. Also add input validation on `time` and `frequency` fields so the system fails gracefully on bad input rather than silently skipping tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The tool is changing fast. There's still much for developers to do to harness its power. The "harnesses" and tooling around it all is developing. No doubt it will change software development and engineering. The same forces of not enough time, money, and other resources still exist. Though it's clear that simple to "just do it with AI" is a dumb thing to wield. But it's not new. It's unmitigated stress.
