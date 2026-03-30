#!/usr/bin/env python3
"""
Phase 4: Algorithmic Layer Demo

Demonstrates new features:
- Sorting tasks by urgency and time
- Filtering by pet, priority, and completion status
- Automated recurring task creation
- Conflict detection in schedules
"""

from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_sorting_and_filtering():
    """Demonstrate sorting and filtering algorithms."""
    print_section("Phase 4a: Sorting & Filtering Algorithms")
    
    # Setup
    owner = Owner(name="Alice", available_time_per_day=120)
    dog = Pet(name="Max", pet_type="dog", age=3)
    owner.add_pet(dog)
    
    # Create tasks with different priorities (out of order)
    tasks_data = [
        ("Evening walk", 20, 4, "walk", "daily"),
        ("Morning walk", 30, 5, "walk", "daily"),
        ("Dog feeding", 10, 5, "feeding", "daily"),
        ("Play time", 15, 2, "play", "daily"),
        ("Grooming", 45, 3, "grooming", "weekly"),
    ]
    
    for name, duration, priority, category, frequency in tasks_data:
        task = Task(
            name=name,
            duration=duration,
            priority=priority,
            category=category,
            pet_id=dog.name,
            frequency=frequency
        )
        dog.add_task(task)
    
    scheduler = Scheduler(owner)
    
    # TEST 1: Sort by Urgency
    print("\n📊 SORTING BY URGENCY SCORE (highest first):")
    print("-" * 60)
    urgency_sorted = scheduler.sort_by_urgency()
    for i, task in enumerate(urgency_sorted, 1):
        print(f"{i}. {task.name:20} | Urgency: {task.get_urgency_score():4.1f} | Priority: {task.priority}")
    
    # TEST 2: Filter by Pet
    print("\n🐕 FILTERING BY PET 'Max':")
    print("-" * 60)
    max_tasks = scheduler.filter_by_pet("Max")
    print(f"Tasks for Max: {len(max_tasks)} total")
    for task in max_tasks:
        print(f"  • {task.name} ({task.category})")
    
    # TEST 3: Filter by Priority
    print("\n⭐ FILTERING BY PRIORITY >= 4:")
    print("-" * 60)
    high_priority = scheduler.filter_by_priority(4)
    for task in high_priority:
        print(f"  • {task.name}: Priority {task.priority}/5")


def demo_recurring_tasks():
    """Demonstrate automated recurring task creation."""
    print_section("Phase 4b: Automated Recurring Tasks")
    
    # Create a daily task
    daily_task = Task(
        name="Morning walk",
        duration=30,
        priority=5,
        category="walk",
        pet_id="Max",
        frequency="daily",
        due_date=date(2026, 3, 30)
    )
    
    print(f"\n📋 Original Task:")
    print(f"  Name: {daily_task.name}")
    print(f"  Frequency: {daily_task.frequency}")
    print(f"  Due Date: {daily_task.due_date}")
    
    # Mark complete and generate next occurrence
    daily_task.mark_complete()
    print(f"\n✅ Task marked complete!")
    
    next_task = daily_task.generate_next_occurrence()
    print(f"\n📋 Next Occurrence (Auto-generated):")
    print(f"  Name: {next_task.name}")
    print(f"  Frequency: {next_task.frequency}")
    print(f"  Due Date: {next_task.due_date}")
    print(f"  Completed: {next_task.completed}")
    
    # Demo with weekly task
    print("\n" + "-" * 60)
    weekly_task = Task(
        name="Grooming",
        duration=45,
        priority=3,
        category="grooming",
        pet_id="Max",
        frequency="weekly",
        due_date=date(2026, 3, 30)
    )
    
    print(f"\n📋 Weekly Task:")
    print(f"  Name: {weekly_task.name}")
    print(f"  Due Date: {weekly_task.due_date}")
    
    next_weekly = weekly_task.generate_next_occurrence()
    print(f"\n📋 Next Weekly Occurrence (7 days later):")
    print(f"  Due Date: {next_weekly.due_date}")


