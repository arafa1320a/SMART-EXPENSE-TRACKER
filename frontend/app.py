import streamlit as nn
import requests

# Set ukurasa ukae vizuri na uonekane wa kiprofeshinali
nn.set_page_config(page_title="Smart Expense Tracker", page_icon="🔒", layout="centered")

# URL ya Backend (FastAPI) inayorun kwenye kompyuta yako
BACKEND_URL = "http://127.0.0.1:8000"

# ==========================================
# MFUMO WA USIMAMIZI WA HALI YA SEVA (Session State)
# ==========================================
if "logged_in" not in nn.session_state:
    nn.session_state.logged_in = False
if "otp_sent" not in nn.session_state:
    nn.session_state.otp_sent = False
if "user_email" not in nn.session_state:
    nn.session_state.user_email = ""

# ==========================================
# SKRINI YA KWANZA: SECURE LOGIN PORTAL
# ==========================================
if not nn.session_state.logged_in:
    nn.markdown("<h2 style='text-align: center;'>🔒 Secure Login Portal</h2>", unsafe_allow_html=True)
    nn.write("---")
    
    # Sehemu ya kuingiza barua pepe
    email_input = nn.text_input("Enter your Registered Email Address:", placeholder="example@gmail.com", value=nn.session_state.user_email)
    
    # 1. Kitufe cha kuomba OTP
    if nn.button("Send Verification Code (OTP) 📩", use_container_width=True):
        if email_input.strip() == "":
            nn.error("⚠️ Tafadhali weka barua pepe yako kwanza!")
        else:
            with nn.spinner("Inatuma OTP..."):
                try:
                    # Tuma ombi Backend kutengeneza OTP ya kipekee
                    response = requests.post(f"{BACKEND_URL}/api/auth/send-otp", json={"email": email_input.strip()})
                    res_data = response.json()
                    
                    if response.status_code == 200 and res_data.get("status") == "success":
                        nn.session_state.otp_sent = True
                        nn.session_state.user_email = email_input.strip().lower()
                        nn.success(res_data.get("message", "OTP imetumwa! Angalia barua pepe yako na terminal ya Backend."))
                    else:
                        nn.error(f"❌ Imeshindwa: {res_data.get('detail', 'Kosa lisilojulikana')}")
                except Exception as e:
                    nn.error(f"🌐 Hitilafu ya Mtandao: Backend haipatikani. Hakikisha umewasha 'python backend/main.py'.")

    # 2. Sehemu ya kuingiza OTP baada ya kubonyeza kitufe cha kwanza
    if nn.session_state.otp_sent:
        nn.write("---")
        otp_input = nn.text_input("Enter the 6-Digit OTP Sent to You:", placeholder="123456", max_chars=6)
        
        if nn.button("Verify & Login 🚀", use_container_width=True):
            with nn.spinner("Inathibitisha..."):
                try:
                    # Tuma barua pepe na OTP kwenda Backend ikazilinganishe
                    verify_response = requests.post(
                        f"{BACKEND_URL}/api/auth/verify-otp", 
                        json={"email": nn.session_state.user_email, "otp": otp_input.strip()}
                    )
                    verify_data = verify_response.json()
                    
                    if verify_response.status_code == 200 and verify_data.get("status") == "success":
                        nn.session_state.logged_in = True
                        nn.success("✅ Umeingia kwa mafanikio!")
                        nn.rerun()  # Refresh ukurasa kuingia kwenye Dashboard
                    else:
                        nn.error(f"❌ {verify_data.get('detail', 'Namba ya OTP si sahihi.')}")
                except Exception as e:
                    nn.error("🌐 Mwasiliano yamekatika wakati wa uthibitishaji.")

