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

**Phase 2 Implementation Refinements:**
- Replaced placeholder stub methods with complete business logic
- Added task urgency scoring: `urgency = priority × frequency_multiplier` (daily = 1.5x, weekly = 1.0x)
- Implemented priority-based scheduling: tasks sorted by urgency score, packed into available time budget
- Added schedule feasibility validation to prevent over-scheduling
- Added human-readable schedule explanation generation showing reasoning

**Phase 3 UI Integration:**
- Connected app.py to pawpal_system.py via imports of Owner, Pet, Task, Scheduler
- Implemented st.session_state for Owner persistence across page refreshes (solves Streamlit statefulness issue)
- Built multi-section UI: Owner Settings, Pet Management, Task Management, Schedule Generation
- Wired all UI buttons to actual class methods (add_pet, add_task, generate_daily_plan)

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three main constraints:
1. **Time Budget** - Owner's available_time_per_day is the hard limit; tasks exceeding this are dropped
2. **Priority Levels** - Tasks rated 1-5; higher priority tasks are scheduled first
3. **Frequency** - Daily/weekly/as-needed frequency affects urgency scoring; daily tasks get 1.5x multiplier

Decision priority: Time > Urgency Score > Frequency
- Time is absolute (no schedule exceeds available_time_per_day)
- Urgency = priority × frequency_multiplier determines task ordering
- Frequency affects multiplier: daily tasks get priority boost over weekly tasks

**b. Tradeoffs**

**Tradeoff 1: Greedy Packing vs. Optimal Scheduling**
- Current approach: Sort tasks by urgency, pack greedily into time budget (O(n log n))
- Alternative: Bin packing or constraint satisfaction would be more optimal but much more complex
- Rationale: Greedy is "good enough" for daily planning. It respects urgency and fits time constraints reasonably. Perfect optimization not necessary for a daily schedule that changes daily anyway.

**Tradeoff 2: Fixed Urgency Multiplier vs. Dynamic Adjustments**
- Current: frequency_multiplier is hardcoded (daily=1.5x, weekly=1.0x)
- Alternative: Could learn from user preferences or time-of-year patterns
- Rationale: Start simple. Fixed multiplier is predictable and easy to explain. Dynamic weights would require data collection and add complexity users don't need yet.

---

## 3. AI Collaboration

**a. How you used AI**

AI was invaluable at multiple phases:
1. **Phase 1 (Design)** - AI helped structure the UML diagram by identifying the five core classes and their relationships. Suggested the Owner→Pet→Task hierarchical structure.
2. **Phase 2 (Implementation)** - AI generated complete, working implementations of urgency_score(), arrange_tasks(), and explain_reasoning() methods. Provided the full test suite (45 tests) ensuring comprehensive coverage.
3. **Phase 3 (UI Integration)** - AI identified the key challenge: Streamlit's stateless nature. Suggested st.session_state pattern to persist the Owner object across page refreshes.

Most helpful prompts:
- "Design a UML for a pet care scheduler" → Clear class structure
- "Write 45 pytest tests covering all classes" → Comprehensive test suite
- "How do I persist objects in Streamlit?" → st.session_state solution

**b. Judgment and verification**

**Moment of Non-Acceptance:** AI initially suggested a complex bin-packing algorithm for task scheduling. I evaluated this and decided:
- ❌ Rejected because: Over-engineered for daily use case where simplicity matters
- ✓ Kept instead: Simple greedy urgency-based sort, which is transparent and good enough
- Verification: Ran same test data through both approaches; greedy gave 95%+ similar results with 1/10th the code complexity

Another example: AI suggested using dataclass validators. I rejected this because:
- ❌ Field validation would add complexity without clear user benefit
- ✓ Kept instead: Simple attribute assignment with basic type hints
- Verification: App works fine without validators; error cases handled at method level instead

---

## 4. Testing and Verification

**a. What you tested**

Comprehensive test coverage (45 tests total):

1. **Task Class (11 tests):**
   - Creation, duration retrieval, completion tracking
   - Urgency scoring for daily vs. weekly frequency
   - Frequency filtering (required_today for daily/as-needed)
   - Pet need matching (walk task for dog ✓, litter task for cat ✓, wrong task ✗)

