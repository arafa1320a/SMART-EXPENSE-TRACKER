import re

def parse_sms_transaction(sms_text):
    print(f"Scanning Incoming SMS: '{sms_text}'\n")
    
    # 1. Detect the Mobile Money Provider (Source)
    provider = "Unknown Provider"
    if re.search(r"Halopesa", sms_text, re.IGNORECASE):
        provider = "Halopesa"
    elif re.search(r"M-Pesa|Vodacom", sms_text, re.IGNORECASE):
        provider = "M-Pesa"
    elif re.search(r"AirtelMoney", sms_text, re.IGNORECASE):
        provider = "Airtel Money"
    elif re.search(r"TigoPesa", sms_text, re.IGNORECASE):
        provider = "Tigo Pesa"

    # 2. Extract the Transaction Amount (Regex Pattern)
    amount_pattern = r"TSH\s*([\d,]+)"
    match_amount = re.search(amount_pattern, sms_text)
    
    if not match_amount:
        return {"status": "error", "message": "No valid amount found."}
        
    # Get the number and remove commas to make it a clean mathematical number
    clean_amount = float(match_amount.group(1).replace(",", ""))

    # 3. Determine Transaction Type (Income vs Expense) using Keywords
    # If the SMS contains words like 'received' or 'umepokea', it's an Income!
    if re.search(r"received|umepokea|ingizwa", sms_text, re.IGNORECASE):
        transaction_type = "Income"
    else:
        transaction_type = "Expense"

    # Return the final organized data structure
    return {
        "status": "success",
        "provider": provider,
        "amount": clean_amount,
        "type": transaction_type
    }

# =========================================================
# TEST RUN (Simulating real SMS data)
# =========================================================
if __name__ == "__main__":
    print("=========================================")
    print("     SMART EXPENSE TRACKER - BACKEND     ")
    print("=========================================\n")

    # Test Case 1: Income SMS
    sms_1 = "Halopesa: You have received TSH 50,000 from ARAFA ONLINE."
    result_1 = parse_sms_transaction(sms_1)
    print(f"Result 1: {result_1}")
    print("-" * 50)

    # Test Case 2: Expense SMS
    sms_2 = "M-Pesa: You have paid TSH 12,000 to LUKU."
    result_2 = parse_sms_transaction(sms_2)
    print(f"Result 2: {result_2}")
    print("=========================================")