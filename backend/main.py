import smtplib
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# FEATURE 1: AI MULTI-CHANNEL SMS PARSER
# =========================================================
def parse_multi_channel_sms(sms_text, user_phone, user_bank, user_account, has_consent=False):
    # Security Rule: If no consent or credentials missing, block parsing
    if not has_consent or not user_phone or not user_account:
        return {
            "status": "error", 
            "message": "Access Blocked: Security credentials or user consent missing."
        }
        
    source_channel = "Unknown Source"
    account_matched = "N/A"
    
    # 1. Detect Bank Channels and verify Account Number inside the SMS
    if re.search(r"CRDB|SimBanking", sms_text, re.IGNORECASE):
        source_channel = "CRDB Bank"
        if re.search(user_account[-4:], sms_text): # Matching the last 4 digits for security
            account_matched = "Verified"
            
    elif re.search(r"NMB|Klik", sms_text, re.IGNORECASE):
        source_channel = "NMB Bank"
        if re.search(user_account[-4:], sms_text):
            account_matched = "Verified"
            
    # 2. Detect Mobile Channels
    elif re.search(r"Halopesa|M-Pesa|TigoPesa|AirtelMoney", sms_text, re.IGNORECASE):
        source_channel = "Mobile Money"
        account_matched = "Linked to Phone Number"

    # 3. Extract Amount using universal money regex
    amount_pattern = r"TSH\s*([\d,]+)"
    match_amount = re.search(amount_pattern, sms_text)
    
    if not match_amount:
        return {"status": "error", "message": "Could not identify money amount in SMS."}
        
    clean_amount = float(match_amount.group(1).replace(",", ""))

    # 4. Determine if money came in or out
    if re.search(r"received|deposited|ingizwa|umepokea", sms_text, re.IGNORECASE):
        tx_type = "Income"
    else:
        tx_type = "Expense"

    return {
        "status": "success",
        "channel": source_channel,
        "account_verification": account_matched,
        "amount": clean_amount,
        "type": tx_type
    }


# =========================================================
# FEATURE 2: REAL ONLINE EMAIL OTP SENDER
# =========================================================
def send_otp_email(receiver_email):
    otp_code = str(random.randint(100000, 999999))
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # 🚨 WEKA GMAIL YAKO NA APP PASSWORD HAPA:
    sender_email = "your_project_email@gmail.com" 
    sender_password = "your_app_password_here" 

    message = MIMEMultipart()
    message["From"] = f"Smart Expense Tracker 🔒 <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = f"{otp_code} is your Smart Expense Tracker Verification Code"

    body = f"""
    Hello,

    Your security is our priority. Please use the following 6-digit One-Time Password (OTP) to verify your identity and access your Smart Expense Tracker account:

    🔒 YOUR VERIFICATION CODE: {otp_code}

    This code is valid for the next 10 minutes.

    Best regards,
    Smart Expense Tracker Engineering Team.
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
# RUNNING BOTH FOR SYSTEM INTEGRATION TEST
# =========================================================
if __name__ == "__main__":
    print("=========================================")
    print("    COMBINED BACKEND ENGINE (ONLINE)     ")
    print("=========================================\n")

    # 1. Test SMS Parser System
    print("--- 1. Testing SMS Parser Segment ---")
    sample_sms = "CRDB: TSH 35,000 withdrawn from A/C ...8900."
    parser_result = parse_multi_channel_sms(sample_sms, "0712345678", "CRDB Bank", "0152345678900", has_consent=True)
    print(f"Parser Output: {parser_result}\n")

    print("-" * 50)
    print("💡 To test the Email OTP segment, call 'send_otp_email(email)' inside your code.")