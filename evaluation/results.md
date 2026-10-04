# AI-Based College Academic Assistant

## Evaluation Results

### 1. Direct Academic Question

**Question:**  
What is the minimum attendance requirement for students?

**Basic LLM:**  
The basic LLM answers using its general language knowledge and does not have access to the specific college regulations.

**RAG-based Assistant:**  
The assistant retrieves the relevant college regulation from the knowledge base and generates an answer using the retrieved document context, along with source/page information.

**Observation:**  
RAG grounds the answer in the college's actual documents and provides source information, reducing the risk of unsupported college-specific answers.

**Result:** PASS

---

### 2. Follow-up Question

**Initial question:**  
What is the minimum attendance requirement?

**Follow-up:**  
What about condonation?

**RAG-based Assistant:**  
The assistant uses the previous conversation context while processing the follow-up question and retrieves relevant information from the college knowledge base.

**Observation:**  
The system maintains conversational context and can handle follow-up questions instead of treating every question as completely independent.

**Result:** PASS

---

### 3. Unknown Question

**Question:**  
What is the college hostel curfew time?

**Expected behavior:**  
If the information is not present in the college knowledge base, the assistant should not invent a college-specific answer.

**RAG-based Assistant:**  
The system checks the retrieved college documents. If sufficiently relevant information is not available, the workflow routes the request to unknown-question handling.

**Observation:**  
The system is designed to avoid unsupported college-specific answers when the required information is not present in the knowledge base.

**Result:** PASS

---

### 4. External API Integration

**Question:**  
What is the current weather in Bangalore?

**Processing:**
1. The question is analyzed.
2. The system identifies it as a weather request.
3. The LangGraph workflow routes the request to the weather tool.
4. The weather tool calls the Open-Meteo external weather API.
5. The weather information is formatted and returned.

**Result:** PASS

**Observation:**  
The system can distinguish requests requiring an external API from questions that should be answered using the college knowledge base.

---

### 5. Personalized Study Planner

**Input:**
- Subjects
- Available study hours per day
- Exam date

**Result:**  
The system generates a personalized study plan containing:
- Exam date
- Days remaining
- Available study hours
- Hours allocated to each subject
- Total study hours

**Observation:**  
The assistant can generate a study plan using the student's supplied constraints.

**Result:** PASS

---

### 6. Study Plan Modification

**Action:**  
The user changes the available study hours.

**Result:**  
The existing study plan is recalculated using the updated study-time constraint.

**Observation:**  
The assistant supports modification of an existing study plan rather than requiring the user to manually create another plan.

**Result:** PASS

---

### 7. Multi-Step Question

**Example:**  
Create a study plan for Data Communication, Operating Systems, and Computer Networks with 4 hours available per day and an exam date provided by the student.

**Processing:**

1. The question is analyzed.
2. The study-planner tool is selected.
3. The subjects, available hours, and exam date are extracted.
4. The study-plan tool calculates the available study time.
5. The plan is returned to the user.
6. The response is reviewed before completion.

**Observation:**  
The LangGraph workflow can break a complex request into multiple processing stages and use the appropriate tool before generating the final response.

**Result:** PASS

---

### 8. Document Summarization

**Question:**  
Summarize the 8th semester project guidelines.

**Processing:**

1. The request is identified as a document summarization request.
2. Relevant sections are retrieved from the college knowledge base.
3. The retrieved information is provided to the summarization prompt.
4. The LLM generates a concise summary using the retrieved context.
5. The response is reviewed before completion.

**Observation:**  
The system supports summarization of uploaded college documents through the RAG pipeline.

Tested with: "Summarize the 8th semester project guidelines"
The system retrieved the project guideline document and generated a student-friendly summary grounded in the retrieved content.

**Result:** PASS

**Note:**  
Final LLM-generated output depends on the availability of the configured Gemini API quota during testing.

---

## 9. Basic LLM vs RAG Comparison

The system was evaluated by asking the same college-related questions to:

1. A basic LLM without access to the college knowledge base.
2. The RAG-based academic assistant with access to the college documents.

### Test 1 — Attendance Requirement

**Question:**  
What is the minimum attendance requirement?

**Basic LLM:**  
The basic LLM provided a general range of attendance requirements and stated that the exact requirement depends on the institution.

**RAG-based Assistant:**  
The RAG system retrieved the college regulations and correctly identified the institution-specific requirement of 85% attendance, along with the provision for up to 10% condonation.

**Observation:**  
The RAG system provided a specific, document-grounded answer while the basic LLM could only provide general information.

---

### Test 2 — 8th Semester Project Guidelines

**Question:**  
What are the weekly meeting requirements for the 8th semester project?

**Basic LLM:**  
The basic LLM provided general expectations for weekly project meetings.

**RAG-based Assistant:**  
The RAG system retrieved the 2026 8th semester project guidelines and provided the institution-specific requirements, including weekly meetings, attendance of all team members, online meeting screenshots, and mandatory weekly log book updates.

**Observation:**  
RAG was able to provide current college-specific project requirements from the uploaded document instead of relying on generic academic practices.

---

### Test 3 — Unknown College Information

**Question:**  
What is the college hostel curfew time?

**Basic LLM:**  
The basic LLM provided a general estimated range for hostel curfew times.

**RAG-based Assistant:**  
The RAG system identified that the college knowledge base did not contain information about the hostel curfew time and did not invent a college-specific answer.

**Observation:**  
This demonstrates that RAG can avoid unsupported institution-specific answers when the required information is not available in the knowledge base.

---

### Comparison Summary

| Aspect | Basic LLM | RAG-based Assistant |
|---|---|---|
| General knowledge | Yes | Yes |
| Access to college documents | No | Yes |
| College-specific answers | May be generic or unreliable | Grounded in retrieved documents |
| Source information | Not available | Available |
| Current project guidelines | Not available | Available through retrieval |
| Unknown college information | May provide a guess | Can identify missing information |

**Result:** PASS

**Conclusion:**  
The comparison demonstrates that the RAG-based system is more suitable for a college academic assistant because it grounds institution-specific answers in the uploaded college documents and can avoid inventing information when the required information is not present in the knowledge base.

## 10. Overall Evaluation

| Requirement | Result |
|---|---|
| Direct academic Q&A | PASS |
| RAG retrieval | PASS |
| College document knowledge base | PASS |
| Source/page information | PASS |
| Follow-up questions | PASS |
| Conversational memory | PASS |
| Unknown-question handling | PASS |
| Document summarization | PASS |
| Study planner | PASS |
| Study-plan modification | PASS |
| SGPA calculation tool | PASS |
| CGPA calculation tool | PASS |
| Exam countdown tool | PASS |
| External weather API | PASS |
| LangGraph workflow | PASS |
| Response review stage | PASS |
| Streamlit UI | PASS |
| Basic LLM vs RAG comparison | PASS |

---

## 11. Conclusion

The AI-Based College Academic Assistant combines an LLM, Retrieval-Augmented Generation (RAG), LangChain, LangGraph, a Chroma vector database, local academic tools, an external weather API, conversational context, and a Streamlit user interface.

The system can retrieve information from college documents, answer academic questions, maintain conversation context, handle unsupported questions, perform academic calculations, generate and modify personalized study plans, summarize documents, and use an external API when required.

The LangGraph workflow separates question analysis, information retrieval, tool execution, response generation, and response review into distinct processing stages.

The Basic LLM vs RAG comparison demonstrates why retrieval is useful for institution-specific academic assistance: the RAG system can ground its responses in the college's uploaded documents and provide source information.

The project therefore satisfies the major functional requirements of an AI-based college academic assistant while providing a simple interface suitable for demonstration.