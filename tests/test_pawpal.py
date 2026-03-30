"""
Comprehensive test suite for PawPal+ pet care scheduling system.

Tests cover all 5 main classes: Owner, Pet, Task, Schedule, and Scheduler.
Uses pytest fixtures for test setup and isolation.
"""

import pytest
from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler


# ============================================================================
# FIXTURES - Setup for tests
# ============================================================================

@pytest.fixture
def sample_owner():
    """Create a sample owner for testing."""
    return Owner(
        name="Alice",
        available_time_per_day=120,  # 2 hours
        preferences={"early_morning": True}
    )


@pytest.fixture
def sample_dog():
    """Create a sample dog pet."""
    return Pet(
        name="Max",
        pet_type="dog",
        age=3,
        dietary_needs="High protein"
    )


@pytest.fixture
def sample_cat():
    """Create a sample cat pet."""
    return Pet(
        name="Whiskers",
        pet_type="cat",
        age=5,
        dietary_needs="Fish-based"
    )


@pytest.fixture
def sample_task():
    """Create a sample task."""
    return Task(
        name="Morning walk",
        duration=30,
        priority=5,
        category="walk",
        pet_id="Max",
        frequency="daily"
    )


@pytest.fixture
def setup_with_all_pets(sample_owner, sample_dog, sample_cat):
    """Setup owner with multiple pets."""
    rabbit = Pet(name="Hoppy", pet_type="rabbit", age=2)
    sample_owner.add_pet(sample_dog)
    sample_owner.add_pet(sample_cat)
    sample_owner.add_pet(rabbit)
    return sample_owner, sample_dog, sample_cat, rabbit


# ============================================================================
# TESTS FOR TASK CLASS
# ============================================================================

class TestTask:
    """Tests for Task class."""
    
    def test_task_creation(self, sample_task):
        """Test that task is created with correct attributes."""
        assert sample_task.name == "Morning walk"
        assert sample_task.duration == 30
        assert sample_task.priority == 5
        assert sample_task.category == "walk"
        assert sample_task.completed is False
    
    def test_task_get_duration(self, sample_task):
        """Test get_duration returns correct value."""
        assert sample_task.get_duration() == 30
    
    def test_task_completion_tracking(self, sample_task):
        """Test task completion state changes."""
        assert sample_task.completed is False
        sample_task.mark_complete()
        assert sample_task.completed is True
        sample_task.mark_incomplete()
        assert sample_task.completed is False
    
    def test_task_urgency_score_daily(self, sample_task):
        """Test urgency score for daily tasks."""
        sample_task.frequency = "daily"
        # Priority 5 * daily multiplier 1.5 = 7.5
        assert sample_task.get_urgency_score() == 7.5
    
    def test_task_urgency_score_weekly(self):
        """Test urgency score for weekly tasks."""
        task = Task(
            name="Grooming",
            duration=45,
            priority=3,
            category="grooming",
            pet_id="Max",
            frequency="weekly"
        )
        # Priority 3 * weekly multiplier 1.0 = 3.0
        assert task.get_urgency_score() == 3.0
    
    def test_task_is_required_today_daily(self, sample_task):
        """Test that daily tasks are required today."""
        sample_task.frequency = "daily"
        assert sample_task.is_required_today() is True
    
    def test_task_is_required_today_weekly(self, sample_task):
        """Test that weekly tasks are not required today."""
        sample_task.frequency = "weekly"
        assert sample_task.is_required_today() is False
    
    def test_task_is_required_today_as_needed(self, sample_task):
        """Test that 'as needed' tasks are required today."""
        sample_task.frequency = "as needed"
        assert sample_task.is_required_today() is True
    
    def test_matches_pet_needs_dog(self, sample_dog):
        """Test task matches dog's care needs."""
        walk_task = Task(
            name="Walk",
            duration=20,
            priority=5,
            category="walk",
            pet_id="Max",
            frequency="daily"
        )
        assert walk_task.matches_pet_needs(sample_dog) is True
    
    def test_matches_pet_needs_cat(self, sample_cat):
        """Test task matches cat's care needs."""
        litter_task = Task(
            name="Litter",
            duration=10,
            priority=4,
            category="litter",
            pet_id="Whiskers",
            frequency="daily"
        )
        assert litter_task.matches_pet_needs(sample_cat) is True
    
    def test_does_not_match_pet_needs(self, sample_dog):
        """Test task doesn't match unrelated pet needs."""
        litter_task = Task(
            name="Litter",
            duration=10,
            priority=4,
            category="litter",
            pet_id="Whiskers",
            frequency="daily"
        )
        assert litter_task.matches_pet_needs(sample_dog) is False