# ==========================================
# SKRINI YA PILI: BANGO KUU (DASHBOARD & AI FEATURES)
# ==========================================
else:
    # Kitufe cha kutoka kwenye mfumo (Logout) kilichopo juu kulia
    col1, col2 = nn.columns([4, 1])
    with col1:
        nn.title("📊 Smart Expense Tracker Dashboard")
        nn.write(f"Karibu, **{nn.session_state.user_email}** 👋")
    with col2:
        if nn.button("Log Out 🚪"):
            nn.session_state.logged_in = False
            nn.session_state.otp_sent = False
            nn.session_state.user_email = ""
            nn.rerun()

    nn.write("---")

    # Tengeneza tab mbili kwa ajili ya mifumo yetu miwili mikuu
    tab1, tab2 = nn.tabs(["📱 Multi-Channel SMS Parser", "🤖 AI Expense Classifier"])

    # ------------------------------------------
    # TAB 1: MULTI-CHANNEL SMS PARSER (CRDB nk.)
    # ------------------------------------------
    with tab1:
        nn.header("CRDB & Multi-Bank SMS Core Parser")
        nn.write("Weka matini (text) ya meseji ya benki hapa chini ili mfumo uichuje kiotomatiki.")
        
        bank_name = nn.selectbox("Chagua Benki:", ["CRDB Bank", "NMB Bank", "NMB Mkononi", "Exim Bank"])
        phone_no = nn.text_input("Namba ya Simu iliyopokea SMS:", value="0655567917")
        account_no = nn.text_input("Namba ya Akaunti ya Mtumiaji:", value="12345-XXXX-6789")
        
        sms_text_area = nn.text_area(
            "Bandika (Paste) Meseji ya SMS Hapa:",
            value="Imepokelewa TZS 35,000.00 kutoka kwa Arafa. Salio jipya ni TZS 150,000.00"
        )
        
        consent_check = nn.checkbox("Ninaruhusu mfumo kusoma na kuchuja ujumbe huu kwa usalama.")

        if nn.button("Anza Kuchuja SMS (Parse SMS) 🔍"):
            if not consent_check:
                nn.warning("⚠️ Lazima ukubali kutoa idhini (consent) ili mfumo uchakate ujumbe.")
            else:
                with nn.spinner("Inachuja SMS..."):
                    try:
                        parser_res = requests.post(
                            f"{BACKEND_URL}/api/parser/parse-sms",
                            json={
                                "sms_text": sms_text_area,
                                "user_phone": phone_no,
                                "user_bank": bank_name,
                                "user_account": account_no,
                                "has_consent": True
                            }
                        )
                        data = parser_res.json()
                        if data.get("status") == "success":
                            nn.success("✅ SMS Imesomwa kwa Ufanisi!")
                            
                            # Onyesha majibu kwenye maboksi maridadi (Metrics)
                            c1, c2, c3 = nn.columns(3)
                            c1.metric(label="Kiasi (Amount)", value=f"TZS {data.get('amount'):,}")
                            c2.metric(label="Aina ya Muamala", value=data.get("type"))
                            c3.metric(label="Hali ya Akaunti", value=data.get("account_verification"))
                        else:
                            nn.error(f"❌ Kosa: {data.get('message')}")
                    except Exception as e:
                        nn.error("🌐 Imeshindwa kuwasiliana na mfumo wa kuchuja SMS wa Backend.")

    # ------------------------------------------
    # TAB 2: AI EXPENSE CLASSIFIER (KNN / Rules)
    # ------------------------------------------
    with tab2:
        nn.header("AI Automated Spending Categorization")
        nn.write("Mfumo wa AI unaotumia usindikaji wa lugha asilia (NLP) kupanga matumizi yako kwenye makundi.")
        
        exp_amount = nn.number_input("Weka Kiasi cha Pesa zilizotumika (TZS):", min_value=0.0, value=15000.0)
        exp_desc = nn.text_input("Andika Maelezo ya Matumizi (Mfano: nilinunua chips na kuku au nauli ya bolt):", value="chips dume na kuku")
        
        if nn.button("Panga kwa AI (Predict Category) 🤖"):
            if exp_desc.strip() == "":
                nn.warning("⚠️ Tafadhali andika maelezo ya matumizi.")
            else:
                with nn.spinner("AI Inatafakari..."):
                    try:
                        ai_res = requests.post(
                            f"{BACKEND_URL}/api/ai/predict-category",
                            json={"amount": exp_amount, "description": exp_desc}
                        )
                        ai_data = ai_res.json()
                        
                        if ai_data.get("status") == "success":
                            nn.info(f"🤖 **Matokeo ya AI:** Matumizi haya yanajumuishwa kwenye kundi la:")
                            nn.subheader(f"👉 {ai_data.get('predicted_category')}")
                            
                            # Confusion Matrix Metric Simulation
                            nn.caption(f"Kiwango cha Usahihi wa AI (Confidence Score): {ai_data.get('confidence_score') * 100}%")
                        else:
                            nn.error("AI imeshindwa kupanga matumizi haya.")
                    except Exception as e:
                        nn.error("🌐 Mawasiliano na AI Core Backend yamefeli.")