import json
import streamlit as st
from pathlib import Path

# ── Data Layer ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)
database = DATABASE_DIR / "database.json"

def load_data():
    if database.exists():
        content = database.read_text()
        if content.strip():
            return json.loads(content)
    return {"student": [], "teacher": []}

def save_data(data):
    with open(database, "w") as f:
        json.dump(data, f, indent=4)

def validate_email(email):
    return "@" in email and "." in email

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduCore",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], .main {
    background: #09090f !important;
    color: #e8e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(99,91,255,0.18) 0%, transparent 70%),
                radial-gradient(ellipse 50% 40% at 85% 90%, rgba(0,212,180,0.10) 0%, transparent 60%),
                #09090f !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── Main container ── */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7c6fff;
    border: 1px solid rgba(124,111,255,0.35);
    border-radius: 100px;
    padding: 0.3rem 1rem;
    margin-bottom: 1.2rem;
    background: rgba(124,111,255,0.06);
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.8rem, 5vw, 4.2rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #ffffff;
    background: linear-gradient(135deg, #ffffff 0%, #c8c5ff 50%, #7c6fff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    margin-top: 0.8rem;
    font-size: 0.95rem;
    font-weight: 400;
    color: rgba(232,232,240,0.45);
    letter-spacing: 0.01em;
}

/* ── Divider ── */
.hdivider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,111,255,0.4), transparent);
    margin: 0.5rem 0 2.5rem;
}

/* ── Tab Strip ── */
[data-testid="stHorizontalBlock"] { gap: 0 !important; }

div[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 4px !important;
    backdrop-filter: blur(12px);
    margin-bottom: 2.2rem;
}
div[data-testid="stTabs"] [role="tab"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: rgba(232,232,240,0.45) !important;
    background: transparent !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.3rem !important;
    border: none !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em;
}
div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #ffffff !important;
    background: rgba(124,111,255,0.2) !important;
    border: 1px solid rgba(124,111,255,0.35) !important;
    box-shadow: 0 0 18px rgba(124,111,255,0.15), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}

/* ── 3D Cards ── */
.card-3d {
    background: linear-gradient(145deg, rgba(255,255,255,0.055) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.085);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(20px);
    box-shadow:
        0 1px 0 rgba(255,255,255,0.06) inset,
        0 20px 60px rgba(0,0,0,0.45),
        0 4px 16px rgba(0,0,0,0.25);
    transform: perspective(800px) rotateX(0.8deg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    position: relative;
    overflow: hidden;
}
.card-3d::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}
.card-3d:hover {
    transform: perspective(800px) rotateX(0deg) translateY(-2px);
    box-shadow:
        0 1px 0 rgba(255,255,255,0.08) inset,
        0 28px 80px rgba(0,0,0,0.5),
        0 0 40px rgba(124,111,255,0.08);
}

/* ── Section Label ── */
.section-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #7c6fff;
    margin-bottom: 0.35rem;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(124,111,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(124,111,255,0.12), 0 2px 8px rgba(0,0,0,0.2) !important;
    background: rgba(124,111,255,0.06) !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stNumberInput"] input::placeholder { color: rgba(232,232,240,0.25) !important; }

/* Input labels */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label {
    color: rgba(232,232,240,0.6) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    margin-bottom: 0.3rem !important;
}

/* Number input buttons */
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e8e8f0 !important;
    border-radius: 8px !important;
}

/* ── Buttons ── */
[data-testid="stButton"] button {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.8rem !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

/* Primary button — purple */
[data-testid="stButton"]:first-of-type button,
button[kind="primary"],
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #7c6fff 0%, #5b4fd4 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 20px rgba(124,111,255,0.35), 0 1px 0 rgba(255,255,255,0.15) inset !important;
}
[data-testid="stButton"]:first-of-type button:hover {
    background: linear-gradient(135deg, #8d82ff 0%, #6b5fe4 100%) !important;
    box-shadow: 0 6px 28px rgba(124,111,255,0.5), 0 1px 0 rgba(255,255,255,0.15) inset !important;
    transform: translateY(-1px) !important;
}

/* Secondary button — ghost */
[data-testid="stButton"]:not(:first-of-type) button {
    background: rgba(255,255,255,0.05) !important;
    color: rgba(232,232,240,0.75) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
}
[data-testid="stButton"]:not(:first-of-type) button:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,0.18) !important;
}

