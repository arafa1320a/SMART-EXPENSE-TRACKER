import streamlit as st 
# Page Configuration
st.set_page_config(page_title="SMART EXPENSE TRACKER",layout="wide") 
#Main Title and Subtitle
st.title("SMART EXPENSE TRACKER - Dashboard")
st.markdown("Welcome to your AI-powered  financial management system.")
st.write("---")
#Moc Data (example of data)
st.sidebar.header("Update Dashboard Data")
total_income=st.sidebar.number_input("Enter your total income (TSH):", value=90000)
total_expenses=st.sidebar.number_input("Enter your total expenses (TSH):", value=65000)
available_amount=total_income-total_expenses
#The 3 core dashboard sections(using columns)
col1,col2,col3=st.columns(3)
with col1:
    st.metric(label="SECTION 1: Total Income", value=f"TSH {total_income:,}")
    st.caption("Total amount of all your incoming revenues.")
with col2:
    st.metric(label="SECTION 2: Tptal Expenses", value=f"TSH {total_expenses:,}")
    st.caption("Total amount of all your registered expenditures.")
with col3:
    st.metric(label="SECTION 3:Available Amount", value=f"TSH {available_amount:,}")
    st.caption("The remaining balance in your account.")
st.write("---")
# Recent Unfilled Expenses Alert Section
st.subheader("Recent Activity: Unfilled Expenses")
st.info("A new transaction of TSH 12,000 has been detected from your SMS.") 
#Interactive AI button
if st.button("run AI Classifier"):
    st.success("AI Classification Successful! The transaction of TSH 12,000 has been categorized under: Internet and bundle")           