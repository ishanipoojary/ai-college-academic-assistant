# Basic LLM vs RAG Comparison

This evaluation compares a basic LLM response with a Retrieval-Augmented Generation (RAG) response.

## Test 1

**Question:** What is the minimum attendance requirement?

### Basic LLM

The minimum attendance requirement generally varies depending on the institution, the academic department, and the individual instructor. 

Here are the most common standards across higher education:

* **Instructor/Syllabus-Specific Policies:** Many colleges leave attendance policies to the discretion of the course instructor. A common rule is allowing **2 to 3 unexcused absences** per term for a standard course before it negatively impacts your grade or leads to administrative withdrawal.
* **Percentage-Based Requirements:** In institutions or programs that enforce a fixed percentage (common in laboratory sciences, professional degree programs, or certain international university systems), the requirement is typically between **75% and 85%** of all scheduled classes to earn credit or sit for final exams.
* **Visa and Financial Aid Requirements:** Students receiving federal financial aid or attending on an international student visa often have strict attendance and active-participation mandates that must be met to maintain their status and funding.

To find the precise requirement for your situation, you should review the specific syllabus for each course, consult your academic advisor, or check your institution's official academic catalog or student portal.

### RAG

Based on the provided college regulations, the attendance requirements are as follows:

* A student must maintain a minimum attendance of **85% in each subject** (with each semester considered as a unit).
* There is a provision for the Principal to **condone up to 10%** of the attendance for valid reasons, such as medical grounds, participation in University-level sports, cultural activities, seminars, workshops, and paper presentations.

**Source:**
*
 [Source 1: 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 29]

### Retrieved Sources

- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 29 (distance: 0.7761)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 16 (distance: 0.9286)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 34 (distance: 1.0499)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 36 (distance: 1.0532)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 8 (distance: 1.0893)

---

## Test 2

**Question:** What are the weekly meeting requirements for the 8th semester project?

### Basic LLM

Weekly meeting requirements for an 8th-semester (final year/capstone) project vary depending on the institution, department, and individual faculty guide. However, standard academic practices typically involve the following:

### 1. Typical Meeting Frequency
* **Guide/Supervisor Meetings:** Most programs require project groups to meet with their assigned faculty guide **at least once per week** for 30 to 60 minutes.
* **Review Committee Meetings:** Periodic reviews (often monthly or at mid-semester/end-semester milestones) are usually held with an internal project evaluation committee in addition to regular guide meetings.

### 2. Standard Meeting Expectations
During weekly meetings, students are generally expected to:
* **Report Progress:** Present work completed over the previous week (e.g., literature review updates, code/system architecture, hardware prototypes, simulation results, or draft chapters).
* **Maintain a Project Logbook / Diary:** Most colleges require maintaining a weekly log sheet detailing tasks completed, hours spent, and targets for the next week. The faculty guide typically reviews and signs this logbook weekly.
* **Discuss Obstacles:** Bring up technical, logistical, or design challenges to receive guidance or approval for alternative approaches.
* **Set Weekly Milestones:** Agree on actionable goals to be delivered by the next scheduled meeting.

### 3. Evaluation and Attendance
* **Continuous Assessment:** Attendance and active participation in these weekly meetings often count directly toward the internal assessment/continuous evaluation component of your final project grade.
* **Unexcused Absences:** Missing consecutive meetings without prior notice may lead to point deductions or escalation to the project coordinator/head of department.

---

*Because exact requirements (such as required forms, minimum hours, and reporting templates) depend on your specific university and department regulations, you should verify the exact guidelines directly with your assigned project supervisor or departmental project coordinator.*

### RAG

Based on the provided college documents, the weekly meeting requirements for the 8th-semester project are as follows:

* **Format and Attendance:** The project guide and team members must conduct weekly meetings either in person or via Google Meet. All team members are required to be present.
* **Timeline:** Weekly meetings must begin from the week starting 25/01/2026, which is designated as Week 1.
* **Online Meeting Documentation:** If meetings are held online, the guide must take a screenshot each week, name the file with the respective team number and week number, and upload it to the designated Google Drive link.
* **Log Book:** Updating the log book weekly is mandatory. The guide must collect a soft copy of the updated log book and upload it to the respective Google Drive.
* **Interaction Hours:** The syllabus specifies 24 hours per week for interaction between the project guide and students.

**Sources:**
* *[Source 1: 8th_Semester_Project_Guidelines_2026.docx]*
* *[Source 2: 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 28]*

### Retrieved Sources

- 8th_Semester_Project_Guidelines_2026.docx (distance: 0.6357)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 28 (distance: 0.8738)
- 8th_Semester_Project_Guidelines_2026.docx (distance: 0.9399)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 29 (distance: 0.9483)
- 8th_Semester_Project_Guidelines_2026.docx (distance: 0.9794)

---

## Test 3

**Question:** What is the college hostel curfew time?

### Basic LLM

Hostel curfew times vary widely depending on the specific institution, the type of housing, and sometimes the student's academic year. 

At colleges that enforce a curfew, it typically falls between **9:00 PM and 11:00 PM** on weeknights, sometimes with later hours on weekends. Other institutions do not have a strict curfew at all and instead utilize 24-hour keycard or security-desk access.

To find the exact curfew time for your campus, you should check in directly with your hostel warden, Resident Advisor (RA), or the college housing and residence life office.

### RAG

The information regarding the college hostel curfew time could not be found in the provided college documents.

### Retrieved Sources

- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 14 (distance: 1.0319)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 43 (distance: 1.0373)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 17 (distance: 1.0622)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 14 (distance: 1.0730)
- 14ENGR09D2_B.Tech._IS_2024-02_Regulations_Syllabus.pdf, page 14 (distance: 1.0976)

---

## Overall Observation

The basic LLM answers using its general language knowledge without access to the college knowledge base.

The RAG system first retrieves relevant college documents and then generates an answer using that retrieved context.

For college-specific questions, RAG is expected to provide answers grounded in the uploaded institutional documents, while questions outside the knowledge base should be identified as unsupported rather than answered with invented college-specific information.