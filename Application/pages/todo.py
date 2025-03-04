
#This file is decrepated will update with use of google sheet as database

import streamlit as st
import json
import os
from Intellexa_Login import login

# Redirect to login if not authenticated
if not st.session_state.get("authenticated", False):
    login()
    st.stop()

# File to store tasks
TODO_FILE = "todos.json"
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
    "rakhul"
    "keerthana"


]  # Default list of names

# Load existing tasks
def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_todos(todos):
    with open(TODO_FILE, "w") as file:
        json.dump(todos, file, indent=4)

# Initialize todos
todos = load_todos()

# Streamlit UI
st.set_page_config(page_title="To-Do List", page_icon="✅", layout="centered")
st.title("✅ Interactive To-Do List")

# Custom CSS for alignment
st.markdown("""
    <style>
        .stCheckbox {margin-top: 10px;}
        .stButton button {background-color: #A7C7E7; color: black; border-radius: 5px;}
        .delete-btn button {background-color: #ff006e !important; color: white; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# Input field for new tasks
new_task = st.text_input("Add a new task:", label_visibility="collapsed")
assigned_to = st.multiselect("Assign to:", NAMES)

col_add, _ = st.columns([0.3, 0.7])
with col_add:
    if st.button("➕ **Add Task**"):
        if new_task.strip() and assigned_to:
            todos.append({"task": new_task.strip(), "completed": False, "assigned_to": assigned_to})
            save_todos(todos)
            st.rerun()

# Display tasks
st.markdown("### 📌 Your Tasks:")

if not todos:
    st.info("No tasks added yet!")

for i, todo in enumerate(todos):
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

    with col1:
        checked = st.checkbox("completed ?", value=todo["completed"], key=f"chk_{i}", label_visibility="collapsed")
        if checked != todo["completed"]:  # Ensure change is saved before rerunning
            todos[i]["completed"] = checked
            save_todos(todos)
            st.rerun()

    with col2:
        task_text = f"~~{todo['task']}~~" if todo["completed"] else todo["task"]
        assigned_text = f"👤 Assigned to: {', '.join(todo['assigned_to'])}"
        st.markdown(f"<p style='margin-top:8px;'>{task_text}</p>", unsafe_allow_html=True)
        st.caption(assigned_text)

    with col3:
        if st.button("❌", key=f"del_{i}"):
            todos = [t for j, t in enumerate(todos) if j != i]  # Prevent index shifting
            save_todos(todos)
            st.rerun()

# Button to remove completed tasks
if any(todo.get("completed", False) for todo in todos):  
    if st.button("🗑️ **Remove Completed Tasks**"):
        todos = [todo for todo in todos if not todo["completed"]]
        save_todos(todos)
        st.rerun()

# Footer
st.markdown("---")
st.caption("With great power comes great responsibility")



# Ensure session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True  # Set to True for testing

if st.session_state["authenticated"]:
    if st.sidebar.button("🔓 Logout", key="logout"):
        st.session_state["authenticated"] = False
        st.rerun()  # Refresh the page to return to login
