# AI-Based College Academic Assistant

## 1. Project Overview

The AI-Based College Academic Assistant is a Retrieval-Augmented Generation (RAG) based academic assistant designed to answer college-specific academic questions using official college documents.

The system combines:
- Large Language Model (Gemini)
- Retrieval-Augmented Generation (RAG)
- LangChain
- LangGraph
- Chroma vector database
- Academic calculation tools
- Personalized study planning
- External API integration
- Conversational context
- Streamlit user interface

---

## 2. Main Features

### Academic Question Answering

Answers college-specific questions using information retrieved from the uploaded academic documents.

### Document Summarization

Summarizes college documents such as project guidelines and regulations in a student-friendly format.

### Conversational Follow-up

Maintains conversation context so that follow-up questions can be answered using the previous interaction.

### Personalized Study Planner

Creates a study plan based on:
- Subjects
- Available study hours
- Examination date

### Study Plan Modification

Allows students to modify an existing study plan, such as changing the available study hours.

### Academic Tools

Provides tools for:
- SGPA calculation
- CGPA calculation
- Examination countdown
- Study planning
- Study plan modification

### External API

Uses an external weather API as an example of tool/API integration.

### Unknown Question Handling

If the requested information is not available in the college knowledge base, the system avoids inventing an answer and informs the user that the information could not be found.

### Basic LLM vs RAG Comparison

The project evaluates the difference between:
- A basic LLM response
- A RAG-based response using college documents

---

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| LLM | Google Gemini |
| LLM Framework | LangChain |
| Agent Workflow | LangGraph |
| Vector Database | Chroma |
| Embeddings | Chroma ONNX Default Embedding Function |
| Document Processing | PyPDF, python-docx |
| Frontend | Streamlit |
| External API | Open-Meteo |
| Environment Management | python-dotenv |

---

## 4. Project Structure

~~~text
L&T/
├── data/
├── docs/
├── evaluation/
│   ├── compare_llm_rag.py
│   ├── results.md
│   └── basic_vs_rag_results.md
├── src/
│   ├── app.py
│   ├── config.py
│   ├── external_api.py
│   ├── graph.py
│   ├── ingest.py
│   ├── llm.py
│   ├── memory.py
│   ├── prompts.py
│   ├── qa.py
│   ├── rag.py
│   └── tools.py
├── chroma_db/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
~~~

---

## 5. Knowledge Base

The system currently uses the following college documents:

1. B.Tech Information Science Regulations and Syllabus
2. 8th Semester Project Guidelines 2026
3. B.Tech First Year syllabus for AIDS, AIML, CCE, CSE, ISE, RAI, CYB and CSBS
4. B.Tech First Year syllabus for AER, MEC, CIV and BTY

These documents are processed, divided into smaller chunks, embedded, and stored in Chroma for retrieval.

Current knowledge base:

- Documents/sections loaded: 640
- Chunks stored: 1916

---

## 6. RAG Pipeline

The system follows this pipeline:

~~~text
College Documents
       ↓
Document Loading
       ↓
Text Preprocessing
       ↓
Chunking
       ↓
Embedding
       ↓
Chroma Vector Database
       ↓
User Question
       ↓
Question Analysis
       ↓
Relevant Document Retrieval
       ↓
Context + Prompt
       ↓
Gemini LLM
       ↓
Response Review
       ↓
Final Answer
~~~

---

## 7. LangGraph Workflow

The academic assistant uses LangGraph to organize the processing workflow.

Main nodes include:

1. Question Analysis
2. Information Retrieval
3. Response Generation
4. Summary Generation
5. Response Review
6. Tool Execution
7. Unknown Question Handling

The question analysis stage determines whether the request requires:
- Academic RAG
- Document summarization
- SGPA/CGPA calculation
- Examination countdown
- Study planning
- Study plan modification
- Weather information
- No tool

---

## 8. Prompt Templates

Reusable prompt templates are used for different academic tasks.

The system includes prompts for:

- Academic question answering
- Document summarization
- Study planning
- Tool selection

This allows prompts to be reused instead of creating a new prompt for every request.

---

## 9. Personalized Study Planner

The study planner accepts information such as:

- Subjects
- Available study hours per day
- Examination date

It then calculates:

- Days remaining
- Total available study hours
- Approximate study time per subject

The generated plan can subsequently be modified when the student's available study time changes.

---

## 10. External API Integration

The project demonstrates external tool/API integration using the Open-Meteo weather API.

The weather tool retrieves weather information and integrates the result into the LangGraph workflow.

This demonstrates that the assistant can use external services in addition to the college knowledge base.

---

## 11. Conversation Memory

The system maintains conversational context using LangGraph memory.

This allows follow-up questions such as:

~~~text
User: What is the minimum attendance requirement?

Assistant: The minimum attendance requirement is 85%.

User: What about condonation?

Assistant: The system uses the previous conversation context to interpret the follow-up question.
~~~

---

## 12. Unknown Question Handling

The system is designed not to hallucinate college-specific information.

For example, if a student asks about information that is not present in the knowledge base, the system indicates that the information could not be found instead of presenting an unsupported college-specific answer.

---

## 13. Evaluation

The system was tested using:

- Direct academic questions
- Follow-up questions
- RAG-based questions
- Unknown questions
- Multi-step questions
- Document summarization
- Study planning
- Study plan modification
- External API usage
- Basic LLM vs RAG comparison

### Basic LLM vs RAG

The comparison demonstrated that:

- A basic LLM may provide generic or unsupported answers for college-specific questions.
- RAG retrieves information from the provided college documents and produces answers grounded in those documents.
- For information unavailable in the knowledge base, the RAG system can identify that the information was not found.

Detailed evaluation results are available in:

- `evaluation/results.md`
- `evaluation/basic_vs_rag_results.md`

---

## 14. Running the Project

### Step 1: Activate the virtual environment

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

### Step 2: Install dependencies

~~~powershell
python -m pip install -r requirements.txt
~~~

### Step 3: Configure the API key

Create a `.env` file containing the required Google Gemini API key.

Example:

~~~text
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
~~~

Do not commit the `.env` file to version control.

### Step 4: Build the knowledge base

~~~powershell
.\.venv\Scripts\python.exe -m src.ingest
~~~

### Step 5: Run the Streamlit application

~~~powershell
.\.venv\Scripts\python.exe -m streamlit run src\app.py
~~~

The application can then be opened in the browser using the local Streamlit URL displayed in the terminal.

---

## 15. Project Outcome

The completed system demonstrates how an AI academic assistant can combine:

~~~text
LLM
+
RAG
+
Vector Database
+
LangChain
+
LangGraph
+
Tools/APIs
+
Conversation Memory
+
Personalized Planning
+
Streamlit UI
~~~

to provide a college-focused academic assistance system.