import time
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from Intellexa_Login import login

# Redirect to login if not authenticated
if not st.session_state.get("authenticated", False):
    login()
    st.stop()

# Load credentials securely from Streamlit Secrets
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
creds_dict = dict(st.secrets["google"])
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Initialize Google Drive API
drive_service = build("drive", "v3", credentials=creds)

# Rate-limiting function to prevent excessive API calls
def api_request(func, *args, **kwargs):
    time.sleep(0.5)  # Prevents API abuse
    return func(*args, **kwargs)

# Function to fetch all files with secure webViewLink
def get_all_files():
    query = "trashed=false"
    results = api_request(
        drive_service.files().list,
        q=query,
        fields="files(id, name, parents, mimeType, webViewLink)"
    ).execute()
    return results.get("files", [])

# Function to fetch only folders
def get_folders():
    query = "mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = api_request(
        drive_service.files().list,
        q=query,
        fields="files(id, name, webViewLink)"
    ).execute()
    return results.get("files", [])

# Streamlit UI
st.title("🔐 Secure Google Drive File Manager")

# Get folders and files
folders = get_folders()
files = get_all_files()

# Categorize files into folders and standalone files
folder_contents = {folder["id"]: [] for folder in folders}
standalone_files = []

for file in files:
    if file["mimeType"] == "application/vnd.google-apps.folder":
        continue  # Skip folders in standalone files
    if "parents" in file:
        parent_id = file["parents"][0]  # Assuming a single parent folder
        if parent_id in folder_contents:
            folder_contents[parent_id].append(file)
        else:
            standalone_files.append(file)
    else:
        standalone_files.append(file)

# Display folders and their files securely
st.subheader("📁 Secure Folders")
if folders:
    for folder in folders:

        folder_url = folder.get("webViewLink", "#")
        folder_name = folder["name"]

        with st.expander(f"📂 {folder['name']}"):

            st.markdown(f"🔗 **[Open Folder in Drive]({folder_url})**", unsafe_allow_html=True)
            
            if folder_contents[folder["id"]]:
                for file in folder_contents[folder["id"]]:
                    file_url = file.get("webViewLink", "#")  # Secure Drive link
                    st.markdown(f"📄 **[{file['name']}]({file_url})**", unsafe_allow_html=True)
            else:
                st.write("No files in this folder.")
else:
    st.write("No folders found.")

# Display standalone files securely
st.subheader("📄 Secure Standalone Files")
if standalone_files:
    for file in standalone_files:
        file_url = file.get("webViewLink", "#")
        st.markdown(f"📄 **[{file['name']}]({file_url})**", unsafe_allow_html=True)
else:
    st.write("No standalone files found.")


# Ensure session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True  # Set to True for testing

if st.session_state["authenticated"]:
    if st.sidebar.button("🔓 Logout", key="logout"):
        st.session_state["authenticated"] = False
        st.rerun()  # Refresh the page to return to login