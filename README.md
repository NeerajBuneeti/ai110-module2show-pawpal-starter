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

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

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
