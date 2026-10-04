from typing import TypedDict, List, Dict, Optional

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.rag import (
    retrieve_documents_with_scores,
    format_sources,
    is_relevant,
)

from src.llm import get_llm
from src.prompts import ACADEMIC_QA_PROMPT, SUMMARY_PROMPT

from src.tools import (
    calculate_sgpa_from_grades,
    calculate_days_until_exam,
    create_study_plan,
    modify_study_plan,
)

from src.external_api import (
    get_weather,
    format_weather_result,
)


# ============================================================
# STATE
# ============================================================

class AcademicAssistantState(TypedDict, total=False):
    question: str
    standalone_question: str
    context: str
    answer: str
    sources: List[Dict]
    conversation_history: List[Dict]
    tool_name: str
    tool_result: str
    current_plan: Optional[Dict]
    review_passed: bool


# ============================================================
# QUESTION ANALYSIS
# ============================================================

def question_analysis_node(state: AcademicAssistantState):

    question = state["question"]

    history = state.get(
        "conversation_history",
        []
    )

    llm = get_llm()

    history_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in history
    )

    prompt = f"""
You are analyzing a student's question for a college
academic assistant.

Previous conversation:

{history_text if history_text else "No previous conversation."}

Current question:

{question}

Available tools:

- sgpa
- exam_countdown
- study_planner
- modify_study_plan
- weather
- summary
- none

Tool selection rules:

- Choose sgpa when the student asks to calculate SGPA.
- Choose exam_countdown when the student asks how many
  days remain until an exam or provides an exam date
  for a countdown.
- Choose study_planner when the student wants to create
  a study plan.
- Choose modify_study_plan when the student wants to
  change, update, reduce, increase, or reschedule an
  existing study plan.
- Choose weather when the student asks about current
  weather, temperature, rainfall, humidity, wind, or
  forecast for a location.
- Choose none for normal college academic questions
  that should be answered using the college knowledge base.
- Choose summary when the student asks to summarize,
  summarise, or provide a summary of college documents.

Return exactly:

QUESTION: <standalone question>
TOOL: <sgpa OR exam_countdown OR study_planner OR modify_study_plan OR weather OR summary OR none>
"""

    response = llm.invoke(prompt)
    result = response.content

    if isinstance(result, list):
        result = "".join(
            item.get("text", "")
            for item in result
            if isinstance(item, dict)
        )

    standalone_question = question
    tool_name = "none"

    for line in result.splitlines():

        if line.startswith("QUESTION:"):
            standalone_question = line.replace(
                "QUESTION:",
                ""
            ).strip()

        elif line.startswith("TOOL:"):
            tool_name = line.replace(
                "TOOL:",
                ""
            ).strip().lower()

    valid_tools = {
        "sgpa",
        "exam_countdown",
        "study_planner",
        "modify_study_plan",
        "weather",
        "summary",
        "none",
    }

    if tool_name not in valid_tools:
        tool_name = "none"

    return {
        **state,
        "standalone_question": standalone_question,
        "tool_name": tool_name,
    }


# ============================================================
# INFORMATION RETRIEVAL
# ============================================================

def information_retrieval_node(
    state: AcademicAssistantState
):

    question = state["standalone_question"]

    results = retrieve_documents_with_scores(
        question,
        k=5
    )

    documents = [
        document
        for document, score in results
    ]

    sources = format_sources(documents)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    relevant = is_relevant(
        results,
        threshold=1.2
    )

    return {
        **state,
        "context": context,
        "sources": sources,
        "review_passed": relevant,
    }


# ============================================================
# SGPA TOOL
# ============================================================

def sgpa_tool_node(
    state: AcademicAssistantState
):

    import re

    question = state["question"]

    pattern = (
        r"\b(O|A\+|A|B\+|B|C|P|F|AB)"
        r"\s*[-:]?\s*"
        r"(\d+(?:\.\d+)?)"
        r"\s*(?:credits?|cr)?"
    )

    matches = re.findall(
        pattern,
        question,
        flags=re.IGNORECASE
    )

    if not matches:

        return {
            **state,
            "tool_result":
                "Could not detect grades and credits."
        }

    courses = []

    for grade, credits in matches:

        courses.append({
            "grade": grade,
            "credits": float(credits)
        })

    try:

        sgpa = calculate_sgpa_from_grades(
            courses
        )

        result = f"Calculated SGPA: {sgpa}"

    except Exception as error:

        result = f"SGPA calculation error: {error}"

    return {
        **state,
        "tool_result": result
    }


