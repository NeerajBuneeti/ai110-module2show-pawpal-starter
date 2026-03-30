#!/usr/bin/env python3
"""
PawPal+ System Demo

This script demonstrates the PawPal+ pet care scheduling system with a complete workflow:
1. Create a pet owner with available time
2. Add multiple pets with different types
3. Create various pet care tasks
4. Generate an optimized daily schedule
5. Display the schedule with reasoning
"""

from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_create_owner() -> Owner:
    """Create a pet owner with realistic constraints."""
    print_section("1. Creating Pet Owner")
    
    owner = Owner(
        name="Alice",
        available_time_per_day=120,  # 2 hours per day
        preferences={"early_walks": True, "flexible_feeding": False}
    )
    
    print(f"✓ Created: {owner.get_info()}")
    return owner


def demo_add_pets(owner: Owner) -> list:
    """Add multiple pets to the owner."""
    print_section("2. Adding Pets")
    
    pets = []
    
    # Dog
    dog = Pet(
        name="Max",
        pet_type="dog",
        age=3,
        preferences={"breed": "Golden Retriever"},
        dietary_needs="High protein, grain-free"
    )
    owner.add_pet(dog)
    pets.append(dog)
    print(f"✓ Added: {dog.get_info()}")
    print(f"  Care needs: {', '.join(dog.get_care_needs())}")
    print(f"  Dietary: {dog.dietary_needs}")
    
    # Cat
    cat = Pet(
        name="Whiskers",
        pet_type="cat",
        age=5,
        preferences={"temperament": "affectionate"},
        dietary_needs="Wet and dry food mix"
    )
    owner.add_pet(cat)
    pets.append(cat)
    print(f"✓ Added: {cat.get_info()}")
    print(f"  Care needs: {', '.join(cat.get_care_needs())}")
    
    # Rabbit
    rabbit = Pet(
        name="Hoppy",
        pet_type="rabbit",
        age=2,
        preferences={"habitat": "outdoor_hutch"},
        dietary_needs="Timothy hay and vegetables"
    )
    owner.add_pet(rabbit)
    pets.append(rabbit)
    print(f"✓ Added: {rabbit.get_info()}")
    print(f"  Care needs: {', '.join(rabbit.get_care_needs())}")
    
    return pets


def demo_create_tasks(owner: Owner, pets: list) -> None:
    """Create various pet care tasks and add to pets."""
    print_section("3. Creating Pet Care Tasks")
    
    tasks_config = [
        # Dog tasks
        {
            "name": "Morning walk",
            "pet": pets[0],
            "duration": 30,
            "priority": 5,
            "category": "walk",
            "frequency": "daily"
        },
        {
            "name": "Evening walk",
            "pet": pets[0],
            "duration": 20,
            "priority": 4,
            "category": "walk",
            "frequency": "daily"
        },
        {
            "name": "Dog feeding",
            "pet": pets[0],
            "duration": 10,
            "priority": 5,
            "category": "feeding",
            "frequency": "daily"
        },
        {
            "name": "Dog play/exercise",
            "pet": pets[0],
            "duration": 15,
            "priority": 4,
            "category": "play",
            "frequency": "daily"
        },
        # Cat tasks
        {
            "name": "Cat feeding",
            "pet": pets[1],
            "duration": 5,
            "priority": 5,
            "category": "feeding",
            "frequency": "daily"
        },
        {
            "name": "Cat litter cleaning",
            "pet": pets[1],
            "duration": 10,
            "priority": 4,
            "category": "litter",
            "frequency": "daily"
        },
        {
            "name": "Cat playtime",
            "pet": pets[1],
            "duration": 15,
            "priority": 3,
            "category": "play",
            "frequency": "daily"
        },
        # Rabbit tasks
        {
            "name": "Rabbit feeding",
            "pet": pets[2],
            "duration": 10,
            "priority": 5,
            "category": "feeding",
            "frequency": "daily"
        },
        {
            "name": "Hutch cleaning",
            "pet": pets[2],
            "duration": 20,
            "priority": 4,
            "category": "cage_clean",
            "frequency": "daily"
        },
        {
            "name": "Rabbit exercise",
            "pet": pets[2],
            "duration": 15,
            "priority": 3,
            "category": "exercise",
            "frequency": "daily"
        },
    ]
    
    for task_info in tasks_config:
        pet = task_info.pop("pet")
        task = Task(
            name=task_info["name"],
            duration=task_info["duration"],
            priority=task_info["priority"],
            category=task_info["category"],
            pet_id=pet.name,
            frequency=task_info.get("frequency", "daily")
        )
        pet.add_task(task)
        print(f"✓ Created: {task.name} ({task.duration}min, Priority {task.priority}/5)")
    
    print(f"\nTotal tasks created: {len(owner.get_all_tasks())}")


def demo_generate_schedule(owner: Owner) -> Schedule:
    """Generate an optimized daily schedule."""
    print_section("4. Generating Daily Schedule")
    
    scheduler = Scheduler(owner)
    print(f"Tasks available for today: {len(scheduler.get_tasks_for_today())}")
    print(f"Owner available time: {owner.available_time_per_day} minutes")
    
    schedule = scheduler.generate_daily_plan(date.today())
    
    print(f"\n✓ Schedule generated with {len(schedule.tasks)} tasks")
    print(f"  Total duration: {schedule.get_total_duration()} minutes")
    print(f"  Feasible: {'Yes ✓' if schedule.is_feasible() else 'No ✗ (EXCEEDS TIME)'}")
    
    return schedule, scheduler


def demo_display_schedule(schedule: Schedule, scheduler: 'Scheduler') -> None:
    """Display the schedule with full reasoning."""
    print_section("5. Daily Schedule Report")
    
    explanation = scheduler.explain_reasoning(schedule)
    print(explanation)
    
    # Additional detailed view
    print("\nTask Details:")
    print("-" * 60)
    for i, task in enumerate(schedule.get_ordered_tasks(), 1):
        urgency = task.get_urgency_score()
        print(f"{i}. {task.name}")
        print(f"   Duration: {task.duration} min | Urgency Score: {urgency:.1f}")
        print(f"   Category: {task.category} | Frequency: {task.frequency}")
        print()


def main():
    """Run the complete PawPal+ demo."""
    print("\n" + "=" * 60)
    print("  PawPal+ Pet Care Planning System - Demo")
    print("=" * 60)
    print("This demo shows how PawPal+ organizes all your pet tasks")
    print("into a realistic daily schedule based on priority and time.")
    
    # Run demo steps
    owner = demo_create_owner()
    pets = demo_add_pets(owner)
    demo_create_tasks(owner, pets)
    schedule, scheduler = demo_generate_schedule(owner)
    demo_display_schedule(schedule, scheduler)
    
    print_section("Demo Complete")
    print("✓ Successfully demonstrated PawPal+ scheduling system")
    print("  - Owner and pets created")
    print("  - Tasks added for all pets")
    print("  - Daily schedule optimized by urgency")
    print("  - All tasks fit within available time")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
