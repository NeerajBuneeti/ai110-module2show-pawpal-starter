# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

### Core User Actions
1. Add/manage a pet - Enter pet info (name, type, age, preferences)
2. Add/edit pet care tasks - Create tasks with duration and priority
3. Generate daily schedule - Produce optimized daily plan respecting constraints

### UML Classes (5-class architecture)

1. **Owner** - Pet owner with time constraints and preferences
   - Attributes: name, available_time_per_day, preferences, pets list
   - Methods: get_available_time(), set_preferences(), get_info(), add_pet(), get_all_tasks()
   - Responsibility: Define constraints, manage pets, aggregate tasks

2. **Pet** - Pet with care needs and task list
   - Attributes: name, pet_type, age, preferences, dietary_needs, tasks list
   - Methods: get_info(), update_preferences(), get_care_needs(), add_task()
   - Responsibility: Represent pet characteristics and needs

3. **Task** - Care activity with priority and duration
   - Attributes: name, duration, priority (1-5), category, pet_id, frequency, completed status
   - Methods: get_duration(), matches_pet_needs(), get_urgency_score(), is_required_today(), mark_complete()
   - Responsibility: Define individual tasks with priority and state tracking

4. **Schedule** - Daily plan with ordered tasks
   - Attributes: date, owner reference, tasks list, task_order, total_time
   - Methods: add_task(), remove_task(), get_total_duration(), is_feasible(), get_ordered_tasks()
   - Responsibility: Build, validate, and order daily schedules

5. **Scheduler** - Orchestrates scheduling algorithm
   - Methods: get_tasks_for_today(), generate_daily_plan(), arrange_tasks(), explain_reasoning(), validate_schedule()
   - Responsibility: Core scheduling algorithm balancing priorities and constraints

**b. Design changes**

(To be filled in during implementation phase)

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
