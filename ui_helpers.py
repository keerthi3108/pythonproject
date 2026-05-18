"""
UI helpers compatible with all Streamlit versions used in this project.
"""

import json

import streamlit as st
import streamlit.components.v1 as components


def copy_button(
    label: str,
    text: str,
    key: str | None = None,
    use_container_width: bool = False,
) -> None:
    """Copy-to-clipboard via HTML/JS (works on Streamlit 1.52+)."""
    btn_id = key or "copy_btn"
    width = "100%" if use_container_width else "auto"
    safe_label = json.dumps(label)
    safe_text = json.dumps(text)

    components.html(
        f"""
        <button id="{btn_id}" style="
            width: {width};
            padding: 0.5rem 1rem;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            font-weight: 600;
            font-family: Inter, system-ui, sans-serif;
            font-size: 0.9rem;
            color: white;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
            transition: transform 0.2s, box-shadow 0.2s;
        "
        onmouseover="this.style.transform='translateY(-1px)'"
        onmouseout="this.style.transform='translateY(0)'"
        onclick="
            navigator.clipboard.writeText({safe_text}).then(function() {{
                var b = document.getElementById('{btn_id}');
                var orig = {safe_label};
                b.textContent = '✓ Copied!';
                setTimeout(function() {{ b.textContent = orig; }}, 1500);
            }}).catch(function() {{
                alert('Copy failed. Select text manually from the app.');
            }});
        ">
        {label}
        </button>
        """,
        height=48,
    )
