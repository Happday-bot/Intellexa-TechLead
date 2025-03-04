import streamlit as st
import pandas as pd
import smtplib
import io
import fitz  # PyMuPDF for PDF to image conversion
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image
import time
from Intellexa_Login import login

# Redirect to login if not authenticated
if not st.session_state.get("authenticated", False):
    login()
    st.stop()

def generate_certificate_pdf(data, font_path, positions, font_sizes, template_file):
    buffer = io.BytesIO()
    template = Image.open(template_file)
    width, height = template.size  
    temp_template_path = "./temp_certificate.png"
    template.save(temp_template_path)
    c = canvas.Canvas(buffer, pagesize=(width, height))
    if font_path:
        try:
            pdfmetrics.registerFont(TTFont("CustomFont", font_path))
            font_name = "CustomFont"
        except Exception as e:
            st.error(f"Font Error: {e}")
            font_name = "Helvetica"
    else:
        font_name = "Helvetica"
    c.drawImage(temp_template_path, 0, 0, width, height)
    text_drawn = False
    for key, value in data.items():
        if key in positions and value:
            start_x, end_x, y = positions[key]
            font_size = font_sizes.get(key, 40)
            c.setFont(font_name, font_size)
            text_width = c.stringWidth(str(value), font_name, font_size)
            x_pos = start_x + (end_x - start_x - text_width) / 2  # Centering text
            c.drawString(x_pos, y, str(value))
            text_drawn = True
    if not text_drawn:
        print("⚠ Warning: No text drawn on the certificate!")
    c.save()
    buffer.seek(0)
    return buffer

def send_email(sender_email, sender_password, recipient_email, email_subject, email_body, cert_buffer, file_name):
    msg = MIMEMultipart()
    msg["From"] = f"INTELLEXA REC <{sender_email}>"
    msg["To"] = recipient_email
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_body, "plain"))
    attachment = MIMEApplication(cert_buffer.read(), Name=file_name)
    attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
    msg.attach(attachment)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email to {recipient_email}: {e}")
        return False

def show_certificate_preview(cert_buffer):
    try:
        pdf_document = fitz.open("pdf", cert_buffer.getvalue())
        first_page = pdf_document[0]
        pix = first_page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        st.image(img, caption="Sample Certificate Preview", use_container_width=True)
    except Exception as e:
        st.error(f"Error displaying preview: {e}")



def show_progress(current_value, final_value, progress_bar):
    progress = int((current_value / final_value) * 100) if final_value > 0 else 100
    progress_bar.progress(progress)


st.title("Automated Certificate Generator & Email Sender")
sender_email = st.text_input("Enter your email")
sender_password = st.text_input("Enter your 16-digit app password", type="password")
csv_file = st.file_uploader("Upload CSV file", type=["csv"])
email_subject = st.text_input("Email Subject")
email_body = st.text_area("Email Body")
template_file = st.file_uploader("Upload Certificate Template", type=["png", "jpg", "jpeg"])
font_file = st.file_uploader("Upload Font File (Optional, e.g., Arial.ttf)", type=["ttf"])

positions = {}
font_sizes = {}

final_value = 0 
progress_bar = st.progress(0)



if csv_file:
    csv_file.seek(0)
    df = pd.read_csv(csv_file, encoding="utf-8")
    
    final_value = len(df)

    for column in df.columns:
        if column.lower() != "email":
            start_x = st.number_input(f"{column} Start X Position", min_value=0, value=200)
            end_x = st.number_input(f"{column} End X Position", min_value=0, value=600)
            y_pos = st.number_input(f"{column} Y Position", min_value=0, value=150)
            font_size = st.number_input(f"{column} Font Size", min_value=10, max_value=100, value=40)
            positions[column] = (start_x, end_x, y_pos)
            font_sizes[column] = font_size

font_path = None
if font_file:
    font_path = "./uploaded_font.ttf"
    with open(font_path, "wb") as f:
        f.write(font_file.read())

if template_file and csv_file:
    st.subheader("Preview Certificate")
    if st.button("Preview Sample Certificate"):
        sample_data = df.iloc[0].to_dict() if not df.empty else {col: "Sample " + col for col in positions.keys()}
        if not positions or not font_sizes:
            st.error("Please set text positions and font sizes before previewing!")
        else:
            cert_buffer = generate_certificate_pdf(sample_data, font_path, positions, font_sizes, template_file)
            show_certificate_preview(cert_buffer)

if template_file and st.button("Generate & Send Certificates"):
    success_count = 0
    failed_count = 0
    for _, row in df.iterrows():
        recipient_email = row.get("email", "").strip()
        if not recipient_email:
            st.warning("Skipping row with missing email.")
            continue
        cert_buffer = generate_certificate_pdf(row, font_path, positions, font_sizes, template_file)
        file_name = f"certificate_{row['Name']}.pdf"
        if send_email(sender_email, sender_password, recipient_email, email_subject, email_body, cert_buffer, file_name):
            success_count += 1
            show_progress(success_count, final_value, progress_bar)
            time.sleep(0.1)  
        else:
            failed_count += 1
    st.success(f"Process complete! {success_count} emails sent, {failed_count} failed.")


# Ensure session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True  # Set to True for testing

if st.session_state["authenticated"]:
    if st.sidebar.button("🔓 Logout", key="logout"):
        st.session_state["authenticated"] = False
        st.rerun()  # Refresh the page to return to login
