"""
PawPal+ System Design - Core Logic Layer

This module contains the main classes for the PawPal+ pet care planning system:
- Owner: Pet owner profile and constraints
- Pet: Pet information and needs
- Task: Pet care tasks with priority and duration
- Schedule: A planned schedule for a specific day
- Scheduler: Orchestrates task scheduling
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import date, timedelta


@dataclass
class Owner:
    """Represents a pet owner with time constraints and preferences."""
    
    name: str
    available_time_per_day: int  # minutes
    preferences: Dict[str, any] = field(default_factory=dict)
    pets: List['Pet'] = field(default_factory=list)
    
    def get_available_time(self) -> int:
        """Returns available time in minutes."""
        return self.available_time_per_day
    
    def set_preferences(self, preferences: Dict[str, any]) -> None:
        """Update owner preferences."""
        self.preferences.update(preferences)
    
    def get_info(self) -> str:
        """Return owner information as string."""
        return f"Owner: {self.name} | Available time: {self.available_time_per_day} min/day | Pets: {len(self.pets)}"
    
    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)
    
    def get_all_tasks(self) -> List['Task']:
        """Get all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Pet:
    """Represents a pet with care needs and preferences."""
    
    name: str
    pet_type: str  # e.g., "dog", "cat", "rabbit"
    age: int  # in years
    preferences: Dict[str, any] = field(default_factory=dict)
    dietary_needs: str = ""
    tasks: List['Task'] = field(default_factory=list)
    
    def get_info(self) -> str:
        """Return pet information as string."""
        return f"{self.name} ({self.pet_type}, {self.age} years old) | Tasks: {len(self.tasks)}"
    
    def update_preferences(self, preferences: Dict[str, any]) -> None:
        """Update pet preferences."""
        self.preferences.update(preferences)
    
    def get_care_needs(self) -> List[str]:
        """Return list of primary care needs based on pet type."""
        care_needs_map = {
            "dog": ["walk", "feeding", "play", "grooming"],
            "cat": ["feeding", "litter", "play", "grooming"],
            "rabbit": ["feeding", "exercise", "cage_clean", "grooming"],
            "bird": ["feeding", "water", "cage_clean", "social_time"],
            "hamster": ["feeding", "water", "cage_clean", "exercise"],
        }
        return care_needs_map.get(self.pet_type.lower(), ["feeding", "water"])
    
    def add_task(self, task: 'Task') -> None:
        """Add a task to this pet."""
        self.tasks.append(task)


@dataclass
class Task:
    """Represents a pet care task with priority and duration."""
    
    name: str
    duration: int  # minutes
    priority: int  # 1-5, where 5 is highest
    category: str  # e.g., "walk", "feeding", "medication", "enrichment", "grooming"
    pet_id: str  # ID of the pet this task applies to
    frequency: str = "daily"  # e.g., "daily", "weekly", "as needed"
    description: str = ""
    completed: bool = False  # Track if task is completed
    scheduled_time: Optional[str] = None  # HH:MM format time slot
    due_date: Optional[date] = None  # Date task is due
    
    def get_duration(self) -> int:
        """Return task duration in minutes."""
        return self.duration
    
    def matches_pet_needs(self, pet: Pet) -> bool:
        """Check if this task is appropriate for a given pet."""
        pet_care_needs = pet.get_care_needs()
        return self.category in pet_care_needs
    
    def get_urgency_score(self) -> float:
        """Calculate urgency based on priority and frequency."""
        # Higher priority = higher urgency, daily tasks > weekly tasks
        frequency_multiplier = 1.0
        if self.frequency == "daily":
            frequency_multiplier = 1.5
        elif self.frequency == "weekly":
            frequency_multiplier = 1.0
        
        return self.priority * frequency_multiplier
    
    def is_required_today(self) -> bool:
        """Determine if task should be done today based on frequency."""
        # For now, "daily" and "as needed" are considered required
        return self.frequency in ["daily", "as needed"]
    
    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False
    
    def generate_next_occurrence(self) -> Optional['Task']:
        """Create next occurrence for recurring tasks (daily/weekly)."""
        if self.frequency == "as needed":
            return None  # No automatic recurrence for "as needed"
        
        # Calculate next due date
        if self.due_date is None:
            next_due = date.today()
        else:
            if self.frequency == "daily":
                next_due = self.due_date + timedelta(days=1)
            elif self.frequency == "weekly":
                next_due = self.due_date + timedelta(weeks=1)
            else:
                return None
        
        # Create new task instance with same properties
        return Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            pet_id=self.pet_id,
            frequency=self.frequency,
            description=self.description,
            completed=False,
            scheduled_time=None,
            due_date=next_due
        )