# ============================================================
# EXAM COUNTDOWN TOOL
# ============================================================

def exam_countdown_tool_node(
    state: AcademicAssistantState
):

    import re

    question = state["question"]

    match = re.search(
        r"\b\d{4}-\d{2}-\d{2}\b",
        question
    )

    if not match:

        return {
            **state,
            "tool_result":
                "Could not detect an exam date."
        }

    exam_date = match.group()

    try:

        days = calculate_days_until_exam(
            exam_date
        )

        if days > 0:

            result = (
                f"Exam date: {exam_date}\n"
                f"Days remaining: {days}"
            )

        elif days == 0:

            result = (
                f"Exam date: {exam_date}\n"
                f"The exam is today."
            )

        else:

            result = (
                f"Exam date: {exam_date}\n"
                f"The exam was {abs(days)} days ago."
            )

    except Exception as error:

        result = f"Exam countdown error: {error}"

    return {
        **state,
        "tool_result": result
    }


# ============================================================
# STUDY PLANNER TOOL
# ============================================================

def study_planner_tool_node(
    state: AcademicAssistantState
):

    import re

    question = state["question"]

    hours_match = re.search(
        r"(\d+(?:\.\d+)?)\s*hours?\s*(?:per day|a day|daily)",
        question,
        flags=re.IGNORECASE
    )

    date_match = re.search(
        r"\b\d{4}-\d{2}-\d{2}\b",
        question
    )

    if not hours_match or not date_match:

        return {
            **state,
            "tool_result": (
                "To create a study plan, I need "
                "your subjects, available study hours "
                "per day, and exam date in YYYY-MM-DD format."
            )
        }

    hours_per_day = float(
        hours_match.group(1)
    )

    exam_date = date_match.group()

    subjects = []

    subject_match = re.search(
        r"(?:subjects?|courses?)\s*[:\-]\s*(.+?)(?:\s+for\s+\d+(?:\.\d+)?\s*hours?|$)",
        question,
        flags=re.IGNORECASE
    )

    if subject_match:

        subject_text = subject_match.group(1)

        subjects = [
            subject.strip()
            for subject in re.split(
                r",|;|\band\b",
                subject_text,
                flags=re.IGNORECASE
            )
            if subject.strip()
        ]

    if not subjects:

        match = re.search(
            r"(?:study|prepare)\s+for\s+(.+?)"
            r"\s+(?:for|with)\s+\d+(?:\.\d+)?\s*hours?",
            question,
            flags=re.IGNORECASE
        )

        if match:

            subject_text = match.group(1)

            subjects = [
                subject.strip()
                for subject in re.split(
                    r",|;|\band\b",
                    subject_text,
                    flags=re.IGNORECASE
                )
                if subject.strip()
            ]

    if not subjects:

        return {
            **state,
            "tool_result": (
                "I need the subjects to create "
                "your study plan."
            )
        }

    try:

        plan = create_study_plan(
            subjects=subjects,
            hours_per_day=hours_per_day,
            exam_date=exam_date
        )

        result_lines = [
            "Study Plan:",
            f"Exam date: {plan['exam_date']}",
            f"Days remaining: {plan['days_remaining']}",
            f"Study hours per day: {plan['hours_per_day']}",
            f"Total available study hours: "
            f"{plan['total_study_hours']}",
            "",
        ]

        for item in plan["subjects"]:

            result_lines.append(
                f"- {item['subject']}: "
                f"{item['hours_per_day']} hours/day "
                f"({item['total_hours']} total hours)"
            )

        result = "\n".join(result_lines)

    except Exception as error:

        result = f"Study planner error: {error}"
        plan = None

    return {
        **state,
        "tool_result": result,
        "current_plan": plan,
    }


