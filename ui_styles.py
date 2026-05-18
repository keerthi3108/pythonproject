"""Global CSS for StudyAI — injected once per run."""

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(165deg, #08090d 0%, #10131c 50%, #0c0e14 100%);
    font-family: 'Inter', system-ui, sans-serif;
}

#MainMenu, footer, header { visibility: hidden; height: 0; }

/* Top navbar */
.app-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 1.25rem;
    margin: -1rem -1rem 1.25rem -1rem;
    background: rgba(15, 17, 26, 0.75);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 0 0 14px 14px;
}
.app-navbar .brand {
    font-size: 1.35rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-navbar .tagline {
    color: #6b7280;
    font-size: 0.8rem;
    margin-top: 2px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c0e14 0%, #141824 100%) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.12);
}
[data-testid="stSidebar"] .block-container { padding-top: 1rem; }

.profile-glass {
    background: rgba(99, 102, 241, 0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(129, 140, 248, 0.22);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}
.profile-glass .avatar { font-size: 2rem; line-height: 1; }
.profile-glass .uname {
    color: #f3f4f6;
    font-weight: 700;
    font-size: 1.05rem;
    margin: 0.35rem 0 0.25rem;
}
.profile-glass .status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    color: #34d399;
    font-weight: 600;
}
.profile-glass .status-dot {
    width: 7px; height: 7px;
    background: #34d399;
    border-radius: 50%;
    box-shadow: 0 0 8px #34d399;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.45; }
}

.stat-box {
    background: rgba(30, 33, 45, 0.6);
    border: 1px solid #2d303a;
    border-radius: 10px;
    padding: 0.65rem 0.75rem;
    margin-bottom: 0.5rem;
    text-align: center;
}
.stat-box .num {
    color: #a5b4fc;
    font-size: 1.35rem;
    font-weight: 800;
}
.stat-box .lbl {
    color: #6b7280;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.section-title {
    color: #9ca3af;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0.75rem 0 0.4rem;
}

.history-chip {
    color: #d1d5db;
    font-size: 0.82rem;
    padding: 0.35rem 0.5rem;
    margin: 0.2rem 0;
    border-left: 2px solid #6366f1;
    padding-left: 0.55rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.45) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(45, 48, 58, 0.9) !important;
    box-shadow: none !important;
}

/* Form fields */
.stTextInput input, .stNumberInput input, .stSelectbox > div > div {
    background: rgba(30, 33, 45, 0.85) !important;
    border: 1px solid #3f4454 !important;
    border-radius: 8px !important;
    color: #f3f4f6 !important;
}
.stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
}

/* Question cards */
.q-card {
    background: linear-gradient(145deg, rgba(26,29,40,0.95), rgba(18,20,28,0.98));
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    transition: transform 0.2s, border-color 0.2s;
}
.q-card:hover {
    transform: translateY(-2px);
    border-color: rgba(129, 140, 248, 0.4);
}
.q-card .q-badge {
    color: #818cf8;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.q-card .q-title {
    color: #f9fafb;
    font-size: 1rem;
    font-weight: 600;
    margin: 0.45rem 0 0.65rem;
    line-height: 1.5;
}
.q-card .q-opt {
    color: #d1d5db;
    font-size: 0.9rem;
    padding: 0.2rem 0;
}

.pill-row span {
    display: inline-block;
    background: rgba(99,102,241,0.12);
    color: #a5b4fc;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 0.4rem;
    margin-bottom: 0.35rem;
}

div[data-testid="stExpander"] {
    background: rgba(24, 27, 38, 0.9);
    border: 1px solid #2d303a;
    border-radius: 10px;
}

div[data-testid="stStatusWidget"] {
    border-radius: 12px;
}
</style>
"""