def demo_conflict_detection():
    """Demonstrate conflict detection in schedules."""
    print_section("Phase 4c: Conflict Detection Algorithm")
    
    # Setup
    owner = Owner(name="Alice", available_time_per_day=120)
    dog = Pet(name="Max", pet_type="dog", age=3)
    cat = Pet(name="Whiskers", pet_type="cat", age=5)
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Add tasks that will conflict
    task1 = Task(
        name="Dog morning walk",
        duration=30,
        priority=5,
        category="walk",
        pet_id="Max",
        frequency="daily",
        scheduled_time="08:00"  # Same time as task2
    )
    
    task2 = Task(
        name="Cat feeding",
        duration=10,
        priority=5,
        category="feeding",
        pet_id="Whiskers",
        frequency="daily",
        scheduled_time="08:00"  # CONFLICT!
    )
    
    task3 = Task(
        name="Dog feeding",
        duration=10,
        priority=5,
        category="feeding",
        pet_id="Max",
        frequency="daily",
        scheduled_time="09:00"  # No conflict
    )
    
    dog.add_task(task1)
    cat.add_task(task2)
    dog.add_task(task3)
    
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_plan()
    
    print("\n📅 GENERATED SCHEDULE:")
    print("-" * 60)
    for task in schedule.get_ordered_tasks():
        print(f"  {task.scheduled_time} | {task.name:20} | {task.pet_id}")
    
    # Detect conflicts
    conflicts = scheduler.detect_conflicts(schedule)
    
    if conflicts:
        print("\n⚠️  CONFLICTS DETECTED:")
        for conflict in conflicts:
            print(f"  {conflict}")
    else:
        print("\n✅ No conflicts detected!")
    
    # Show full reasoning with conflicts
    print("\n📖 SCHEDULE EXPLANATION:")
    print("-" * 60)
    explanation = scheduler.explain_reasoning(schedule)
    print(explanation)


def demo_filter_completion_status():
    """Demonstrate filtering by completion status."""
    print_section("Phase 4d: Filter by Completion Status")
    
    owner = Owner(name="Alice", available_time_per_day=120)
    dog = Pet(name="Max", pet_type="dog", age=3)
    owner.add_pet(dog)
    
    # Create multiple tasks
    task1 = Task(
        name="Morning walk",
        duration=30,
        priority=5,
        category="walk",
        pet_id="Max",
        frequency="daily"
    )
    task2 = Task(
        name="Dog feeding",
        duration=10,
        priority=5,
        category="feeding",
        pet_id="Max",
        frequency="daily"
    )
    task3 = Task(
        name="Play time",
        duration=15,
        priority=3,
        category="play",
        pet_id="Max",
        frequency="daily"
    )
    
    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task3)
    
    # Mark some as complete
    task1.mark_complete()
    task2.mark_complete()
    
    scheduler = Scheduler(owner)
    
    print("\n✅ COMPLETED TASKS:")
    print("-" * 60)
    completed = scheduler.filter_by_completion_status(True)
    for task in completed:
        print(f"  ✓ {task.name}")
    
    print("\n⬜ INCOMPLETE TASKS:")
    print("-" * 60)
    incomplete = scheduler.filter_by_completion_status(False)
    for task in incomplete:
        print(f"  ◻ {task.name}")


def main():
    """Run all Phase 4 demos."""
    print("\n" + "=" * 60)
    print("  PawPal+ Phase 4: Algorithmic Layer Demo")
    print("=" * 60)
    print("Showcasing: Sorting, Filtering, Recurring Tasks, Conflict Detection")
    
    demo_sorting_and_filtering()
    demo_recurring_tasks()
    demo_filter_completion_status()
    demo_conflict_detection()
    
    print_section("Phase 4 Demo Complete")
    print("✓ Sorting & filtering algorithms functional")
    print("✓ Recurring task automation working")
    print("✓ Conflict detection operational")
    print("✓ Completion status tracking verified")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