# ============================================================================
# TESTS FOR PET CLASS
# ============================================================================

class TestPet:
    """Tests for Pet class."""
    
    def test_pet_creation(self, sample_dog):
        """Test pet creation with attributes."""
        assert sample_dog.name == "Max"
        assert sample_dog.pet_type == "dog"
        assert sample_dog.age == 3
        assert len(sample_dog.tasks) == 0
    
    def test_pet_get_info(self, sample_dog):
        """Test pet info string."""
        info = sample_dog.get_info()
        assert "Max" in info
        assert "dog" in info
        assert "3 years" in info
    
    def test_pet_get_care_needs_dog(self, sample_dog):
        """Test dog care needs."""
        needs = sample_dog.get_care_needs()
        assert "walk" in needs
        assert "feeding" in needs
        assert "play" in needs
        assert "grooming" in needs
    
    def test_pet_get_care_needs_cat(self, sample_cat):
        """Test cat care needs."""
        needs = sample_cat.get_care_needs()
        assert "feeding" in needs
        assert "litter" in needs
        assert "play" in needs
    
    def test_pet_get_care_needs_rabbit(self):
        """Test rabbit care needs."""
        rabbit = Pet(name="Hoppy", pet_type="rabbit", age=2)
        needs = rabbit.get_care_needs()
        assert "feeding" in needs
        assert "exercise" in needs
        assert "cage_clean" in needs
    
    def test_pet_add_task(self, sample_dog, sample_task):
        """Test adding tasks to pet."""
        assert len(sample_dog.tasks) == 0
        sample_dog.add_task(sample_task)
        assert len(sample_dog.tasks) == 1
        assert sample_dog.tasks[0] == sample_task
    
    def test_pet_multiple_tasks(self, sample_dog):
        """Test adding multiple tasks to pet."""
        task1 = Task(
            name="Walk", duration=30, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        )
        task2 = Task(
            name="Feeding", duration=10, priority=5,
            category="feeding", pet_id="Max", frequency="daily"
        )
        sample_dog.add_task(task1)
        sample_dog.add_task(task2)
        assert len(sample_dog.tasks) == 2
    
    def test_pet_update_preferences(self, sample_dog):
        """Test updating pet preferences."""
        assert "breed" not in sample_dog.preferences
        sample_dog.update_preferences({"breed": "Golden Retriever"})
        assert sample_dog.preferences["breed"] == "Golden Retriever"


# ============================================================================
# TESTS FOR OWNER CLASS
# ============================================================================

class TestOwner:
    """Tests for Owner class."""
    
    def test_owner_creation(self, sample_owner):
        """Test owner creation."""
        assert sample_owner.name == "Alice"
        assert sample_owner.available_time_per_day == 120
        assert len(sample_owner.pets) == 0
    
    def test_owner_get_available_time(self, sample_owner):
        """Test available time getter."""
        assert sample_owner.get_available_time() == 120
    
    def test_owner_get_info(self, sample_owner):
        """Test owner info string."""
        info = sample_owner.get_info()
        assert "Alice" in info
        assert "120" in info
    
    def test_owner_add_pet(self, sample_owner, sample_dog):
        """Test adding pet to owner."""
        assert len(sample_owner.pets) == 0
        sample_owner.add_pet(sample_dog)
        assert len(sample_owner.pets) == 1
        assert sample_owner.pets[0] == sample_dog
    
    def test_owner_add_multiple_pets(self, setup_with_all_pets):
        """Test owner with multiple pets."""
        owner = setup_with_all_pets[0]
        assert len(owner.pets) == 3
        assert owner.pets[0].name == "Max"
        assert owner.pets[1].name == "Whiskers"
    
    def test_owner_get_all_tasks(self, setup_with_all_pets):
        """Test retrieving all tasks from all pets."""
        owner, dog, cat, rabbit = setup_with_all_pets
        
        # Add tasks to pets
        dog.add_task(Task(
            name="Walk", duration=30, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        ))
        cat.add_task(Task(
            name="Feeding", duration=5, priority=5,
            category="feeding", pet_id="Whiskers", frequency="daily"
        ))
        
        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 2
    
    def test_owner_set_preferences(self, sample_owner):
        """Test setting owner preferences."""
        new_prefs = {"early_morning": False, "flexible_schedule": True}
        sample_owner.set_preferences(new_prefs)
        assert sample_owner.preferences["early_morning"] is False
        assert sample_owner.preferences["flexible_schedule"] is True


