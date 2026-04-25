import subprocess
import sys

# Force install packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "gspread", "google-auth"])

import streamlit as st
import json
import random
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from google.oauth2.service_account import Credentials
from datetime import datetime

# ============== PAGE SETUP ==============
st.set_page_config(
    page_title="💝 Love Task",
    page_icon="💝",
    layout="centered"
)

# ============== GOOGLE SHEETS CONNECTION ==============
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource
def connect_to_sheets():
    """Connect to Google Sheets using secrets"""
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(st.secrets["sheet_name"]).sheet1
    return sheet

def load_tasks_from_sheet(sheet):
    """Load all tasks from Google Sheet"""
    records = sheet.get_all_records()
    tasks = []
    for r in records:
        tasks.append({
            "name": r.get("name", ""),
            "priority": r.get("priority", "⭐ Important"),
            "done": str(r.get("done", "False")) == "True",
            "date": r.get("date", ""),
        })
    return tasks

def save_tasks_to_sheet(sheet, tasks):
    """Save all tasks to Google Sheet (rewrite entire sheet)"""
    sheet.clear()
    sheet.append_row(["name", "priority", "done", "date"])
    for task in tasks:
        sheet.append_row([
            task["name"],
            task["priority"],
            str(task["done"]),
            task["date"],
        ])

# Connect to sheet
try:
    sheet = connect_to_sheets()
except Exception as e:
    st.error(f"Could not connect to database: {e}")
    st.stop()

# ============== CUTE MESSAGES ==============
completion_messages = [
    "Yay! You did it! You're amazing! 🎉",
    "Task CRUSHED! You're literally the best 💪",
    "Done! Now come get your kiss 💋",
    "Look at you being all productive and handsome 😍",
    "Another one done! You're on fire today 🔥",
    "Wow, is it hot in here or is it just your productivity? 😏",
    "Task complete! You deserve a snack break 🍕",
    "BOOM! Done! I'm so proud of you 🥺",
    "Finished! You're my favorite human ❤️",
    "That's my man! Getting stuff DONE! 👑",
    "Completed! Now flex for me 💪😂",
    "Done! One step closer to world domination 🌍",
]

nag_messages = [
    "Heyyyy... you still haven't done this 👀",
    "This task is getting lonely... finish it! 😢",
    "Babe... this has been here for a while 😂",
    "I'm not saying I'm judging you... but 👀",
    "This task called. It misses being completed 📞",
    "Tick tock... this task is waiting for its hero 🦸",
]

love_notes = [
    "I just wanted to say... I love you! 💝",
    "You're the best thing that ever happened to me 🥺",
    "Hey handsome, don't forget to drink water! 💧",
    "I believe in you! You can do ANYTHING! 🚀",
    "Just thinking about you makes me smile 😊",
    "You + Me = ❤️ (that's the only math I like)",
    "I'm so lucky to have you 🍀",
    "You make my heart go 💓💓💓",
    "Plot twist: You're amazing and everyone knows it 👑",
    "Sending you a virtual hug right now 🤗",
]

welcome_messages = [
    "Welcome back, handsome! 💝",
    "Hey good looking, ready to be productive? 😘",
    "My favorite person is here! Let's get stuff done! 🚀",
    "Welcome! You look extra cute today 😍",
    "The productivity king has arrived! 👑",
]

PRIORITY_MAP = {
    "🔥 URGENT": "🔥",
    "⭐ Important": "⭐",
    "🌙 Chill": "🌙",
}

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks_from_sheet(sheet)

if "message" not in st.session_state:
    st.session_state.message = ""

if "welcome" not in st.session_state:
    st.session_state.welcome = random.choice(welcome_messages)

