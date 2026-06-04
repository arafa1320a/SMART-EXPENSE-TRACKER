from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

# =========================================================
# DATA MODELS (Mifumo ya kupokea data kutoka Frontend)
# =========================================================
class EmailRequest(BaseModel):
    email: str

class SMSRequest(BaseModel):
    sms_text: str

# =========================================================
# FEATURE 1: AKILI YA KUTUMA OTP (API Endpoint)
# =========================================================
@app.post("/send-otp")
def api_send_otp(payload: EmailRequest):
    receiver_email = payload.email
    otp_code = str(random.randint(100000, 999999))
    
    # 🚨 PATNA: Weka email na App Password yako hapa kwa ajili ya seva
    sender_email = "project_backend_email@gmail.com" 
    sender_password = "your_app_password_here" 

    message = MIMEMultipart()
    message["From"] = f"Smart Expense Tracker 🔒 <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = f"{otp_code} is your Security Verification Code"

    body = f"Hello, Your 6-digit verification code is: {otp_code}"
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return {"status": "success", "otp": otp_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================
# FEATURE 2: AKILI YA SMS PARSER (Kazi ya Partner Wako)
# =========================================================
@app.post("/parse-sms")
def api_parse_sms(payload: SMSRequest):
    text = payload.sms_text
    
    # Mfano wa Regex ya kutafuta kiasi cha pesa (TSH) kwenye meseji
    # (Hapa ataweka zile kanuni zake mlizozipanga za kusoma SMS za CRDB, NMB n.k.)
    amount_match = re.search(r'(?:Kiasi:|Paid|Sent|Imetumwa|Imepokelewa)\s*(?:TSH|Tsh|Sh)?\s*([\d,]+)', text)
    
    if amount_match:
        # Kusafisha namba (kuondoa mawakf/commas)
        amount_str = amount_match.group(1).replace(",", "")
        amount = float(amount_str)
        
        return {
            "status": "success",
            "detected_amount": amount,
            "message": "SMS processed successfully by Backend parser."
        }
    else:
        return {
            "status": "failed",
            "detected_amount": 0.0,
            "message": "No transaction amount detected in the SMS text."
        }

# Kuwasha seva
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