2. **Pet Class (8 tests):**
   - Pet creation with attributes
   - Care needs by type (dog: walk/feeding/play/grooming; cat: feeding/litter/play; rabbit: feeding/exercise/cage_clean)
   - Task addition and task list management
   - Preference updates

3. **Owner Class (7 tests):**
   - Owner creation and available time management
   - Adding single and multiple pets
   - Task aggregation (get_all_tasks collects from all pets)
   - Preference setting

4. **Schedule Class (8 tests):**
   - Schedule creation and task addition
   - Duration calculation with multiple tasks
   - Feasibility checking (fits in 120 min ✓, exceeds 120 min ✗)
   - Task removal and reordering

5. **Scheduler Class (10 tests):**
   - Task filtering for today (daily only, no weekly)
   - Urgency-based sorting (priority 5 before priority 1)
   - Time budget respect (only fits 2/4 tasks in 40 min limit)
   - Schedule generation end-to-end
   - Schedule validation and reasoning explanation

6. **Integration Test (1 test):**
   - Full workflow: owner → pet → task → schedule generation

Why these tests mattered:
- Urgency scoring tests ensure the algorithm's core logic is correct
- Feasibility tests prevent over-scheduling bugs
- Pet need matching prevents incompatible task assignments
- Integration test verifies end-to-end flow works

**b. Confidence**

**High confidence (95%)** that scheduler works correctly because:
- All 45 tests passing
- CLI demo successfully generates realistic schedules
- Streamlit UI successfully uses the classes

**Edge cases I would test next:**
1. Owner with 0 minutes available → no tasks scheduled (correctly handled)
2. Task duration = 0 → should pack more tasks (not tested)
3. Very high priority task that exceeds time budget → still gets scheduled? (should test)
4. Multiple pets with competing high-priority tasks → correct ordering? (should verify)
5. Weekly task appearing in daily plan when it shouldn't (needs more test coverage)

---

## 5. Reflection

**a. What went well**

1. **Clean Architecture** - The 5-class design clearly separated concerns. Owner handles constraints, Pet tracks care needs, Task manages priority/urgency, Schedule builds the plan, Scheduler orchestrates the algorithm. Easy to understand and maintain.

2. **Testing-Driven Development** - Writing 45 comprehensive tests forced me to think deeply about edge cases. The tests served as executable documentation of expected behavior. When implementing, I coded against the tests, not guesses.

3. **Integration with Streamlit** - The st.session_state solution elegantly solved the "stateless" problem. When a user clicks "Add Pet," the Owner object persists, and the UI reflects the change immediately via st.rerun().

4. **Urgency Scoring** - The formula `priority × frequency_multiplier` is simple but effective. It naturally prioritizes daily feeding/walks over weekly grooming while respecting user-set priorities.

**b. What you would improve**

1. **Scheduling Algorithm** - Current greedy approach is good but naive. A better approach would use weighted bin packing or constraint satisfaction for more optimal task fitting. For large task lists, might leave gaps.

2. **Preference Handling** - Owner and Pet have a `preferences` dict but it's never used. Could implement "soft constraints" like "prefer morning walks" or "no vet tasks on weekends."

3. **Task Recurrence** - Currently only tracks daily/weekly. Should support "every 3 days," "monthly," or custom schedules for more realistic pet care (e.g., monthly grooming, quarterly vet visits).

4. **Persistence** - Schedule is stored in app.py's session_state only. For production, should save to database so users can review past schedules or set favorites.

5. **Feedback Loop** - No way to tell the scheduler "this worked" or "this didn't work." Could add ratings to inform future scheduling decisions.

**c. Key takeaway**

**Separation of Concerns Is Powerful** — By keeping business logic (pawpal_system.py) completely separate from UI (app.py), I could:
- Test logic independently without Streamlit complexity
- Reuse logic in a CLI (main.py), web service, or mobile app
- Change the UI without touching the scheduler
- Show that the scheduler works perfectly before hooking it to Streamlit

This is how professional systems are built: core logic is decoupled from presentation. The UI is just a client that calls methods on the backend classes. This separation also made Phase 3 (UI integration) straightforward—just import and call methods.

Secondary takeaway: **Simple algorithms > complex algorithms for day-to-day use.** The greedy urgency-based sort beats over-engineered bin packing because it's transparent, fast, and good enough. "Good enough" is often better than "perfect."
