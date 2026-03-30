# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

### Core Functionality
- ✅ **Owner Management** - Set available time per day, manage preferences
- ✅ **Pet Management** - Add/remove pets with type (dog, cat, rabbit, bird, hamster), age, and preferences
- ✅ **Task Management** - Create tasks with duration, priority (1-5), category, and frequency (daily/weekly/as-needed)
- ✅ **Daily Schedule Generation** - Automatically creates optimized schedule within time constraints
- ✅ **Schedule Explanation** - Shows reasoning behind task ordering and why tasks were/weren't included

### Smart Algorithms (Phase 4)
#### Sorting
- **Sort by Urgency Score** - Tasks prioritized by `priority × frequency_multiplier` (daily tasks get 1.5x boost)
- **Sort by Time** - Tasks ordered chronologically by scheduled HH:MM time

#### Filtering  
- **Filter by Pet** - View tasks for a specific pet
- **Filter by Priority** - Show only high-priority tasks (≥ threshold)
- **Filter by Status** - Separate completed vs. incomplete tasks

#### Intelligent Scheduling
- **Automated Time Slot Assignment** - Tasks assigned sequential time slots starting at 8:00 AM
- **Conflict Detection** - Warns when tasks are scheduled at the same time
- **Feasibility Validation** - Ensures schedules don't exceed owner's available time

#### Recurring Tasks
- **Daily Task Automation** - Daily tasks automatically recreate for tomorrow when marked complete
- **Weekly Task Automation** - Weekly tasks auto-generate 7 days later
- **Property Preservation** - Recurring tasks inherit duration, priority, and category

### UI Features (Phase 6)
- **Smart Task View** - Inline sorting and filtering without page refresh
- **Visual Metrics** - Dashboard showing scheduled tasks, total time, feasibility status
- **Time-Based Display** - Schedule shows specific time slots (08:00, 08:30, etc.)
- **Conflict Warnings** - Highlighted alerts when scheduling conflicts detected
- **Interactive Pet Management** - Quick add/remove pets with inline display
- **Comprehensive Task Breakdown** - Detailed view with urgency scores, categories, and status

### Advanced Features (Challenge 2 & 3)

#### Challenge 2: Data Persistence 💾
- **JSON Serialization** - Save all pets and tasks to `data.json` automatically
- **Auto-Load on Startup** - App loads saved data when restarted, no data loss
- **Full State Preservation** - Maintains all pet info, task details, and scheduling state
- **Manual Save/Load** - Methods available for custom save/load workflows

To test data persistence:
```bash
python3 test_persistence.py
```

#### Challenge 3: Priority-Based UI Colors 🎨
- **Priority Color Coding** - Tasks show emoji indicators:
  - 🔴 **High** (Priority 4-5)
  - 🟡 **Medium** (Priority 3)  
  - 🟢 **Low** (Priority 1-2)
- **Enhanced Task Visibility** - Quickly identify high-priority tasks at a glance
- **Consistent Throughout UI** - Color coding applied in task tables and schedule breakdown
- **Visual Schedule Clarity** - Priority level displayed prominently in daily schedule

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

### Running Demos

```bash
# CLI demo with owner, pets, and schedule
python3 main.py

# Phase 4 algorithms demo (sorting, filtering, conflicts, recurrence)
python3 phase4_demo.py

# Data persistence test (Challenge 2)
python3 test_persistence.py
```

## Implementation Notes: Using AI for Advanced Features

### Challenge 2: Data Persistence Implementation

**Approach:** Used Copilot to design a clean JSON serialization pattern.

**Prompt Used:** 
> "Add `to_dict()` and `from_dict()` methods to the Owner class in pawpal_system.py that handle nested Pet and Task objects. Make sure dates are converted to ISO format strings for JSON compatibility."

**Copilot's Solution:**
- `to_dict()` - Recursively converts the entire owner object tree to nested dictionaries
- `from_dict()` - Reconstructs the full owner hierarchy from dictionaries
- Handles date serialization using ISO format (`date.fromisoformat()`)
- Type-safe restoration of all task properties

**Integration:** 
- Added `save_owner_data()` and `load_owner_data()` helper functions in `app.py`
- App loads from `data.json` at startup (if exists)
- Saves to `data.json` after any pet/task modification
- No database required—simple JSON provides sufficient persistence

**Why This Approach:**
- JSON is human-readable and easily debugged
- Python's `dataclass` fields map directly to dict keys
- Zero external dependencies (no marshmallow, no SQLite)
- Fast enough for a daily scheduler (file I/O is negligible)

### Challenge 3: Priority-Based Color Coding

**Approach:** Added visual indicators using emoji-based priority labels.

**Implementation:**
```python
def get_priority_display(priority: int) -> str:
    """Return emoji and label for priority level."""
    if priority >= 4:
        return "🔴 High"
    elif priority >= 3:
        return "🟡 Medium"
    else:
        return "🟢 Low"
```

