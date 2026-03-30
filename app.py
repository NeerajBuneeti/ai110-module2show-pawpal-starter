import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler
from datetime import date
import json
import os

# Helper function for priority indicators
def get_priority_display(priority: int) -> str:
    """Return emoji and label for priority level."""
    if priority >= 4:
        return "🔴 High"
    elif priority >= 3:
        return "🟡 Medium"
    else:
        return "🟢 Low"

def save_owner_data(owner: Owner, filename: str = "data.json") -> None:
    """Save owner data to JSON file."""
    with open(filename, "w") as f:
        json.dump(owner.to_dict(), f, indent=2)

def load_owner_data(filename: str = "data.json") -> Owner | None:
    """Load owner data from JSON file if it exists."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return Owner.from_dict(data)
    return None

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

# Initialize session state with Owner instance
if "owner" not in st.session_state:
    # Try to load saved data, fall back to default
    loaded_owner = load_owner_data()
    if loaded_owner:
        st.session_state.owner = loaded_owner
        st.info("✓ Loaded saved pets and tasks!")
    else:
        st.session_state.owner = Owner(
            name="Jordan",
            available_time_per_day=120,
            preferences={}
        )

owner = st.session_state.owner

st.markdown(
    """
Welcome to **PawPal+** — your AI-powered pet care planning assistant.