@dataclass
class Schedule:
    """Represents a planned schedule for a single day."""
    
    date: date
    owner: Owner  # Reference to owner for constraint validation
    tasks: List[Task] = field(default_factory=list)
    task_order: List[int] = field(default_factory=list)  # Indices representing order of tasks
    total_time: int = 0  # minutes
    
    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)
        self.task_order.append(len(self.tasks) - 1)
        self.total_time += task.duration
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule."""
        if task in self.tasks:
            idx = self.tasks.index(task)
            self.tasks.remove(task)
            self.task_order.remove(idx)
            self.total_time -= task.duration
    
    def get_total_duration(self) -> int:
        """Calculate total time for all scheduled tasks."""
        return sum(task.duration for task in self.tasks)
    
    def is_feasible(self) -> bool:
        """Check if schedule fits within owner's available time."""
        return self.get_total_duration() <= self.owner.available_time_per_day
    
    def get_ordered_tasks(self) -> List[Task]:
        """Return tasks in planned order."""
        return [self.tasks[i] for i in self.task_order if i < len(self.tasks)]


class Scheduler:
    """Orchestrates daily task scheduling based on constraints and priorities."""
    
    def __init__(self, owner: Owner, pets: List[Pet] = None, tasks: List[Task] = None):
        """Initialize scheduler with owner, pets, and available tasks."""
        self.owner = owner
        self.pets = pets or owner.pets
        self.tasks = tasks or owner.get_all_tasks()
    
    def get_tasks_for_today(self) -> List[Task]:
        """Filter tasks applicable for today based on frequency."""
        return [task for task in self.tasks if task.is_required_today()]
    
    def sort_by_urgency(self, tasks: List[Task] = None) -> List[Task]:
        """Sort tasks by urgency score in descending order (highest urgency first)."""
        if tasks is None:
            tasks = self.get_tasks_for_today()
        return sorted(tasks, key=lambda t: t.get_urgency_score(), reverse=True)
    
    def sort_by_time(self, tasks: List[Task] = None) -> List[Task]:
        """Sort tasks by scheduled time in HH:MM format."""
        if tasks is None:
            tasks = [t for t in self.get_tasks_for_today() if t.scheduled_time is not None]
        return sorted(
            tasks,
            key=lambda t: (t.scheduled_time or "23:59")  # Tasks without time go to end
        )
    
    def filter_by_pet(self, pet_name: str, tasks: List[Task] = None) -> List[Task]:
        """Filter tasks belonging to a specific pet."""
        if tasks is None:
            tasks = self.get_tasks_for_today()
        return [task for task in tasks if task.pet_id == pet_name]
    
    def filter_by_completion_status(self, completed: bool, tasks: List[Task] = None) -> List[Task]:
        """Filter tasks by completion status."""
        if tasks is None:
            tasks = self.get_tasks_for_today()
        return [task for task in tasks if task.completed == completed]
    
    def filter_by_priority(self, min_priority: int, tasks: List[Task] = None) -> List[Task]:
        """Filter tasks with priority >= min_priority."""
        if tasks is None:
            tasks = self.get_tasks_for_today()
        return [task for task in tasks if task.priority >= min_priority]
    
    def detect_conflicts(self, schedule: Schedule) -> List[str]:
        """Detect if tasks in schedule have time conflicts (exact time overlap)."""
        conflicts = []
        scheduled_tasks = schedule.get_ordered_tasks()
        
        # Check for tasks scheduled at the same time
        time_slots = {}
        for task in scheduled_tasks:
            if task.scheduled_time:
                if task.scheduled_time in time_slots:
                    conflicts.append(
                        f"⚠️  CONFLICT: '{task.name}' ({task.pet_id}) and "
                        f"'{time_slots[task.scheduled_time]['name']}' "
                        f"({time_slots[task.scheduled_time]['pet']}) "
                        f"both scheduled at {task.scheduled_time}"
                    )
                else:
                    time_slots[task.scheduled_time] = {"name": task.name, "pet": task.pet_id}
        
        return conflicts
    
    def generate_daily_plan(self, target_date: date = None) -> Schedule:
        """Generate optimized daily schedule respecting time and priority constraints."""
        if target_date is None:
            target_date = date.today()
        
        schedule = Schedule(date=target_date, owner=self.owner)
        today_tasks = self.get_tasks_for_today()
        arranged_tasks = self.arrange_tasks(self.owner.available_time_per_day, today_tasks)
        
        # Add tasks and assign time slots (simplified: evenly distribute across day)
        current_time_minutes = 480  # Start at 8:00 AM
        for task in arranged_tasks:
            schedule.add_task(task)
            # Assign task to time slot
            hours = current_time_minutes // 60
            minutes = current_time_minutes % 60
            task.scheduled_time = f"{hours:02d}:{minutes:02d}"
            current_time_minutes += task.duration
        
        return schedule
    
    def arrange_tasks(self, available_time: int, candidate_tasks: List[Task] = None) -> List[Task]:
        """Sort tasks by urgency and fit within time budget."""
        if candidate_tasks is None:
            candidate_tasks = self.get_tasks_for_today()
        
        # Sort by urgency score (descending) - higher urgency first
        sorted_tasks = sorted(candidate_tasks, key=lambda t: t.get_urgency_score(), reverse=True)
        
        scheduled_tasks = []
        time_used = 0
        
        for task in sorted_tasks:
            if time_used + task.duration <= available_time:
                scheduled_tasks.append(task)
                time_used += task.duration
        
        return scheduled_tasks
    
    def explain_reasoning(self, schedule: Schedule) -> str:
        """Generate human-readable explanation of schedule decisions."""
        explanation = f"Daily Schedule for {schedule.date}\n"
        explanation += "=" * 50 + "\n"
        
        if not schedule.tasks:
            explanation += "No tasks scheduled for today.\n"
            return explanation
        
        explanation += f"Total time allocated: {schedule.get_total_duration()} minutes "
        explanation += f"(Available: {self.owner.available_time_per_day} minutes)\n\n"
        
        for i, task in enumerate(schedule.get_ordered_tasks(), 1):
            time_slot = f" @ {task.scheduled_time}" if task.scheduled_time else ""
            explanation += f"{i}. {task.name}{time_slot} ({task.duration} min) - Priority: {task.priority}/5\n"
            explanation += f"   Category: {task.category} | Frequency: {task.frequency}\n"
        
        # Check for conflicts
        conflicts = self.detect_conflicts(schedule)
        if conflicts:
            explanation += "\n" + "⚠️  DETECTED CONFLICTS:\n"
            for conflict in conflicts:
                explanation += conflict + "\n"
        
        if not schedule.is_feasible():
            explanation += "\n⚠️  WARNING: Schedule exceeds available time!\n"
        
        return explanation
    
    def validate_schedule(self, schedule: Schedule) -> bool:
        """Check if schedule is feasible and meets time constraints."""
        return schedule.is_feasible()