# ============================================================
# MODIFY STUDY PLAN TOOL
# ============================================================

def modify_study_plan_tool_node(
    state: AcademicAssistantState
):

    import re

    existing_plan = state.get(
        "current_plan"
    )

    if not existing_plan:

        return {
            **state,
            "tool_result": (
                "There is no existing study plan "
                "in the current conversation. "
                "Please create a study plan first."
            )
        }

    question = state["question"]

    hours_match = re.search(
        r"(\d+(?:\.\d+)?)\s*hours?\s*(?:per day|a day|daily)",
        question,
        flags=re.IGNORECASE
    )

    new_hours = None

    if hours_match:

        new_hours = float(
            hours_match.group(1)
        )

    date_match = re.search(
        r"\b\d{4}-\d{2}-\d{2}\b",
        question
    )

    new_exam_date = None

    if date_match:

        new_exam_date = date_match.group()

    try:

        updated_plan = modify_study_plan(
            existing_plan=existing_plan,
            new_hours_per_day=new_hours,
            new_exam_date=new_exam_date,
        )

        result_lines = [
            "Updated Study Plan:",
            f"Exam date: {updated_plan['exam_date']}",
            f"Days remaining: "
            f"{updated_plan['days_remaining']}",
            f"Study hours per day: "
            f"{updated_plan['hours_per_day']}",
            f"Total available study hours: "
            f"{updated_plan['total_study_hours']}",
            "",
        ]

        for item in updated_plan["subjects"]:

            result_lines.append(
                f"- {item['subject']}: "
                f"{item['hours_per_day']} hours/day "
                f"({item['total_hours']} total hours)"
            )

        result = "\n".join(result_lines)

    except Exception as error:

        result = (
            f"Study plan modification error: "
            f"{error}"
        )

        updated_plan = existing_plan

    return {
        **state,
        "tool_result": result,
        "current_plan": updated_plan,
    }


# ============================================================
# WEATHER TOOL
# ============================================================

def weather_tool_node(
    state: AcademicAssistantState
):

    import re

    question = state["question"]

    city = None

    patterns = [
        r"weather\s+(?:in|at|for)\s+([A-Za-z ]+)",
        r"temperature\s+(?:in|at|for)\s+([A-Za-z ]+)",
        r"forecast\s+(?:in|for)\s+([A-Za-z ]+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            question,
            flags=re.IGNORECASE
        )

        if match:

            city = match.group(1).strip()

            city = re.sub(
                r"\b(today|tomorrow|now|currently)\b",
                "",
                city,
                flags=re.IGNORECASE
            ).strip()

            break

    if not city:

        return {
            **state,
            "tool_result": (
                "I need a city name to check the weather."
            )
        }

    try:

        weather = get_weather(city)

        result = format_weather_result(
            weather
        )

    except Exception as error:

        result = (
            f"Weather lookup error: {error}"
        )

    return {
        **state,
        "tool_result": result
    }


# ============================================================
# NO TOOL
# ============================================================

def no_tool_node(
    state: AcademicAssistantState
):

    return {
        **state,
        "tool_result": ""
    }


# ============================================================
# UNKNOWN QUESTION
# ============================================================

def unknown_question_node(
    state: AcademicAssistantState
):

    answer = (
        "I couldn't find this information in the "
        "available college knowledge base. "
        "I don't want to guess or provide information "
        "that is not supported by the college documents."
    )

    return {
        **state,
        "answer": answer,
    }


# ============================================================
# SUMMARY GENERATION
# ============================================================

