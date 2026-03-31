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
- The original design did not establish a was for Owners to reference their Pets since they lived inside Schedular and Schedule. I also removed the redundant list of Tasks that was contained inside of Schedule and used a weekly_plan to avoid redundance. 

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