# ============== CUSTOM STYLING ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ff6b6b, #ee5a24, #f0932b, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        font-family: 'Quicksand', sans-serif;
    }
    
    .subtitle {
        text-align: center;
        color: #a29bfe;
        font-size: 1.2rem;
        margin-top: 0;
        font-family: 'Quicksand', sans-serif;
    }
    
    .welcome-msg {
        text-align: center;
        font-size: 1.3rem;
        color: #fd79a8;
        padding: 10px;
        font-family: 'Quicksand', sans-serif;
    }
    
    .task-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 15px 20px;
        margin: 8px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        color: white;
    }
    
    .task-card:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateX(5px);
        border-color: #fd79a8;
    }
    
    .cute-message {
        background: linear-gradient(135deg, #fd79a8, #e84393);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        font-size: 1.2rem;
        color: white;
        margin: 15px 0;
        font-family: 'Quicksand', sans-serif;
    }
    
    .nag-message {
        background: linear-gradient(135deg, #a29bfe, #6c5ce7);
        border-radius: 15px;
        padding: 15px 20px;
        margin: 8px 0;
        color: white;
        font-family: 'Quicksand', sans-serif;
    }
    
    .love-note {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        font-size: 1.4rem;
        color: white;
        margin: 20px 0;
        font-family: 'Quicksand', sans-serif;
        box-shadow: 0 10px 30px rgba(238, 90, 36, 0.3);
    }
    
    .progress-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        text-align: center;
        color: white;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Quicksand', sans-serif;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 10px;
        font-family: 'Quicksand', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# ============== HEADER ==============
st.markdown('<p class="main-title">💝 Love Task 💝</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Cute To-Do List</p>', unsafe_allow_html=True)
st.markdown(f'<p class="welcome-msg">{st.session_state.welcome}</p>', unsafe_allow_html=True)

# ============== SHOW MESSAGE ==============
if st.session_state.message:
    st.markdown(f'<div class="cute-message">{st.session_state.message}</div>', unsafe_allow_html=True)
    st.session_state.message = ""

# ============== REFRESH BUTTON ==============
col_refresh, col_empty = st.columns([1, 3])
with col_refresh:
    if st.button("🔄 Refresh Tasks"):
        st.session_state.tasks = load_tasks_from_sheet(sheet)
        st.rerun()

# ============== PROGRESS BAR ==============
tasks = st.session_state.tasks
total = len(tasks)
done = sum(1 for t in tasks if t["done"])

if total > 0:
    percentage = done / total
    
    if percentage == 1.0:
        progress_msg = "ALL DONE! You're incredible! 🏆"
        progress_color = "#00b894"
    elif percentage >= 0.75:
        progress_msg = "Almost there, baby! 💪"
        progress_color = "#00b894"
    elif percentage >= 0.5:
        progress_msg = "Halfway! Keep going! 🚀"
        progress_color = "#fdcb6e"
    elif percentage >= 0.25:
        progress_msg = "Good start! You got this! ⭐"
        progress_color = "#fdcb6e"
    else:
        progress_msg = "Let's get to work, handsome! 😘"
        progress_color = "#ff7675"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="progress-section"><span class="stats-number" style="color: #74b9ff;">{total}</span><br><span style="color:white;">Total Tasks</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="progress-section"><span class="stats-number" style="color: #00b894;">{done}</span><br><span style="color:white;">Completed</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="progress-section"><span class="stats-number" style="color: #ff7675;">{total - done}</span><br><span style="color:white;">Remaining</span></div>', unsafe_allow_html=True)
    
    st.progress(percentage)
    st.markdown(f'<p style="text-align:center; color:{progress_color}; font-size:1.1rem;">{progress_msg}</p>', unsafe_allow_html=True)

# ============== TABS ==============
tab1, tab2, tab3, tab4 = st.tabs(["📋 Tasks", "➕ Add Task", "😂 Nag Mode", "💌 Love Note"])

# ============== TAB 1: SHOW TASKS ==============
with tab1:
    if not tasks:
        st.markdown("""
        <div style="text-align:center; padding:40px; color:#a29bfe; font-size:1.2rem;">
            No tasks yet! Add some and get productive! ✨
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, task in enumerate(tasks):
            priority_icon = PRIORITY_MAP.get(task["priority"], "⭐")
            
            col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
            
            with col1:
                status = "✅" if task["done"] else "⬜"
                style = "opacity:0.5;" if task["done"] else ""
                task_name = f"<s>{task['name']}</s>" if task["done"] else task["name"]
                st.markdown(
                    f'<div class="task-card" style="{style}">'
                    f'{status} {priority_icon} <strong style="color:white;">{task_name}</strong>'
                    f'<br><small style="color:#b2bec3;">{task.get("date", "")}</small>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            with col2:
                if not task["done"]:
                    if st.button("✅ Done", key=f"done_{i}"):
                        st.session_state.tasks[i]["done"] = True
                        save_tasks_to_sheet(sheet, st.session_state.tasks)
                        st.session_state.message = random.choice(completion_messages)
                        st.rerun()
            
            with col3:
                if st.button("🗑️ Delete", key=f"del_{i}"):
                    st.session_state.tasks.pop(i)
                    save_tasks_to_sheet(sheet, st.session_state.tasks)
                    st.rerun()

# ============== TAB 2: ADD TASK ==============
with tab2:
    st.markdown("### ✍️ What needs to be done?")
    
    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("📝 Task name", placeholder="e.g., Buy me flowers 💐")
        task_priority = st.radio(
            "Priority level",
            ["🔥 URGENT", "⭐ Important", "🌙 Chill"],
            index=1,
            horizontal=True,
        )
        
        submitted = st.form_submit_button("➕ Add Task!", use_container_width=True)
        
        if submitted and task_name.strip():
            new_task = {
                "name": task_name.strip(),
                "priority": task_priority,
                "done": False,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            }
            st.session_state.tasks.append(new_task)
            save_tasks_to_sheet(sheet, st.session_state.tasks)
            st.session_state.message = f"✅ Added: '{task_name}' — You got this, babe! 💪"
            st.rerun()
        elif submitted:
            st.warning("Task can't be empty, silly! 😜")

# ============== TAB 3: NAG MODE ==============
with tab3:
    pending = [t for t in tasks if not t["done"]]
    
    if st.button("😂 ACTIVATE NAG MODE", use_container_width=True):
        if not pending:
            st.markdown("""
            <div class="cute-message">
                Nothing to nag about! You're perfect! 💯
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### 📢 NAG MODE ACTIVATED!")
            for task in pending:
                nag = random.choice(nag_messages)
                st.markdown(
                    f'<div class="nag-message">'
                    f'<strong>📢 {task["name"]}</strong><br>'
                    f'→ {nag}'
                    f'</div>',
                    unsafe_allow_html=True
                )

# ============== TAB 4: LOVE NOTE ==============
with tab4:
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <p style="color:#a29bfe; font-size:1.1rem;">Click the button for a surprise message 💝</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💌 Get a Love Note", use_container_width=True):
        note = random.choice(love_notes)
        st.markdown(f'<div class="love-note">{note}</div>', unsafe_allow_html=True)
        st.balloons()

# ============== FOOTER ==============
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#dfe6e9; font-size:0.9rem;">'
    'Made with 💝 by your girlfriend'
    '</p>',
    unsafe_allow_html=True
)
