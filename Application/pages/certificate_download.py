# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw, ImageFont
# import zipfile
# import io

# from Intellexa_Login import login

# # Redirect to login if not authenticated
# if not st.session_state.get("authenticated", False):
#     login()
#     st.stop()

# def add_text_to_certificate(image, name, college, events, positions, font):
#     draw = ImageDraw.Draw(image)
#     font_name = font if font else ImageFont.load_default()
#     font_college = font if font else ImageFont.load_default()
#     font_events = font if font else ImageFont.load_default()

#     draw.text(positions["name"], name, fill="black", font=font_name)
#     draw.text(positions["college"], college, fill="black", font=font_college)
#     draw.text(positions["events"], events, fill="black", font=font_events)

#     return image

# def generate_certificates(template, csv_data, positions, font, file_type):
#     df = pd.read_csv(csv_data)
#     zip_buffer = io.BytesIO()

#     with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for index, row in df.iterrows():
#             image = template.copy()
#             cert = add_text_to_certificate(image, row['Name'], row['College'], row['Events'], positions, font)
#             img_buffer = io.BytesIO()
#             cert.save(img_buffer, format=file_type.upper())
#             zipf.writestr(f"certificate_{index+1}.{file_type}", img_buffer.getvalue())
    
#     zip_buffer.seek(0)
#     return zip_buffer

# # Streamlit UI
# st.title("Certificate Generator")

# uploaded_template = st.file_uploader("Upload Certificate Template (JPG/PNG)", type=["jpg", "jpeg", "png"])
# uploaded_csv = st.file_uploader("Upload CSV File", type=["csv"])

# file_type = st.selectbox("Select Output Format", ["jpg", "png"], index=0)

# uploaded_font = st.file_uploader("Upload Custom Font (TTF)", type=["ttf"])

# st.subheader("Adjust Text Positions")
# name_x = st.number_input("Name X Position", min_value=0, value=500)
# name_y = st.number_input("Name Y Position", min_value=0, value=300)
# college_x = st.number_input("College X Position", min_value=0, value=500)
# college_y = st.number_input("College Y Position", min_value=0, value=400)
# events_x = st.number_input("Events X Position", min_value=0, value=500)
# events_y = st.number_input("Events Y Position", min_value=0, value=500)

# positions = {
#     "name": (name_x, name_y),
#     "college": (college_x, college_y),
#     "events": (events_x, events_y)
# }

# if uploaded_template and uploaded_csv:
#     template = Image.open(uploaded_template).convert("RGB")
    
#     if uploaded_font:
#         font = ImageFont.truetype(io.BytesIO(uploaded_font.read()), 40)
#     else:
#         font = None  # Use default font
    
#     if st.button("Preview Sample Certificate"):
#         sample_image = template.copy()
#         sample_cert = add_text_to_certificate(sample_image, "Sample Name", "Sample College", "Sample Event", positions, font)
#         st.image(sample_cert, caption="Sample Certificate", use_container_width=True)
    
#     if st.button("Generate Certificates"):
#         zip_buffer = generate_certificates(template, uploaded_csv, positions, font, file_type)
#         st.download_button("Download Certificates", zip_buffer, file_name="certificates.zip", mime="application/zip")


# # Ensure session state for authentication
# if "authenticated" not in st.session_state:
#     st.session_state["authenticated"] = True  # Set to True for testing

# if st.session_state["authenticated"]:
#     if st.sidebar.button("🔓 Logout", key="logout"):
#         st.session_state["authenticated"] = False
#         st.rerun()  # Refresh the page to return to login













import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import zipfile
import io
from Intellexa_Login import login

# Redirect to login if not authenticated
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if not st.session_state.get("authenticated", False):
    login()
    st.stop()

def add_text_to_certificate(image, data, positions, fonts):
    draw = ImageDraw.Draw(image)
    for key, value in data.items():
        if key in positions and value and key.lower() != "email":
            font = fonts[key]
            bbox = draw.textbbox((0, 0), str(value), font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            start_x = positions[key][0]
            end_x = positions[key][2]
            x_centered = (start_x + end_x) // 2 - text_width // 2
            y_centered = positions[key][1] - text_height // 2
            draw.text((x_centered, y_centered), str(value), fill="black", font=font)
    return image

def generate_certificates(template, df, positions, fonts, file_type):
    zip_buffer = io.BytesIO()
    preview_image = None

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for index, row in df.iterrows():
            image = template.copy()
            cert = add_text_to_certificate(image, {k: v for k, v in row.to_dict().items() if k.lower() != "email"}, positions, fonts)
            if index == 0:
                preview_image = cert.copy()
            img_buffer = io.BytesIO()
            cert.save(img_buffer, format=file_type.upper())
            zipf.writestr(f"certificate_{index+1}.{file_type}", img_buffer.getvalue())
    
    zip_buffer.seek(0)
    return zip_buffer, preview_image

# Streamlit UI
st.title("Certificate Generator")

uploaded_template = st.file_uploader("Upload Certificate Template (JPG/PNG)", type=["jpg", "jpeg", "png"])
uploaded_csv = st.file_uploader("Upload CSV File", type=["csv"])
file_type = st.selectbox("Select Output Format", ["jpg", "png"], index=0)
uploaded_font = st.file_uploader("Upload Custom Font (TTF)", type=["ttf"])

positions = {}
fonts = {}
df = None
if uploaded_csv:
    try:
        df = pd.read_csv(uploaded_csv)
        if df.empty:
            st.error("Uploaded CSV is empty. Please upload a valid file.")
        else:
            for column in df.columns:
                if column.lower() != "email":
                    x_start = st.number_input(f"{column} Start X Position", min_value=0, value=400)
                    x_end = st.number_input(f"{column} End X Position", min_value=0, value=600)
                    y = st.number_input(f"{column} Y Position", min_value=0, value=300)
                    font_size = st.number_input(f"{column} Font Size", min_value=10, max_value=100, value=40)
                    positions[column] = (x_start, y, x_end)
                    fonts[column] = ImageFont.truetype(io.BytesIO(uploaded_font.read()), font_size) if uploaded_font else ImageFont.load_default()
    except pd.errors.EmptyDataError:
        st.error("Error reading CSV: No data found. Please upload a valid CSV file.")

if uploaded_template and df is not None and not df.empty:
    template = Image.open(uploaded_template).convert("RGB")

    if st.button("Preview Certificate"):
        _, preview_image = generate_certificates(template, df.head(1), positions, fonts, file_type)
        if preview_image:
            st.image(preview_image, caption="Preview Certificate", use_column_width=True)

    if st.button("Generate Certificates"):
        zip_buffer, _ = generate_certificates(template, df, positions, fonts, file_type)
        st.download_button("Download Certificates", zip_buffer, file_name="certificates.zip", mime="application/zip")

# Ensure session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

if st.session_state["authenticated"]:
    if st.sidebar.button("🔓 Logout", key="logout"):
        st.session_state["authenticated"] = False
        st.rerun()
