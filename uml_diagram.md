# PawPal+ System Architecture (Final UML)

```mermaid
classDiagram
    class Owner {
        -String name
        -int available_time_per_day
        -dict preferences
        -List~Pet~ pets
        +get_available_time() int
        +add_pet(pet: Pet) void
        +get_all_tasks() List~Task~
        +set_preferences(key: str, value: any) void
        +get_info() str
    }

    class Pet {
        -String name
        -String pet_type
        -int age
        -dict preferences
        -List~String~ dietary_needs
        -List~Task~ tasks
        +get_info() str
        +get_care_needs() List~String~
        +add_task(task: Task) void
        +update_preferences(key: str, value: any) void
    }

    class Task {
        -String name
        -int duration
        -int priority
        -String category
        -String pet_id
        -String frequency
        -bool completed
        -String scheduled_time
        -Date due_date
        -String description
        +get_duration() int
        +get_urgency_score() float
        +is_required_today() bool
        +mark_complete() void
        +mark_incomplete() void
        +matches_pet_needs(pet: Pet) bool
        +generate_next_occurrence() Task
    }

    class Schedule {
        -Date date
        -Owner owner_ref
        -List~Task~ tasks
        -List~int~ task_order
        +add_task(task: Task) void
        +remove_task(idx: int) void
        +get_total_duration() int
        +is_feasible() bool
        +get_ordered_tasks() List~Task~
    }

    class Scheduler {
        -Owner owner
        -List~Pet~ pets
        -List~Task~ tasks
        +get_tasks_for_today() List~Task~
        +sort_by_urgency(tasks: List) List~Task~
        +sort_by_time(tasks: List) List~Task~
        +filter_by_pet(pet_name: str, tasks: List) List~Task~
        +filter_by_completion_status(completed: bool, tasks: List) List~Task~
        +filter_by_priority(min_priority: int, tasks: List) List~Task~
        +detect_conflicts(schedule: Schedule) List~String~
        +generate_daily_plan(date: Date) Schedule
        +arrange_tasks(time_budget: int) List~Task~
        +explain_reasoning(schedule: Schedule) str
        +validate_schedule(schedule: Schedule) bool
    }

    Owner "1" --> "*" Pet : manages
    Pet "1" --> "*" Task : contains
    Owner --> Scheduler : uses
    Scheduler --> Schedule : creates
    Schedule --> Task : includes
```

## Class Relationships

### Owner ↔ Pet (1:Many)
- Owner can manage multiple pets
- Each pet belongs to one owner
- Owner aggregates all pet tasks via `get_all_tasks()`

### Pet ↔ Task (1:Many)
- Each pet has multiple tasks
- Tasks reference their pet via `pet_id`
- Pet.add_task() adds tasks to its task list

### Owner ↔ Scheduler (1:1)
- Each owner has a scheduler instance
- Scheduler operates on owner's pets and tasks

### Scheduler ↔ Schedule (1:Many)
- Scheduler generates multiple schedules over time
- Each schedule is a daily plan created by the scheduler

### Schedule ↔ Task (Many:Many)
- Schedules contain zero or more tasks
- Tasks can appear in multiple schedules across different days

## Phase 4 Algorithmic Methods

### Sorting Algorithms
- `sort_by_urgency(tasks)` - Orders tasks by urgency score (priority × frequency_multiplier)
- `sort_by_time(tasks)` - Orders tasks by scheduled_time in HH:MM format

### Filtering Algorithms  
- `filter_by_pet(pet_name, tasks)` - Returns only tasks for specified pet
- `filter_by_completion_status(completed, tasks)` - Separates completed/incomplete tasks
- `filter_by_priority(min_priority, tasks)` - Returns tasks with priority ≥ threshold

### Conflict Detection
- `detect_conflicts(schedule)` - Identifies tasks scheduled at same time
- Returns warnings for conflicts to prevent double-booking

### Recurring Task Automation
- `Task.generate_next_occurrence()` - Creates next task instance
- Daily tasks → tomorrow, Weekly tasks → 7 days later
- Preserves all task properties (duration, priority, pet_id, etc.)

### Time-Based Scheduling
- `generate_daily_plan(date)` - Assigns HH:MM slots starting at 8:00 AM
- Sequential scheduling based on task duration
- Auto-detects and warns about conflicts

## Design Principles

1. **Separation of Concerns**
   - Business logic in `pawpal_system.py` (Owner, Pet, Task, Schedule, Scheduler)
   - UI in `app.py` (Streamlit presentation)
   - Tests in `tests/test_pawpal.py` (comprehensive coverage)

2. **Single Responsibility**
   - Owner: Manages constraints and pet aggregation
   - Pet: Represents pet characteristics and care needs
   - Task: Tracks individual care activities with urgency
   - Schedule: Builds and validates daily plans
   - Scheduler: Orchestrates scheduling algorithm

3. **Clean Interfaces**
   - Methods accept lists and return modified lists (functional style)
   - Allows chaining: filter → sort → use
   - Easy to unit test independently

4. **Stateful Persistence**
   - Streamlit `st.session_state` persists Owner object across page refreshes
   - Owner changes reflect immediately in UI via `st.rerun()`
