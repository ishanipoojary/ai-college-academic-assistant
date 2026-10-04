import streamlit as st
from src.tools import create_study_plan, modify_study_plan


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="College Academic Assistant",
    page_icon="🎓",
    layout="wide",
)


# ============================================================
# LAZY LOAD LANGGRAPH
# ============================================================

@st.cache_resource
def get_graph():
    # Import the heavy AI/RAG stack only when the
    # Academic Assistant is actually used.
    from src.graph import build_academic_graph
    return build_academic_graph()


# ============================================================
# SESSION STATE
# ============================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "student_session_1"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_plan" not in st.session_state:
    st.session_state.current_plan = None


# ============================================================
# HELPER — DISPLAY STUDY PLAN
# ============================================================

def display_study_plan(plan, title="📚 Your Study Plan"):

    if not isinstance(plan, dict):
        st.write(plan)
        return

    st.subheader(title)

    exam_date = plan.get("exam_date")
    days_remaining = plan.get("days_remaining")
    hours_per_day = plan.get("hours_per_day")
    total_study_hours = plan.get("total_study_hours")

    # Summary
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📅 Exam Date",
            str(exam_date) if exam_date else "N/A"
        )

    with col2:
        st.metric(
            "⏳ Days Remaining",
            str(days_remaining)
            if days_remaining is not None
            else "N/A"
        )

    with col3:
        st.metric(
            "⏱️ Hours / Day",
            str(hours_per_day)
            if hours_per_day is not None
            else "N/A"
        )

    with col4:
        st.metric(
            "📖 Total Study Hours",
            str(total_study_hours)
            if total_study_hours is not None
            else "N/A"
        )

    st.write("")

    subjects = plan.get("subjects", [])

    if subjects:
        st.markdown("### 📖 Subject-wise Plan")

        for subject in subjects:

            if isinstance(subject, dict):

                name = subject.get("subject", "Subject")
                subject_hours = subject.get("hours_per_day", 0)
                days = subject.get("days", 0)
                total_hours = subject.get("total_hours", 0)

                # Use simple Streamlit elements instead of
                # bordered containers for maximum compatibility.
                st.markdown(f"#### 📘 {name}")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write("⏱️ **Daily Study**")
                    st.write(f"{subject_hours} hour(s)")

                with col2:
                    st.write("📅 **Study Days**")
                    st.write(f"{days} days")

                with col3:
                    st.write("📚 **Total Study**")
                    st.write(f"{total_hours} hour(s)")

                st.divider()

            else:
                st.write(subject)

    else:
        st.info("No subject-wise plan available.")


# ============================================================
# HEADER
# ============================================================

st.title("🎓 College Academic Assistant")

st.write(
    "Your intelligent assistant for college regulations, "
    "academic policies, study planning, and academic calculations."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🛠️ Academic Tools")

    st.markdown(
        """
        **The assistant can help with:**

        📚 Academic questions  
        🔎 College document search  
        📝 Document summarization  
        🧮 SGPA / CGPA calculations  
        📅 Exam countdown  
        📖 Personalized study planning  
        🔄 Study plan modification  
        🌦️ External information lookup
        """
    )

    st.divider()

    st.subheader("📚 Knowledge Base")

    st.write(
        "College regulations, curriculum, "
        "academic policies and related documents."
    )


# ============================================================
# ACADEMIC QUESTION SECTION
# ============================================================

st.subheader("💬 Ask the Academic Assistant")

question = st.text_input(
    "What would you like to know?",
    placeholder=(
        "e.g. What is the minimum attendance requirement? "
        "or Summarize the 8th semester project guidelines"
    ),
)


# ============================================================
# ASK ASSISTANT
# ============================================================

if st.button("🚀 Ask Assistant", type="primary"):

    if not question.strip():

        st.warning("⚠️ Please enter a question.")

    else:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.write(question)

        try:

            graph = get_graph()

            config = {
                "configurable": {
                    "thread_id": st.session_state.thread_id
                }
            }

            result = graph.invoke(
                {
                    "question": question,
                    "conversation_history": st.session_state.messages[:-1],
                    "current_plan": st.session_state.current_plan,
                },
                config=config,
            )

            answer = result.get(
                "answer",
                "I could not generate an answer."
            )

            with st.chat_message("assistant"):

                st.write(answer)

                sources = result.get("sources", [])

                if sources:

                    with st.expander("📚 View Sources"):

                        for source in sources:

                            page = source.get("page")
                            source_file = source.get(
                                "source",
                                "Unknown document"
                            )

                            if page is not None:
                                st.markdown(
                                    f"**📄 {source_file} — Page {page}**"
                                )
                            else:
                                st.markdown(
                                    f"**📄 {source_file}**"
                                )

                            content = source.get(
                                "content",
                                ""
                            )

                            if content:
                                st.write(content[:500])

                            st.divider()

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as e:

            error_message = str(e)

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
                or "quota" in error_message.lower()
            ):

                with st.chat_message("assistant"):

                    st.warning(
                        "⏳ Gemini API quota is currently exhausted."
                    )

                    st.write(
                        "The LangGraph and RAG backend is connected, "
                        "but Gemini cannot generate an answer until "
                        "the API quota refreshes."
                    )

            else:

                with st.chat_message("assistant"):

                    st.error(
                        "Something went wrong while processing "
                        "the question."
                    )

                    st.code(error_message)


