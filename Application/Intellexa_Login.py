import streamlit as st


# Hardcoded credentials (Use a secure approach in production)
USERNAME = "admin"
PASSWORD = "password123"
# WILL USE st.secrets to hide this password and username



# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    """Simple authentication function."""
    st.markdown("<h2 style='text-align: center;'>🔒 Login to Intellexa</h2>", unsafe_allow_html=True)
    st.markdown("""
        <style>
            /* Hide the entire sidebar */
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.success("✅ Login successful! Redirecting...")
            st.rerun()  # Refresh the page to reflect authentication state
        else:
            st.error("❌ Invalid credentials. Try again.")

# 🚨 Redirect to login if not authenticated
if not st.session_state["authenticated"]:
    login()
    st.stop()  # Stop execution if not logged in

st.markdown("""
    <style>
        /* Hide the entire sidebar */
        [data-testid="stSidebar"] {
            display: visible;
        }
    </style>
    """, unsafe_allow_html=True
)

# 🖼️ Display Logo
st.image("https://raw.githubusercontent.com/Happday-bot/Intellexa-TechLead/main/Application/assests/logo.png", use_container_width=True)

# 🏠 **Intellexa Login Panel**
st.markdown(
    """
    <h1 style='text-align: center; color: #2E86C1;'>🚀 Intellexa Login Panel</h1>
    <hr style='border: 1px solid #2E86C1;'>
    """,
    unsafe_allow_html=True
)

# 📌 **Overview**
st.markdown(
    """
    ### 📝 Overview  
    Intellexa is a comprehensive platform offering functionalities such as **certificate generation, email automation, and file management**.  
    This panel serves as the **main navigation hub** to access different modules.  
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# 📂 **Navigation Options**
st.markdown(
    """
    ### 🔍 Navigation Options  
    - 🔑 **Intellexa Login** – Secure login access to the Intellexa platform.  
    - 📜 **Certificate Download** – Retrieve generated certificates.  
    - 📩 **Certificate Send** – Send certificates via email automatically.  
    - 📂 **Intellexa Drive** – Manage documents and certificates.  
    - ✉️ **Mail Automation** – Automate bulk email sending.  
    - 📑 **REC OD** – Record/document management (details needed).  
    - ✅ **Todo** – Task management and pending work tracker.  
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ⚠️ **Notes Section**
st.markdown(
    """
    ### ⚠️ Important Notes  
    - 🔒 **Security**: Keep your credentials confidential.  
    - ❗ **Troubleshooting**: If you encounter issues, verify email settings and ensure the CSV format is correct.  
    """,
    unsafe_allow_html=True
)

st.markdown("<hr style='border: 1px solid #2E86C1;'>", unsafe_allow_html=True)


# Ensure session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True  # Set to True for testing

if st.session_state["authenticated"]:
    if st.sidebar.button("🔓 Logout", key="logout"):
        st.session_state["authenticated"] = False
        st.rerun()  # Refresh the page to return to login