def summary_generation_node(
    state: AcademicAssistantState
):
    """
    Generate a student-friendly summary using only retrieved
    college-document context.
    """

    llm = get_llm()

    context = state.get("context", "").strip()
    question = state.get(
        "standalone_question",
        state["question"]
    )

    prompt = SUMMARY_PROMPT.format(
        context=context,
    )

    full_prompt = f"""
{prompt}

The student's request is:
{question}

Create the summary now.
"""

    response = llm.invoke(full_prompt)
    answer = response.content

    if isinstance(answer, list):
        answer = "".join(
            item.get("text", "")
            for item in answer
            if isinstance(item, dict)
        )

    history = state.get(
        "conversation_history",
        []
    )

    updated_history = list(history)

    updated_history.append({
        "role": "user",
        "content": state["question"]
    })

    updated_history.append({
        "role": "assistant",
        "content": answer
    })

    return {
        **state,
        "answer": answer,
        "conversation_history":
            updated_history,
    }


# ============================================================
# RESPONSE GENERATION
# ============================================================

def response_generation_node(
    state: AcademicAssistantState
):

    llm = get_llm()

    history = state.get(
        "conversation_history",
        []
    )

    history_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in history
    )

    tool_result = state.get(
        "tool_result",
        ""
    )

    context = state.get(
        "context",
        ""
    )

    question = state.get(
        "standalone_question",
        state["question"]
    )

    # Tool/API responses do not need RAG context.
    if tool_result:

        full_prompt = f"""
You are a college academic assistant.

Answer the student's question using the tool result below.

Rules:
- Use the tool result as the source of truth.
- Do not invent information.
- Give a clear and concise answer.
- If the tool result contains an error, explain the error clearly.
- Do not claim that information came from the college
  knowledge base if it came from an external tool.

Student question:
{question}

Previous conversation:
{history_text if history_text else "No previous conversation."}

Tool result:
{tool_result}

Answer:
"""

    else:

        prompt = ACADEMIC_QA_PROMPT.format(
            context=context,
            question=question
        )

        full_prompt = f"""
{prompt}

Previous conversation:

{history_text if history_text else "No previous conversation."}

Tool result:

No tool was used.

Use the previous conversation when necessary
to understand follow-up questions.
"""

    response = llm.invoke(full_prompt)

    answer = response.content

    if isinstance(answer, list):

        answer = "".join(
            item.get("text", "")
            for item in answer
            if isinstance(item, dict)
        )

    updated_history = list(history)

    updated_history.append({
        "role": "user",
        "content": state["question"]
    })

    updated_history.append({
        "role": "assistant",
        "content": answer
    })

    return {
        **state,
        "answer": answer,
        "conversation_history":
            updated_history,
    }


# ============================================================
# RESPONSE REVIEW
# ============================================================

def response_review_node(
    state: AcademicAssistantState
):

    answer = state.get(
        "answer",
        ""
    ).strip()

    context = state.get(
        "context",
        ""
    ).strip()

    sources = state.get(
        "sources",
        []
    )

    tool_name = state.get(
        "tool_name",
        "none"
    )

    # Summary responses must be based on retrieved
    # college-document context and sources.
    if tool_name == "summary":

        review_passed = (
            bool(answer)
            and bool(context)
            and len(sources) > 0
        )

    # Tool/API responses are valid without RAG sources.
    elif tool_name != "none":

        review_passed = bool(
            answer
        )

    # Unknown-question responses are valid even though
    # they were not generated from the LLM.
    elif not state.get(
        "review_passed",
        False
    ):

        review_passed = bool(answer)

    # Normal RAG responses require context and sources.
    else:

        review_passed = (
            bool(answer)
            and bool(context)
            and len(sources) > 0
        )

    return {
        **state,
        "review_passed": review_passed,
    }


# ============================================================
# ROUTER AFTER ANALYSIS
# ============================================================

def route_after_analysis(
    state: AcademicAssistantState
):

    tool_name = state.get(
        "tool_name",
        "none"
    )

    # Tool questions bypass RAG retrieval.

    if tool_name == "sgpa":
        return "sgpa_tool"

    if tool_name == "exam_countdown":
        return "exam_countdown_tool"

    if tool_name == "study_planner":
        return "study_planner_tool"

    if tool_name == "modify_study_plan":
        return "modify_study_plan_tool"

    if tool_name == "weather":
        return "weather_tool"

    # Summaries need retrieved college-document context.
    if tool_name == "summary":
        return "information_retrieval"

    return "information_retrieval"