**Applied Throughout UI:**
- Task lists show priority with color emoji
- Schedule breakdown displays priority level prominently  
- Consistent visual language across all views

**Why Emojis:**
- Streamlit natively supports emoji rendering
- Emojis are color-blind friendly (shape + color redundancy)
- Visual scanning is faster than reading "Priority 4/5"
- Works across multiple languages

## Running the App

```bash
streamlit run app.py
```

### Running Demos

```bash
# CLI demo with owner, pets, and schedule
python3 main.py

# Phase 4 algorithms demo (sorting, filtering, conflicts, recurrence)
python3 phase4_demo.py

# Data persistence test (Challenge 2)
python3 test_persistence.py
```

## System Architecture

See [uml_diagram.md](uml_diagram.md) for the complete UML class diagram showing:
- 5-class architecture: Owner, Pet, Task, Schedule, Scheduler
- Class relationships and dependencies
- All methods including Phase 4 algorithms
- Design principles and separation of concerns

Quick overview:
- **Owner** - Manages time constraints and pet aggregation
- **Pet** - Represents pet characteristics and care needs
- **Task** - Individual care activity with priority and urgency
- **Schedule** - Daily plan with feasibility validation
- **Scheduler** - Orchestrates scheduling algorithm with sorting, filtering, and conflict detection

## Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling (Phase 4)

PawPal+ now includes intelligent algorithmic features:

### Sorting & Filtering
- **Sort by Urgency**: Tasks ordered by priority × frequency multiplier (daily tasks get 1.5x boost)
- **Sort by Time**: Tasks sorted by scheduled time in HH:MM format
- **Filter by Pet**: Show only tasks for a specific pet
- **Filter by Priority**: Show only high-priority tasks (e.g., priority ≥ 4)
- **Filter by Status**: Show completed vs. incomplete tasks

### Recurring Task Automation
- **Daily Tasks**: Automatically create next occurrence for tomorrow when marked complete
- **Weekly Tasks**: Auto-generate 7 days later
- **As-Needed Tasks**: No automatic recurrence

### Conflict Detection
- Identifies tasks scheduled at the same time for same or different pets
- Returns warning messages without crashing
- Helps prevent double-booking of owner's time

### Time-Based Scheduling
- Automatic time slot assignment starting at 8:00 AM
- Sequential task scheduling based on duration
- Readable schedule display with times (e.g., "08:00 | Morning walk | 30 min")

## Testing PawPal+ (Phase 5)

PawPal+ has comprehensive test coverage ensuring reliability and correctness across all features.

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/test_pawpal.py -v

# Run tests for a specific class
python3 -m pytest tests/test_pawpal.py::TestScheduler -v

# Run tests for Phase 4 algorithms only
python3 -m pytest tests/test_pawpal.py::TestPhase4Algorithms -v
```

### Test Coverage

**62 tests** covering all system components:

#### Phase 1-3: Core System (45 tests)
- **Owner Management** (7 tests): Creation, pet aggregation, task collection, preferences
- **Pet Management** (8 tests): Creation, care needs by type, task management
- **Task Management** (11 tests): Urgency scoring, completion tracking, frequency handling, pet matching
- **Schedule Planning** (8 tests): Feasibility checks, duration calculation, task ordering
- **Scheduler Algorithm** (10 tests): Task filtering, arrangement, plan generation, validation
- **Integration Tests** (1 test): Full workflow from owner creation to daily plan generation

#### Phase 4: Algorithmic Layer (17 tests)
- **Sorting Algorithms** (4 tests): By urgency score, by time, handling edge cases
- **Filtering Algorithms** (6 tests): By pet, by completion status, by priority
- **Conflict Detection** (3 tests): Identifying same-time tasks, handling conflicts
- **Recurring Tasks** (3 tests): Daily/weekly recurrence, property preservation
- **Combined Workflows** (1 test): Filter + sort + conflict check in realistic scenarios

### Test Strategies

1. **Unit Testing**: Individual class methods tested in isolation
2. **Integration Testing**: Multi-class workflows tested end-to-end
3. **Edge Case Coverage**: Empty lists, null values, boundary priority levels
4. **Algorithm Verification**: Sorting order, filtering accuracy, conflict detection

### Running Demos

```bash
# CLI demo with owner, pets, and schedule
python3 main.py

# Phase 4 algorithms demo
python3 phase4_demo.py
```

### Confidence Level

**⭐⭐⭐⭐⭐ (5/5 stars)**

- All 62 tests passing consistently
- Phase 4 algorithms verified by both tests and demo script
- Edge cases covered (empty lists, conflicts, boundaries)
- Manual UI testing shows correct integration with Streamlit
- Full system workflow validated from owner creation to schedule generation
