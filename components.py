"""
Reusable UI components for StudyAI.
"""

import html
from datetime import datetime

import streamlit as st

from auth import bump_stats, login_user, logout, register_user
from local_generator import generate_local_questions
from ui_helpers import copy_button
from utils import format_questions_for_export, format_single_question


def inject_css(css: str) -> None:
    st.markdown(css, unsafe_allow_html=True)


def render_navbar(title: str, subtitle: str = "") -> None:
    sub_html = f'<div class="tagline">{html.escape(subtitle)}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="app-navbar">
            <div>
                <div class="brand">{html.escape(title)}</div>
                {sub_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    username = st.session_state.username or "User"
    topics_count = len(st.session_state.history)
    questions_count = st.session_state.total_questions_count

    with st.sidebar:
        st.markdown(
            f"""
            <div class="profile-glass">
                <div class="avatar">👤</div>
                <div class="uname">{html.escape(username)}</div>
                <span class="status"><span class="status-dot"></span> Active</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="stat-box"><div class="num">{topics_count}</div>'
                f'<div class="lbl">Topics</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="stat-box"><div class="num">{questions_count}</div>'
                f'<div class="lbl">Questions</div></div>',
                unsafe_allow_html=True,
            )

        if st.button("🚪 Log out", use_container_width=True):
            logout()

        st.markdown('<p class="section-title">Navigation</p>', unsafe_allow_html=True)
        nav = st.radio(
            "Page",
            ["🏠 Dashboard", "💾 Saved"],
            label_visibility="collapsed",
            key="sidebar_nav",
        )
        page = "dashboard" if "Dashboard" in nav else "saved"
        st.session_state.page = page

        st.markdown('<p class="section-title">Topic history</p>', unsafe_allow_html=True)
        if not st.session_state.history:
            st.caption("No topics yet.")
        else:
            for t in reversed(st.session_state.history[-6:]):
                st.markdown(
                    f'<div class="history-chip">📌 {html.escape(t)}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.caption("StudyAI v2.0")

    return page


def _password_field(label: str, key: str, show_key: str) -> str:
    show = st.checkbox("Show password", key=show_key, value=False)
    return st.text_input(
        label,
        type="default" if show else "password",
        key=key,
        placeholder="••••••••",
    )


def render_auth_screen() -> None:
    render_navbar("🧠 StudyAI", "Smart study question generator")

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        tab_login, tab_signup = st.tabs(["🔐 Login", "✨ Sign Up"])

        with tab_login:
            st.subheader("Welcome back")
            u = st.text_input("Username", key="login_user", placeholder="your_username")
            p = _password_field("Password", "login_pass", "show_login")
            if st.button("Log in", type="primary", use_container_width=True):
                if not u.strip() or not p:
                    st.warning("Please enter username and password.")
                else:
                    ok, msg = login_user(u, p)
                    if ok:
                        st.session_state.authenticated = True
                        st.session_state.username = u.strip()
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

        with tab_signup:
            st.subheader("Create account")
            ru = st.text_input("Username", key="reg_user", placeholder="3–20 chars, a-z 0-9 _")
            rp = _password_field("Password", "reg_pass", "show_reg")
            rc = _password_field("Confirm password", "reg_confirm", "show_reg_confirm")
            if st.button("Sign up", type="primary", use_container_width=True):
                if not ru.strip() or not rp or not rc:
                    st.warning("Please fill in all fields.")
                elif rp != rc:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register_user(ru, rp)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)


def render_question_card(index: int, question: dict, key_prefix: str) -> None:
    q_text = html.escape(str(question.get("question", "N/A")))
    options = question.get("options") or []
    opts_html = ""
    if options:
        opts_html = "".join(
            f'<div class="q-opt"><strong>{chr(65 + j)}.</strong> {html.escape(str(opt))}</div>'
            for j, opt in enumerate(options)
        )

    st.markdown(
        f"""
        <div class="q-card">
            <div class="q-badge">Question {index}</div>
            <div class="q-title">{q_text}</div>
            {opts_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📖 Answer & explanation", expanded=False):
        st.markdown(f"**Correct answer:** {question.get('correct_answer', 'N/A')}")
        st.markdown(f"**Explanation:** {question.get('explanation', 'N/A')}")

    copy_button(
        "📋 Copy this question",
        format_single_question(index, question),
        key=f"{key_prefix}_copy_{index}",
        use_container_width=True,
    )


def execute_generation(topic: str, difficulty: str, num_q: int, q_type: str) -> bool:
    st.session_state.gen_error = None
    st.session_state.gen_success = None

    with st.status("📚 Generating study questions…", expanded=True) as status:
        st.write(f"Topic: **{topic}** · {difficulty} · {q_type} · {num_q} questions")
        questions = generate_local_questions(topic, difficulty, num_q, q_type)
        status.update(label=f"Ready — {len(questions)} questions", state="complete")

    st.session_state.generated_questions = questions
    st.session_state.current_topic = topic
    st.session_state.current_difficulty = difficulty
    st.session_state.current_q_type = q_type
    st.session_state.last_topic = topic
    st.session_state.last_difficulty = difficulty
    st.session_state.last_num_questions = num_q
    st.session_state.last_q_type = q_type

    bump_stats(len(questions), topic)
    st.session_state.saved_generations.append(
        {
            "topic": topic,
            "difficulty": difficulty,
            "q_type": q_type,
            "questions": questions,
            "time": datetime.now().strftime("%H:%M:%S"),
        }
    )
    st.session_state.saved_generations = st.session_state.saved_generations[-5:]
    st.session_state.gen_success = f"Generated {len(questions)} questions!"
    return True


def render_results_section() -> None:
    questions = st.session_state.generated_questions
    if not questions:
        return

    topic = st.session_state.current_topic
    difficulty = st.session_state.current_difficulty
    q_type = st.session_state.current_q_type
    export_text = format_questions_for_export(questions, topic, difficulty, q_type)

    st.divider()
    st.subheader("📋 Generated questions")
    st.markdown(
        f'<div class="pill-row">'
        f'<span>📖 {html.escape(topic)}</span>'
        f'<span>{html.escape(difficulty)}</span>'
        f'<span>{html.escape(q_type)}</span>'
        f'<span>{len(questions)} Qs</span></div>',
        unsafe_allow_html=True,
    )

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.download_button(
            "📥 Download all",
            export_text,
            file_name=f"{topic.replace(' ', '_')}_questions.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with b2:
        copy_button("📋 Copy all", export_text, key="copy_all_main", use_container_width=True)
    with b3:
        if st.button("🔄 Generate again", use_container_width=True):
            st.session_state.pending_generate = True
            st.rerun()
    with b4:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.generated_questions = None
            st.session_state.current_topic = ""
            st.session_state.gen_success = None
            st.rerun()

    for i, q in enumerate(questions, start=1):
        render_question_card(i, q, "main")


def render_dashboard() -> None:
    render_navbar("🚀 Question Generator", f"Hello, {st.session_state.username}")

    if st.session_state.gen_error:
        st.error(st.session_state.gen_error)
    if st.session_state.gen_success:
        st.success(st.session_state.gen_success)

    if st.session_state.pending_generate:
        st.session_state.pending_generate = False
        execute_generation(
            st.session_state.last_topic,
            st.session_state.last_difficulty,
            st.session_state.last_num_questions,
            st.session_state.last_q_type,
        )
        st.rerun()

    with st.form("generator_form", clear_on_submit=False):
        st.markdown("**Configure your study set**")
        c1, c2 = st.columns([2, 1])
        with c1:
            topic = st.text_input(
                "Topic",
                value=st.session_state.last_topic,
                placeholder="e.g. Photosynthesis, Java loops",
            )
        with c2:
            difficulty = st.selectbox(
                "Difficulty",
                ["Easy", "Medium", "Hard"],
                index=["Easy", "Medium", "Hard"].index(
                    st.session_state.last_difficulty
                    if st.session_state.last_difficulty in ["Easy", "Medium", "Hard"]
                    else "Medium"
                ),
            )
        c3, c4 = st.columns(2)
        with c3:
            num_q = st.number_input(
                "Number of questions",
                min_value=1,
                max_value=20,
                value=min(int(st.session_state.last_num_questions), 5),
                help="Generate up to 20 questions per topic.",
            )
        with c4:
            q_type = st.selectbox(
                "Question type",
                ["MCQs", "Short Answers", "True/False"],
                index=["MCQs", "Short Answers", "True/False"].index(
                    st.session_state.last_q_type
                    if st.session_state.last_q_type in ["MCQs", "Short Answers", "True/False"]
                    else "MCQs"
                ),
            )

        fc1, fc2 = st.columns(2)
        with fc1:
            submitted = st.form_submit_button("✨ Generate", type="primary", use_container_width=True)
        with fc2:
            cleared = st.form_submit_button("Clear results", use_container_width=True)

    if cleared:
        st.session_state.generated_questions = None
        st.session_state.current_topic = ""
        st.session_state.gen_error = None
        st.session_state.gen_success = None
        st.info("Results cleared.")
        st.rerun()

    if submitted:
        topic_clean = (topic or "").strip()
        if not topic_clean:
            st.warning("Please enter a topic.")
        elif num_q < 1 or num_q > 20:
            st.warning("Number of questions must be between 1 and 20.")
        else:
            execute_generation(topic_clean, difficulty, int(num_q), q_type)
            st.rerun()

    render_results_section()


def render_saved_page() -> None:
    render_navbar("💾 Saved this session", "Your last 5 generations")
    saved = st.session_state.saved_generations
    if not saved:
        st.info("Nothing saved yet. Generate questions from the Dashboard.")
        return

    for idx, entry in enumerate(reversed(saved)):
        label = f"{entry['topic']} · {entry['difficulty']} · {entry['q_type']} · {entry['time']}"
        with st.expander(label, expanded=(idx == 0)):
            export_text = format_questions_for_export(
                entry["questions"], entry["topic"], entry["difficulty"], entry["q_type"]
            )
            d1, d2 = st.columns(2)
            with d1:
                st.download_button(
                    "📥 Download",
                    export_text,
                    file_name=f"{entry['topic'].replace(' ', '_')}_saved.txt",
                    key=f"saved_dl_{idx}",
                    use_container_width=True,
                )
            with d2:
                copy_button("📋 Copy all", export_text, key=f"saved_cp_{idx}", use_container_width=True)
            for i, q in enumerate(entry["questions"], start=1):
                render_question_card(i, q, f"saved_{idx}")
