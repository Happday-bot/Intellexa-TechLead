import streamlit as st
import json
import requests
import base64
from Intellexa_Login import login

# GitHub Configuration
GITHUB_TOKEN = "_____________________________"
REPO_OWNER = "______________________________"
REPO_NAME = "_______________________________"
FILE_PATH = "_______________________________"

# GitHub API URL
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Authentication
if not st.session_state.get("authenticated", False):
    login()
    st.stop()

# Load To-Dos from GitHub
def load_todos():
    response = requests.get(GITHUB_API_URL, headers=HEADERS)
    if response.status_code == 200:
        content = response.json()
        decoded_content = base64.b64decode(content["content"]).decode("utf-8")
        return json.loads(decoded_content), content["sha"]
    return [], None  # Return empty list if file not found

# Save To-Dos back to GitHub
def save_todos(todos, sha):
    encoded_content = base64.b64encode(json.dumps(todos, indent=4).encode("utf-8")).decode("utf-8")
    commit_message = "Updated To-Do List"
    
    data = {
        "message": commit_message,
        "content": encoded_content,
        "sha": sha
    }
    
    response = requests.put(GITHUB_API_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        st.success("✅ Changes saved to GitHub!")
    else:
        st.error("⚠️ Failed to update GitHub!")

# Fetch Todos
todos, sha = load_todos()

# Streamlit UI
st.set_page_config(page_title="To-Do List", page_icon="✅", layout="centered")
st.title("✅ Interactive To-Do List")

# Task Input
new_task = st.text_input("Add a new task:")


NAMES = [   
    "Media Team",
    "Event Team",
    "Content Team",
    "PR Team",
    "Design Team",
    "Buisness Communication",
    "Creative Team",
    "IOT Team",
    "App dev Team",
    "Algoritm Team",
    "AI Team",
    "Backend Team",
    "Kumaran", "Maria", "kabilesh", "krithika", "Pragatheesh",
    "Pugazhendhi", "Janani", "roshini", "sujitha",
    "shivani",
    "Nandhini", "Prinkayatthra", "padmapriya",
    "hareesh", "madhan", "kaarunya", "aadithya", "Lakshmi bhargavi",
    "jayakanth", "Ganesh kumar",
    "swetha", "vishnupriya", "dhivya shree",
    "joderick Sherwin", "yudeeswaran", "Alfred sam",
    "avinash", "shangamitra",
    "bharathraj", "Fareed Ahamed", "Jagadeshwaran",
    "daksh", "shanmuga priya",
    "Jeffrin", "prasanth",
    "saiviswaram", "surweesh",
    "shanthosh",
    "sivaraman",
    "rakhul",
    "keerthana"


 ] 

assigned_to = st.multiselect("Assign to:", NAMES)
assigned_to = ", ".join(assigned_to)

if st.button("➕ **Add Task**"):
    if new_task.strip() and assigned_to.strip():
        todos.append({"task": new_task.strip(), "completed": False, "assigned_to": assigned_to.split(",")})
        save_todos(todos, sha)
        st.rerun()

# Display Tasks
st.markdown("### 📌 Your Tasks:")
if not todos:
    st.info("No tasks added yet!")

for i, todo in enumerate(todos):
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

    with col1:
        checked = st.checkbox("✅", value=todo["completed"], key=f"chk_{i}")
        if checked != todo["completed"]:
            todos[i]["completed"] = checked
            save_todos(todos, sha)
            st.rerun()

    with col2:
        task_text = f"~~{todo['task']}~~" if todo["completed"] else todo["task"]
        st.markdown(f"<p>{task_text}</p>", unsafe_allow_html=True)
        st.caption(f"👤 Assigned to: {', '.join(todo['assigned_to'])}")

    with col3:
        if st.button("❌", key=f"del_{i}"):
            todos.pop(i)
            save_todos(todos, sha)
            st.rerun()

# Remove Completed Tasks
if any(todo.get("completed", False) for todo in todos):
    if st.button("🗑️ **Remove Completed Tasks**"):
        todos = [todo for todo in todos if not todo["completed"]]
        save_todos(todos, sha)
        st.rerun()

st.markdown("---")
st.caption("With great power comes great responsibility")

# Logout Button
if st.sidebar.button("🔓 Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