This app helps you organize all your pet care tasks into a realistic daily schedule
based on your available time and task priorities.
"""
)

# Display current owner info
with st.expander("Owner Settings", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Owner name", value=owner.name)
        if new_name != owner.name:
            owner.name = new_name
    with col2:
        new_time = st.number_input(
            "Available time per day (minutes)",
            min_value=30,
            max_value=480,
            value=owner.available_time_per_day,
            step=15
        )
        if new_time != owner.available_time_per_day:
            owner.available_time_per_day = new_time
    
    st.success(f"✓ {owner.get_info()}")

st.divider()

# ============================================================================
# SECTION 1: PETS MANAGEMENT
# ============================================================================

st.subheader("🐶 My Pets")

col1, col2 = st.columns([2, 1])

with col1:
    st.caption(f"You currently have {len(owner.pets)} pet(s)")
    
    if owner.pets:
        for i, pet in enumerate(owner.pets):
            with st.container(border=True):
                col_info, col_tasks = st.columns([2, 1])
                with col_info:
                    st.write(f"**{pet.name}** • {pet.pet_type.title()} • {pet.age} years old")
                    st.caption(f"Tasks: {len(pet.tasks)} | Needs: {', '.join(pet.get_care_needs())}")
                with col_tasks:
                    if st.button("Remove", key=f"remove_pet_{i}"):
                        owner.pets.pop(i)
                        save_owner_data(owner)
                        st.rerun()
    else:
        st.info("No pets yet. Add one below!")

with col2:
    st.caption("Add a new pet")
    pet_name = st.text_input("Pet name", value="Max", key="pet_name_input")
    pet_type = st.selectbox("Type", ["dog", "cat", "rabbit", "bird", "hamster"], key="pet_type_select")
    pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=1, step=1, key="pet_age_input")
    
    if st.button("➕ Add Pet", key="add_pet_button"):
        new_pet = Pet(name=pet_name, pet_type=pet_type, age=pet_age)
        owner.add_pet(new_pet)
        save_owner_data(owner)
        st.success(f"✓ Added {pet_name}!")
        st.rerun()

st.divider()

# ============================================================================
# SECTION 2: TASKS MANAGEMENT
# ============================================================================

st.subheader("📋 Pet Care Tasks")

if owner.pets:
    selected_pet_idx = st.selectbox(
        "Select pet to add task for",
        range(len(owner.pets)),
        format_func=lambda i: owner.pets[i].name,
        key="pet_select"
    )
    selected_pet = owner.pets[selected_pet_idx]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        task_name = st.text_input("Task name", value="Morning walk", key="task_name")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30, key="task_duration")
    with col3:
        priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=4, key="task_priority")
    with col4:
        category = st.selectbox(
            "Category",
            ["walk", "feeding", "grooming", "play", "medication", "enrichment", "litter", "exercise", "cage_clean", "water"],
            index=0,
            key="task_category"
        )
    
    col1, col2 = st.columns(2)
    with col1:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"], index=0, key="task_frequency")
    with col2:
        description = st.text_input("Description (optional)", value="", key="task_description")
    
    if st.button("➕ Add Task", key="add_task_button"):
        new_task = Task(
            name=task_name,
            duration=int(duration),
            priority=int(priority),
            category=category,
            pet_id=selected_pet.name,
            frequency=frequency,
            description=description
        )
        selected_pet.add_task(new_task)
        save_owner_data(owner)
        st.success(f"✓ Added '{task_name}' for {selected_pet.name}!")
        st.rerun()
    
    st.divider()
    
    # Display all tasks
    st.caption("All tasks across all pets")
    all_tasks = owner.get_all_tasks()
    
    if all_tasks:
        # Smart task view with sorting and filtering options
        col1, col2, col3 = st.columns(3)
        
        view_mode = "default"
        with col1:
            sort_by = st.radio("Sort by", ["Urgency Score", "Time", "Default"], key="sort_mode")
            if sort_by == "Urgency Score":
                view_mode = "urgency"
            elif sort_by == "Time":
                view_mode = "time"
        
        with col2:
            pet_filter = st.selectbox("Filter by pet", ["All Pets"] + [p.name for p in owner.pets], key="pet_filter")
        
        with col3:
            status_filter = st.radio("Show", ["All", "Incomplete Only", "Completed Only"], key="status_filter")
        
        # Apply filters
        filtered_tasks = all_tasks
        
        if pet_filter != "All Pets":
            scheduler = Scheduler(owner)
            filtered_tasks = scheduler.filter_by_pet(pet_filter, filtered_tasks)
        
        if status_filter == "Incomplete Only":
            scheduler = Scheduler(owner)
            filtered_tasks = scheduler.filter_by_completion_status(False, filtered_tasks)
        elif status_filter == "Completed Only":
            scheduler = Scheduler(owner)
            filtered_tasks = scheduler.filter_by_completion_status(True, filtered_tasks)
        
        # Apply sorting
        if view_mode == "urgency":
            scheduler = Scheduler(owner)
            filtered_tasks = scheduler.sort_by_urgency(filtered_tasks)
        elif view_mode == "time":
            scheduler = Scheduler(owner)
            filtered_tasks = scheduler.sort_by_time(filtered_tasks)
        
        # Display tasks
        task_display = []
        for task in filtered_tasks:
            task_display.append({
                "Pet": task.pet_id,
                "Task": task.name,
                "Duration": f"{task.duration} min",
                "Priority": get_priority_display(task.priority),
                "Urgency Score": f"{task.get_urgency_score():.1f}",
                "Category": task.category,
                "Frequency": task.frequency,
                "Status": "✓ Done" if task.completed else "○ Pending"
            })
        
        st.dataframe(task_display, width='stretch', use_container_width=True)
        st.caption(f"Showing {len(task_display)} of {len(all_tasks)} tasks")
    else:
        st.info("No tasks yet. Add one above!")

else:
    st.warning("⚠️ Add a pet first before creating tasks.")

st.divider()

# ============================================================================
# SECTION 3: SCHEDULE GENERATION
# ============================================================================

st.subheader("📅 Daily Schedule Generator")

col1, col2 = st.columns([3, 1])

with col1:
    st.caption("Generate an optimized daily schedule based on your available time and task priorities.")

with col2:
    schedule_date = st.date_input("Schedule for", value=date.today(), key="schedule_date")

if st.button("🚀 Generate Schedule", key="generate_schedule_button", width='stretch'):
    if not owner.pets:
        st.error("❌ Please add at least one pet and a task before generating a schedule.")
    elif not owner.get_all_tasks():
        st.error("❌ Please add at least one task before generating a schedule.")
    else:
        # Generate schedule using Scheduler
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_daily_plan(schedule_date)
        
        st.session_state.current_schedule = schedule
        st.session_state.current_scheduler = scheduler
        st.success("✓ Schedule generated!")

# Display generated schedule
if "current_schedule" in st.session_state:
    schedule = st.session_state.current_schedule
    scheduler = st.session_state.current_scheduler
    
    st.divider()
    st.subheader(f"📖 Your Schedule for {schedule.date}")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tasks Scheduled", len(schedule.tasks))
    with col2:
        st.metric("Total Time", f"{schedule.get_total_duration()} min")
    with col3:
        st.metric("Available Time", f"{owner.available_time_per_day} min")
    with col4:
        feasible = schedule.is_feasible()
        st.metric(
            "Feasible",
            "✓ Yes" if feasible else "✗ No",
            delta="Within time" if feasible else "Exceeds time"
        )
    
    st.divider()
    
    # Schedule explanation and reasoning
    explanation = scheduler.explain_reasoning(schedule)
    st.text(explanation)
    
    # Conflict detection
    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        st.divider()
        with st.container(border=True):
            st.warning("⚠️ **Task Conflicts Detected**")
            for conflict_msg in conflicts:
                st.write(f"• {conflict_msg}")
    
    st.divider()
    
    # Detailed task breakdown with time slots
    st.subheader("Task Breakdown with Time Slots")
    
    if schedule.tasks:
        # Sort by time for display
        time_sorted = scheduler.sort_by_time(schedule.get_ordered_tasks())
        
        for i, task in enumerate(time_sorted, 1):
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    time_display = f"({task.scheduled_time})" if task.scheduled_time else "(No time)"
                    st.write(f"**{i}. {task.name}** {time_display}")
                    st.caption(f"Pet: {task.pet_id} • {task.description if task.description else task.category}")
                
                with col2:
                    st.metric("Duration", f"{task.duration}m")
                
                with col3:
                    st.metric("Priority Level", get_priority_display(task.priority))
                
                with col4:
                    urgency = task.get_urgency_score()
                    st.metric("Urgency", f"{urgency:.1f}")
                
                st.caption(f"Frequency: {task.frequency} • Category: {task.category}")
    else:
        st.info("No tasks fit within your available time.")
    
    # Option to clear schedule
    if st.button("Clear schedule", key="clear_schedule_button"):
        del st.session_state.current_schedule
        del st.session_state.current_scheduler
        st.rerun()