/* ── Alert / Success / Error ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 0.85rem !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-testid="stSuccessMessage"] {
    background: rgba(0,212,130,0.1) !important;
    border: 1px solid rgba(0,212,130,0.3) !important;
    color: #00d482 !important;
    border-radius: 12px !important;
}
div[data-testid="stErrorMessage"] {
    background: rgba(255,75,75,0.1) !important;
    border: 1px solid rgba(255,75,75,0.3) !important;
    color: #ff6b6b !important;
    border-radius: 12px !important;
}
div[data-testid="stWarningMessage"] {
    background: rgba(255,190,60,0.1) !important;
    border: 1px solid rgba(255,190,60,0.3) !important;
    color: #ffbe3c !important;
    border-radius: 12px !important;
}

/* ── Stat cards ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 1px 0 rgba(255,255,255,0.06) inset;
    transform: perspective(600px) rotateX(1deg);
}
.stat-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #7c6fff;
    line-height: 1;
}
.stat-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(232,232,240,0.4);
    margin-top: 0.4rem;
}

/* ── Profile card ── */
.profile-card {
    background: linear-gradient(145deg, rgba(124,111,255,0.1), rgba(124,111,255,0.03));
    border: 1px solid rgba(124,111,255,0.25);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 40px rgba(124,111,255,0.08);
}
.profile-avatar {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #7c6fff, #00d4b4);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(124,111,255,0.4);
}
.profile-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
}
.profile-meta {
    font-size: 0.8rem;
    color: rgba(232,232,240,0.4);
    margin-top: 0.2rem;
    margin-bottom: 1.4rem;
}
.profile-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 0.85rem;
}
.profile-row:last-child { border-bottom: none; }
.profile-key { color: rgba(232,232,240,0.45); font-weight: 400; }
.profile-val { color: #e8e8f0; font-weight: 500; }

/* ── Grade badge ── */
.grade-chip {
    display: inline-block;
    background: rgba(124,111,255,0.15);
    border: 1px solid rgba(124,111,255,0.3);
    color: #a59fff;
    border-radius: 8px;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 0.15rem;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: rgba(232,232,240,0.3);
    font-size: 0.88rem;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 0.8rem; opacity: 0.5; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
}
[data-testid="stSelectbox"] label {
    color: rgba(232,232,240,0.6) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
}

/* ── Columns gap ── */
[data-testid="column"] { padding: 0 0.6rem !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child { padding-right: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,111,255,0.3); border-radius: 4px; }

</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">◈ &nbsp; Academic Management Platform</div>
    <div class="hero-title">EduCore</div>
    <div class="hero-sub">Unified student & faculty administration — clean, precise, fast.</div>
</div>
<div class="hdivider"></div>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
data = load_data()

students  = data.get("student", [])
teachers  = data.get("teacher", [])
total_stu = len(students)
total_tch = len(teachers)
graded    = sum(1 for s in students if s.get("grades"))

# ── Stats ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-val">{total_stu}</div>
        <div class="stat-label">Students</div>
    </div>
    <div class="stat-card">
        <div class="stat-val">{total_tch}</div>
        <div class="stat-label">Faculty</div>
    </div>
    <div class="stat-card">
        <div class="stat-val">{graded}</div>
        <div class="stat-label">Graded</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tabs = st.tabs(["  ＋  Register Student", "  ＋  Register Faculty", "  ✎  Assign Grades", "  ◉  Student Profile", "  ◉  Faculty Profile"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Register Student
# ════════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
    <div class="card-3d">
        <div class="section-label">Enrollment</div>
        <div class="section-title">Register New Student</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        s_name    = st.text_input("Full Name", placeholder="e.g. Arjun Mehta", key="s_name")
        s_email   = st.text_input("Email Address", placeholder="student@school.edu", key="s_email")
    with c2:
        s_age     = st.number_input("Age", min_value=5, max_value=100, value=16, key="s_age")
        s_roll    = st.text_input("Roll Number", placeholder="e.g. STU-2024-001", key="s_roll")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Register Student", key="btn_reg_stu"):
        if not all([s_name.strip(), s_email.strip(), s_roll.strip()]):
            st.error("All fields are required.")
        elif not validate_email(s_email):
            st.error("Invalid email address format.")
        elif any(s["roll_no"] == s_roll for s in students):
            st.warning(f"Roll number **{s_roll}** is already registered.")
        else:
            data["student"].append({
                "name": s_name.strip(),
                "age": int(s_age),
                "email": s_email.strip(),
                "roll_no": s_roll.strip(),
                "grades": {}
            })
            save_data(data)
            st.success(f"✓  {s_name} enrolled successfully.")
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — Register Teacher
# ════════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("""
    <div class="card-3d">
        <div class="section-label">Faculty</div>
        <div class="section-title">Register New Faculty Member</div>
    """, unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    with t1:
        t_name    = st.text_input("Full Name", placeholder="e.g. Dr. Priya Sharma", key="t_name")
        t_email   = st.text_input("Email Address", placeholder="faculty@school.edu", key="t_email")
    with t2:
        t_age     = st.number_input("Age", min_value=21, max_value=100, value=35, key="t_age")
        t_subject = st.text_input("Subject / Department", placeholder="e.g. Mathematics", key="t_subject")

    t_emp = st.text_input("Employee ID", placeholder="e.g. FAC-2024-001", key="t_emp")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Register Faculty", key="btn_reg_tch"):
        if not all([t_name.strip(), t_email.strip(), t_subject.strip(), t_emp.strip()]):
            st.error("All fields are required.")
        elif not validate_email(t_email):
            st.error("Invalid email address format.")
        elif any(t["emp_id"] == t_emp for t in teachers):
            st.warning(f"Employee ID **{t_emp}** already exists.")
        else:
            data["teacher"].append({
                "name": t_name.strip(),
                "age": int(t_age),
                "email": t_email.strip(),
                "emp_id": t_emp.strip(),
                "subject": t_subject.strip()
            })
            save_data(data)
            st.success(f"✓  {t_name} registered successfully.")
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — Add Grades
# ════════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""
    <div class="card-3d">
        <div class="section-label">Academics</div>
        <div class="section-title">Assign Subject Grades</div>
    """, unsafe_allow_html=True)

    if not students:
        st.markdown('<div class="empty-state"><div class="empty-icon">◎</div>No students registered yet.</div>', unsafe_allow_html=True)
    else:
        roll_options = {f"{s['name']}  ·  {s['roll_no']}": s["roll_no"] for s in students}
        selected_label = st.selectbox("Select Student", options=list(roll_options.keys()), key="grade_stu_sel")
        selected_roll  = roll_options[selected_label]

        g1, g2 = st.columns(2)
        with g1:
            g_subject = st.text_input("Subject", placeholder="e.g. Physics", key="g_subject")
        with g2:
            g_marks   = st.number_input("Marks (out of 100)", min_value=0.0, max_value=100.0, value=75.0, step=0.5, key="g_marks")

    st.markdown("</div>", unsafe_allow_html=True)

    if students:
        if st.button("Save Grade", key="btn_grade"):
            if not g_subject.strip():
                st.error("Subject name cannot be empty.")
            else:
                for s in data["student"]:
                    if s["roll_no"] == selected_roll:
                        if "grades" not in s:
                            s["grades"] = {}
                        s["grades"][g_subject.strip()] = float(g_marks)
                        save_data(data)
                        st.success(f"✓  Grade saved — {g_subject}: {g_marks}")
                        st.rerun()
                        break

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — Student Profile
# ════════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    if not students:
        st.markdown('<div class="empty-state"><div class="empty-icon">◎</div>No students registered yet.</div>', unsafe_allow_html=True)
    else:
        roll_map = {f"{s['name']}  ·  {s['roll_no']}": s["roll_no"] for s in students}
        sel_lbl  = st.selectbox("Select Student", options=list(roll_map.keys()), key="view_stu_sel")
        sel_roll = roll_map[sel_lbl]

        student = next((s for s in students if s["roll_no"] == sel_roll), None)
        if student:
            grades  = student.get("grades", {})
            avg     = sum(grades.values()) / len(grades) if grades else None
            initials = "".join(w[0].upper() for w in student["name"].split()[:2])

            grade_chips = "".join(
                f'<span class="grade-chip">{subj}: {mark:.0f}</span>'
                for subj, mark in grades.items()
            ) if grades else "<span style='color:rgba(232,232,240,0.3);font-size:0.82rem'>No grades yet</span>"

            avg_display = f"{avg:.1f}" if avg is not None else "—"

            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-avatar">{initials}</div>
                <div class="profile-name">{student['name']}</div>
                <div class="profile-meta">Student  ·  Roll {student['roll_no']}</div>
                <div class="profile-row">
                    <span class="profile-key">Age</span>
                    <span class="profile-val">{student['age']}</span>
                </div>
                <div class="profile-row">
                    <span class="profile-key">Email</span>
                    <span class="profile-val">{student['email']}</span>
                </div>
                <div class="profile-row">
                    <span class="profile-key">Roll Number</span>
                    <span class="profile-val">{student['roll_no']}</span>
                </div>
                <div class="profile-row">
                    <span class="profile-key">Average Score</span>
                    <span class="profile-val" style="color:#7c6fff;font-weight:700">{avg_display}</span>
                </div>
                <div class="profile-row" style="flex-direction:column;align-items:flex-start;gap:0.6rem">
                    <span class="profile-key">Grades</span>
                    <div>{grade_chips}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — Faculty Profile
# ════════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    if not teachers:
        st.markdown('<div class="empty-state"><div class="empty-icon">◎</div>No faculty registered yet.</div>', unsafe_allow_html=True)
    else:
        emp_map = {f"{t['name']}  ·  {t['emp_id']}": t["emp_id"] for t in teachers}
        sel_emp_lbl = st.selectbox("Select Faculty Member", options=list(emp_map.keys()), key="view_tch_sel")
        sel_emp_id  = emp_map[sel_emp_lbl]

        teacher = next((t for t in teachers if t["emp_id"] == sel_emp_id), None)
        if teacher:
            t_initials = "".join(w[0].upper() for w in teacher["name"].replace("Dr.", "").replace("Prof.", "").split()[:2])

            st.markdown(f"""
            <div class="profile-card">
                <div class="profile-avatar" style="background:linear-gradient(135deg,#00d4b4,#0078d4)">{t_initials}</div>
                <div class="profile-name">{teacher['name']}</div>
                <div class="profile-meta">Faculty  ·  {teacher['subject']}</div>
                <div class="profile-row">
                    <span class="profile-key">Age</span>
                    <span class="profile-val">{teacher['age']}</span>
                </div>
                <div class="profile-row">
                    <span class="profile-key">Email</span>
                    <span class="profile-val">{teacher['email']}</span>
                </div>
                <div class="profile-row">
                    <span class="profile-key">Employee ID</span>
                    <span class="profile-val">{teacher['emp_id']}</span>
                </div>
                <div class="profile-row">
                    <span class="profile-key">Department / Subject</span>
                    <span class="profile-val" style="color:#00d4b4;font-weight:600">{teacher['subject']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