# ============================================================
# CONVERSATION HISTORY
# ============================================================

if st.session_state.messages:

    st.divider()

    st.subheader("💬 Conversation")

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"**👤 You:** {message['content']}"
            )

        else:

            st.markdown(
                f"**🤖 Assistant:** {message['content']}"
            )


# ============================================================
# PERSONALIZED STUDY PLANNER
# ============================================================

st.divider()

st.subheader("📖 Personalized Study Planner")

st.write(
    "Create a study plan based on your subjects, "
    "available study time, and exam date."
)

col1, col2 = st.columns(2)

with col1:

    subjects = st.text_input(
        "Subjects",
        placeholder=(
            "Data Communication, Operating Systems, "
            "Graphics, ESD"
        ),
    )

    hours_per_day = st.number_input(
        "Available study hours per day",
        min_value=0.5,
        max_value=24.0,
        value=4.0,
        step=0.5,
    )

with col2:

    exam_date = st.date_input(
        "Exam date"
    )


# ============================================================
# CREATE STUDY PLAN
# ============================================================

if st.button("📅 Create Study Plan"):

    if not subjects.strip():

        st.warning(
            "⚠️ Please enter at least one subject."
        )

    else:

        try:

            subject_list = [
                subject.strip()
                for subject in subjects.split(",")
                if subject.strip()
            ]

            plan = create_study_plan(
                subjects=subject_list,
                hours_per_day=hours_per_day,
                exam_date=str(exam_date),
            )

            st.session_state.current_plan = plan

            st.success(
                "✅ Study plan created successfully!"
            )

            display_study_plan(
                plan,
                "📚 Your Personalized Study Plan"
            )

        except Exception as e:

            st.error(
                "Unable to create the study plan."
            )

            st.code(str(e))


# ============================================================
# MODIFY STUDY PLAN
# ============================================================

if st.session_state.current_plan is not None:

    st.divider()

    st.subheader("🔄 Modify Your Study Plan")

    st.write(
        "Adjust your available study time and "
        "generate an updated plan."
    )

    current_hours = st.session_state.current_plan.get(
        "hours_per_day",
        hours_per_day,
    )

    new_hours = st.number_input(
        "New study hours per day",
        min_value=0.5,
        max_value=24.0,
        value=float(current_hours),
        step=0.5,
        key="new_hours",
    )

    if st.button("🔄 Update Study Plan"):

        try:

            updated_plan = modify_study_plan(
                st.session_state.current_plan,
                new_hours,
            )

            st.session_state.current_plan = updated_plan

            st.success(
                "✅ Study plan updated successfully!"
            )

            display_study_plan(
                updated_plan,
                "📚 Updated Study Plan"
            )

        except Exception as e:

            st.error(
                "Unable to update the study plan."
            )

            st.code(str(e))


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Based College Academic Assistant • "
    "L&T EduTech Project"
)