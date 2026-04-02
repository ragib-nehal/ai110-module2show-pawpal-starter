# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- For the initial UML design, I decided to create 5 classes. These included Pet, Owner, Task, Scheduler, and Schedule. Pet, Owner, and Task were necessary  by design but I decided to add a Scheduler class to seperate the responsibilities between it and Schedule,which only includes the data.        
- What classes did you include, and what responsibilities did you assign to each?
The 5 classes I went with are Pet, Owner, Task, Schedule, and Scheduler. Pet stores the primary data for the animal such as the name of the animal, type of species, and special needs. The Owner class holds the human's profile and availibility. Task contains the specific care activities, its duration, and frequency. Schedule primarily contains the data for the the 7-day period and Schedular is the algorithmic layer that creates it.  

**b. Design changes**

- Did your design change during implementation?
- Yes, I made a couple of changes to the original UML design to improve the relationships between the classes.
- If yes, describe at least one change and why you made it.
- The original design did not establish a was for Owners to reference their Pets since they lived inside Schedular and Schedule. I also removed the redundant list of Tasks that was contained inside of Schedule and used a weekly_plan to avoid redundance. Another change that I made was the addition of the OwnerScheduler class which handles an common case where an owner might have multple pets. This addresses the issue of conflicts that may result with tasks when an owner has multiple pets. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- Some of the constraints that my scheduler considers are time, preferred time, completion status, and frequency. Time is the daily time budget for the owner across all of the pets. Preferred time is used to sort tasks chronologically. Completion status allows us to exclude tasks from scheduling. Frequency helps manage how often a task occurs for pets.
- How did you decide which constraints mattered most?
- The constraints I mentioned are additional ones that may not have been mentioned in the question. But time, priority, and frequency were essetial. In a real world scenario, an owners cannot provide more time than they have and sometimes, more important tasks need to be prioritized. Frequency gives the owner a consistant schedule, automating the recurring tasks that are scheduled.  

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- One tradeoff I made was the use of the gredy packing algorithm which picks tasks in priority order and stops when the day is full. It does not backtract to lower priority tasks that may be able to fill in more slots during the day.
- Why is that tradeoff reasonable for this scenario?
- This tradeoff is reasonable since the priority of tasks outweight the need to get more done. For instance, if a dog's meds taks about 30 min with high priority, it cannot be overridden by a bath that was added before, has lower priority, and takes less time. Some tasks are non-negotiable.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- I used a combination of Claude-code and Copilot for this  project. Claude code was responsible for most of the coding aspect and I used Copilot to brain storm and plan. I've noticed having multple agents open at once helps take the load off of one tool and keeps the context window sharp. It was also really helpful to plan things out using the plan modee to not only critique that the AI was going to implement but also help the AI focus on smaller tasks rather than implement the entire login in one go.
- What kinds of prompts or questions were most helpful?
- One prompt I found helpful was asking Calude to explain what it will do before it implements the code. This helps me treat the AI almost like a fellow engineer that proposes a solution. Another prompt I've found really helpful is asking the llm to make code more readable and add docstrings for documentation.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- One time I rejected a suggestion from Claude is when it suggested that I sort tasks by time, which overlooks the priority of those tasks. Even though a task may take longer, its priority might be greater than a shorter task, but the AI overlooked this possibility.
- How did you evaluate or verify what the AI suggested?
- I think the easiest way to evaluate what the AI suggested was to go back to the original UML design and the backend logic of the app. Every new feature builds on a preexising blueprint, so if a feature violates the relationship between an owner and a pet, it would clearly be rejected.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- One behavior that I tested is Task Completion, which ensured that a task started incomplete and and once we marked a test complete, that task will be completed. I also tested the pet task management system, which starts off as an empty list, and calling the adding method will add tasks to that list, making them retrievable. I also tested the conflict detection, which handeled edge cases like when the time limit is exceeded by tasks or when pet tasks overlap.
- Why were these tests important?
- Task completion is essential so that the schedules are not corrupted by old tasks. Pet tasks are essentially the backbone of the schedule, so each pet must have at least one task. Conflict detection allows the owner to know when the overall tasks require more time than their schedule can provide.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- I'm confident that my scheduler correctly implemented most of the core features of the Pawpal app. I made sure to handle constraints, multiple pets, schedule conflicts, and sorting and filtering. I also included tip for the user. For instance, tasks that appear for multiple pets can be done together. 
- What edge cases would you test next if you had more time?
- If I had more time, I would definitely implement more tests to see where my logic breaks. For instance, is there a limit to how many pets an owner can have and what if all tasks for the pet(s) take up the maximum amount of time avaiable. For those edge cases, I would need to restructure the schedule so that tasks can be done in parallel so that high priority tasks can still be done. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
- I think I really nailed down the schedule generation aspect of the app and the handeling tasks when an owner is overbooked. The sorting and filtering feature I added to the UI is also convenient for users that want to filter by pets or view their remaining tasks.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
- I would definitely redesign the UI to be more intuative. Right now, everything is top to bottom, so I might be able to add a side panel or a menu bar at the top to make it more user friendly. I would also like to add a feature where you can add multiple owners so you can allocate tasks to multiple people. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
- One thing I learned is that designing your architecture/UML is necessary before you even implement any code. Without that blueprint, the app has no vision and you would have to design everything on the fly without a structured plan.