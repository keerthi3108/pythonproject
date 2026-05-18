"""
StudyAI — Study Question Generator.
"""

import streamlit as st

from auth import init_session_state
from components import (
    inject_css,
    render_auth_screen,
    render_dashboard,
    render_saved_page,
    render_sidebar,
)
from ui_styles import APP_CSS

st.set_page_config(
    page_title="StudyAI — Question Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    inject_css(APP_CSS)
    init_session_state()

    if st.session_state.authenticated:
        render_sidebar()
        if st.session_state.page == "saved":
            render_saved_page()
        else:
            render_dashboard()
    else:
        render_auth_screen()


if __name__ == "__main__":
    main()