# ============================================================================
# TESTS FOR SCHEDULE CLASS
# ============================================================================

class TestSchedule:
    """Tests for Schedule class."""
    
    def test_schedule_creation(self, sample_owner, sample_task):
        """Test schedule creation."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        assert schedule.date == date.today()
        assert schedule.owner == sample_owner
        assert len(schedule.tasks) == 0
    
    def test_schedule_add_task(self, sample_owner, sample_task):
        """Test adding tasks to schedule."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        schedule.add_task(sample_task)
        assert len(schedule.tasks) == 1
        assert schedule.total_time == 30
    
    def test_schedule_add_multiple_tasks(self, sample_owner):
        """Test adding multiple tasks to schedule."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        
        task1 = Task(
            name="Walk", duration=30, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        )
        task2 = Task(
            name="Feeding", duration=10, priority=5,
            category="feeding", pet_id="Max", frequency="daily"
        )
        
        schedule.add_task(task1)
        schedule.add_task(task2)
        
        assert len(schedule.tasks) == 2
        assert schedule.total_time == 40
    
    def test_schedule_remove_task(self, sample_owner, sample_task):
        """Test removing task from schedule."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        schedule.add_task(sample_task)
        assert len(schedule.tasks) == 1
        
        schedule.remove_task(sample_task)
        assert len(schedule.tasks) == 0
        assert schedule.total_time == 0
    
    def test_schedule_get_total_duration(self, sample_owner):
        """Test total duration calculation."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        
        for duration in [30, 20, 15]:
            task = Task(
                name=f"Task {duration}",
                duration=duration,
                priority=3,
                category="walk",
                pet_id="Max",
                frequency="daily"
            )
            schedule.add_task(task)
        
        assert schedule.get_total_duration() == 65
    
    def test_schedule_is_feasible_true(self, sample_owner):
        """Test schedule feasibility when within time."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        
        task = Task(
            name="Quick task",
            duration=60,
            priority=3,
            category="walk",
            pet_id="Max",
            frequency="daily"
        )
        schedule.add_task(task)
        
        assert schedule.is_feasible() is True
    
    def test_schedule_is_feasible_false(self, sample_owner):
        """Test schedule feasibility when exceeds time."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        
        # Owner has 120 minutes available
        task = Task(
            name="Long task",
            duration=130,
            priority=3,
            category="walk",
            pet_id="Max",
            frequency="daily"
        )
        schedule.add_task(task)
        
        assert schedule.is_feasible() is False
    
    def test_schedule_get_ordered_tasks(self, sample_owner):
        """Test getting tasks in order."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        
        tasks = [
            Task(name="Task 1", duration=20, priority=1,
                 category="walk", pet_id="Max", frequency="daily"),
            Task(name="Task 2", duration=20, priority=2,
                 category="walk", pet_id="Max", frequency="daily"),
            Task(name="Task 3", duration=20, priority=3,
                 category="walk", pet_id="Max", frequency="daily"),
        ]
        
        for task in tasks:
            schedule.add_task(task)
        
        ordered = schedule.get_ordered_tasks()
        assert len(ordered) == 3
        assert ordered[0].name == "Task 1"


# ============================================================================
# TESTS FOR SCHEDULER CLASS
# ============================================================================

