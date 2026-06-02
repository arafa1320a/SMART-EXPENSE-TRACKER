import streamlit as st
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# LOCAL EMAIL OTP SENDER (Inafanya kazi hapo hapo kwenye PC yako online)
# =========================================================
def send_otp_email_local(receiver_email):
    # Inazalisha OTP namba 6 kiotomatiki
    otp_code = str(random.randint(100000, 999999))
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # 🚨 WEKA GMAIL YAKO NA APP PASSWORD YAKO HAPA KUTEST LIVE:
    sender_email = "arafahashim52@gmail.c0m" 
    sender_password = "jvmlvvhzufcqqdzw" 

    message = MIMEMultipart()
    message["From"] = f"Smart Expense Tracker 🔒 <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = f"{otp_code} is your Smart Expense Tracker Verification Code"

    body = f"""
    Hello,
    Use this 6-digit One-Time Password (OTP) to access your Smart Expense Tracker:
    🔒 YOUR VERIFICATION CODE: {otp_code}
    """
    message.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return {"status": "success", "otp": otp_code}
    except Exception as e:
        return {"status": "error", "message": str(e), "otp": otp_code}

# =========================================================
# APP CONFIGURATION & LOGIN GATEWAY
# =========================================================
st.set_page_config(page_title="SMART EXPENSE TRACKER", page_icon="💰", layout="wide")

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "real_otp" not in st.session_state:
    st.session_state.real_otp = ""

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>🔒 Secure Login Portal</h2>", unsafe_allow_html=True)
    
    _, login_col, _ = st.columns([1, 2, 1])
    with login_col:
        user_email = st.text_input("Enter your Registered Email Address:", placeholder="student@example.com")
        
        if st.button("Send Verification Code (OTP) 📩"):
            if user_email and "@" in user_email:
                with st.spinner("Connecting to mail servers..."):
                    # Inaita function ya hapa hapa kwenye PC yako
                    email_response = send_otp_email_local(user_email)
                    if email_response["status"] == "success":
                        st.session_state.otp_sent = True
                        st.session_state.real_otp = email_response["otp"]
                        st.success(f"✔ Code sent successfully to {user_email}.")
                    else:
                        st.error(f"❌ Error: {email_response['message']}")
            else:
                st.error("❌ Please enter a valid email address.")
        
        if st.session_state.otp_sent:
            user_otp = st.text_input("Enter the 6-Digit Code received:", type="password", max_chars=6)
            if st.button("Verify & Login 🚀"):
                if user_otp == st.session_state.real_otp:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Code.")

# =========================================================
# THE MAIN DASHBOARD (Kazi yako yote ya mwanzo)
# =========================================================
else:
    dash_col, logout_col = st.columns([9, 1])
    with dash_col:
        st.title("SMART EXPENSE TRACKER - Dashboard")
    with logout_col:
        if st.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.otp_sent = False
            st.rerun()

    st.write("---")
    st.sidebar.header("🔒 Verified Sync Profile")
    user_phone = st.sidebar.text_input("Registered Mobile Number:", value="0655567917")
    user_bank = st.sidebar.selectbox("Select your Primary Bank:", ["CRDB Bank", "NMB Bank", "NBC Bank"])
    user_account = st.sidebar.text_input("Bank Account Number:", placeholder="e.g., 015XXXXXXXXXX")
    allow_all_access = st.sidebar.checkbox("Authorize Automated SMS Analysis", value=True)

    st.sidebar.write("---")
    total_income = st.sidebar.number_input("Enter your total income (TSH):", value=650000)
    total_expense = st.sidebar.number_input("Enter your total expenses (TSH):", value=87000)
    available_amount = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="SECTION 1: Total Income", value=f"TSH {total_income:,}")
    with col2: st.metric(label="SECTION 2: Total Expenses", value=f"TSH {total_expense:,}")
    with col3: st.metric(label="SECTION 3: Available Amount", value=f"TSH {available_amount:,}")