# ============================================================
# ROUTER AFTER RETRIEVAL
# ============================================================

def route_after_retrieval(
    state: AcademicAssistantState
):

    # Summary request: use the retrieved context to
    # generate a document-grounded summary.
    if state.get("tool_name") == "summary":

        if state.get("review_passed", False):
            return "summary_generation"

        return "unknown_question"

    # Normal academic question.

    if state.get(
        "review_passed",
        False
    ):

        return "response_generation"

    # No relevant college information.

    return "unknown_question"


# ============================================================
# BUILD GRAPH
# ============================================================

def build_academic_graph():

    workflow = StateGraph(
        AcademicAssistantState
    )

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    workflow.add_node(
        "question_analysis",
        question_analysis_node
    )

    workflow.add_node(
        "information_retrieval",
        information_retrieval_node
    )

    workflow.add_node(
        "sgpa_tool",
        sgpa_tool_node
    )

    workflow.add_node(
        "exam_countdown_tool",
        exam_countdown_tool_node
    )

    workflow.add_node(
        "study_planner_tool",
        study_planner_tool_node
    )

    workflow.add_node(
        "modify_study_plan_tool",
        modify_study_plan_tool_node
    )

    workflow.add_node(
        "weather_tool",
        weather_tool_node
    )

    workflow.add_node(
        "summary_generation",
        summary_generation_node
    )

    workflow.add_node(
        "no_tool",
        no_tool_node
    )

    workflow.add_node(
        "unknown_question",
        unknown_question_node
    )

    workflow.add_node(
        "response_generation",
        response_generation_node
    )

    workflow.add_node(
        "response_review",
        response_review_node
    )

    # --------------------------------------------------------
    # Entry
    # --------------------------------------------------------

    workflow.set_entry_point(
        "question_analysis"
    )

    # --------------------------------------------------------
    # Question analysis → tool OR RAG
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "question_analysis",
        route_after_analysis,
        {
            "sgpa_tool":
                "sgpa_tool",

            "exam_countdown_tool":
                "exam_countdown_tool",

            "study_planner_tool":
                "study_planner_tool",

            "modify_study_plan_tool":
                "modify_study_plan_tool",

            "weather_tool":
                "weather_tool",

            "information_retrieval":
                "information_retrieval",
        }
    )

    # --------------------------------------------------------
    # RAG → answer OR unknown
    # --------------------------------------------------------

    workflow.add_conditional_edges(
        "information_retrieval",
        route_after_retrieval,
        {
            "response_generation":
                "response_generation",

            "summary_generation":
                "summary_generation",

            "unknown_question":
                "unknown_question",
        }
    )

    # --------------------------------------------------------
    # Tool nodes → response generation
    # --------------------------------------------------------

    workflow.add_edge(
        "sgpa_tool",
        "response_generation"
    )

    workflow.add_edge(
        "exam_countdown_tool",
        "response_generation"
    )

    workflow.add_edge(
        "study_planner_tool",
        "response_generation"
    )

    workflow.add_edge(
        "modify_study_plan_tool",
        "response_generation"
    )

    workflow.add_edge(
        "weather_tool",
        "response_generation"
    )

    # --------------------------------------------------------
    # Response generation → review
    # --------------------------------------------------------

    workflow.add_edge(
        "response_generation",
        "response_review"
    )

    workflow.add_edge(
        "summary_generation",
        "response_review"
    )

    # --------------------------------------------------------
    # Unknown → review
    # --------------------------------------------------------

    workflow.add_edge(
        "unknown_question",
        "response_review"
    )

    # --------------------------------------------------------
    # Review → END
    # --------------------------------------------------------

    workflow.add_edge(
        "response_review",
        END
    )

    # --------------------------------------------------------
    # Memory
    # --------------------------------------------------------

    memory = MemorySaver()

    return workflow.compile(
        checkpointer=memory
    )


# ============================================================
# GRAPH TEST
# ============================================================

if __name__ == "__main__":

    graph = build_academic_graph()

    print(
        "COMPLETE ACADEMIC GRAPH OK"
    )