class TestScheduler:
    """Tests for Scheduler class."""
    
    def test_scheduler_creation(self, setup_with_all_pets):
        """Test scheduler creation."""
        owner = setup_with_all_pets[0]
        scheduler = Scheduler(owner)
        assert scheduler.owner == owner
        assert len(scheduler.pets) == 3
    
    def test_scheduler_get_tasks_for_today_daily(self, setup_with_all_pets):
        """Test filtering daily tasks."""
        owner, dog, _, _ = setup_with_all_pets
        
        daily_task = Task(
            name="Daily walk", duration=30, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        )
        weekly_task = Task(
            name="Grooming", duration=45, priority=3,
            category="grooming", pet_id="Max", frequency="weekly"
        )
        
        dog.add_task(daily_task)
        dog.add_task(weekly_task)
        
        scheduler = Scheduler(owner)
        today_tasks = scheduler.get_tasks_for_today()
        
        assert len(today_tasks) == 1
        assert today_tasks[0].frequency == "daily"
    
    def test_scheduler_get_tasks_for_today_empty(self, setup_with_all_pets):
        """Test handling no tasks for today."""
        owner = setup_with_all_pets[0]
        scheduler = Scheduler(owner)
        
        today_tasks = scheduler.get_tasks_for_today()
        assert len(today_tasks) == 0
    
    def test_scheduler_arrange_tasks_by_urgency(self, setup_with_all_pets):
        """Test tasks are sorted by urgency score."""
        owner, dog, _, _ = setup_with_all_pets
        
        low_priority = Task(
            name="Low", duration=10, priority=1,
            category="walk", pet_id="Max", frequency="daily"
        )
        high_priority = Task(
            name="High", duration=10, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        )
        
        dog.add_task(low_priority)
        dog.add_task(high_priority)
        
        scheduler = Scheduler(owner)
        tasks = scheduler.get_tasks_for_today()
        arranged = scheduler.arrange_tasks(120, tasks)
        
        assert arranged[0].priority == 5
        assert arranged[1].priority == 1
    
    def test_scheduler_arrange_tasks_within_time(self, setup_with_all_pets):
        """Test tasks fit within available time."""
        owner, dog, _, _ = setup_with_all_pets
        
        # Add tasks that total 100 minutes (within 120 available)
        for i in range(5):
            task = Task(
                name=f"Task {i}", duration=20, priority=5-i,
                category="walk", pet_id="Max", frequency="daily"
            )
            dog.add_task(task)
        
        scheduler = Scheduler(owner)
        arranged = scheduler.arrange_tasks(120)
        
        total = sum(t.duration for t in arranged)
        assert total <= 120
    
    def test_scheduler_arrange_tasks_respects_time_limit(self, setup_with_all_pets):
        """Test tasks are dropped when exceeding time limit."""
        owner, dog, _, _ = setup_with_all_pets
        owner.available_time_per_day = 40
        
        # Add 4 tasks of 20 minutes each
        for i in range(4):
            task = Task(
                name=f"Task {i}", duration=20, priority=5-i,
                category="walk", pet_id="Max", frequency="daily"
            )
            dog.add_task(task)
        
        scheduler = Scheduler(owner)
        arranged = scheduler.arrange_tasks(40)
        
        # Should only fit 2 tasks
        assert len(arranged) == 2
        assert arranged[0].priority == 5  # Highest priority first
    
    def test_scheduler_generate_daily_plan(self, setup_with_all_pets):
        """Test generating a complete daily plan."""
        owner, dog, cat, _ = setup_with_all_pets
        
        dog.add_task(Task(
            name="Walk", duration=30, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        ))
        cat.add_task(Task(
            name="Feeding", duration=5, priority=5,
            category="feeding", pet_id="Whiskers", frequency="daily"
        ))
        
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_daily_plan()
        
        assert schedule.date == date.today()
        assert len(schedule.tasks) == 2
        assert schedule.is_feasible()
    
    def test_scheduler_explain_reasoning(self, setup_with_all_pets):
        """Test schedule explanation generation."""
        owner, dog, _, _ = setup_with_all_pets
        
        dog.add_task(Task(
            name="Walk", duration=30, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        ))
        
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_daily_plan()
        explanation = scheduler.explain_reasoning(schedule)
        
        assert "Daily Schedule" in explanation
        assert "Walk" in explanation
        assert "30 min" in explanation
    
    def test_scheduler_validate_schedule_true(self, sample_owner):
        """Test schedule validation when feasible."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        schedule.add_task(Task(
            name="Walk", duration=30, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        ))
        
        scheduler = Scheduler(sample_owner)
        assert scheduler.validate_schedule(schedule) is True
    
    def test_scheduler_validate_schedule_false(self, sample_owner):
        """Test schedule validation when not feasible."""
        schedule = Schedule(date=date.today(), owner=sample_owner)
        schedule.add_task(Task(
            name="Long task", duration=150, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        ))
        
        scheduler = Scheduler(sample_owner)
        assert scheduler.validate_schedule(schedule) is False


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_full_workflow(self, sample_owner, sample_dog, sample_cat):
        """Test complete PawPal+ workflow."""
        # Setup
        sample_owner.add_pet(sample_dog)
        sample_owner.add_pet(sample_cat)
        
        # Add tasks
        sample_dog.add_task(Task(
            name="Walk", duration=30, priority=5,
            category="walk", pet_id="Max", frequency="daily"
        ))
        sample_cat.add_task(Task(
            name="Feeding", duration=5, priority=5,
            category="feeding", pet_id="Whiskers", frequency="daily"
        ))
        
        # Schedule
        scheduler = Scheduler(sample_owner)
        schedule = scheduler.generate_daily_plan()
        
        # Verify
        assert len(schedule.tasks) == 2
        assert schedule.is_feasible()
        assert scheduler.validate_schedule(schedule)
