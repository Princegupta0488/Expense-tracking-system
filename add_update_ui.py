import streamlit as st
from datetime import datetime
import requests

# ✅ localhost -> 127.0.0.1 (same as Postman)
API_URL = "http://127.0.0.1:8000"


def add_update_tab():
    # Date input (convert to YYYY-MM-DD format)
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")
    selected_date = selected_date.strftime("%Y-%m-%d")

    # 🔹 Safe GET request
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}", timeout=5)
        response.raise_for_status()
        existing_expenses = response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Backend server chal nahi raha. Pehle FastAPI start karo.")
        existing_expenses = []
    except requests.exceptions.Timeout:
        st.error("⚠️ Request timeout ho gayi.")
        existing_expenses = []
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error: {e}")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    label="Amount", min_value=0.0, step=1.0,
                    value=amount, key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category", options=categories,
                    index=categories.index(category),
                    key=f"category_{i}", label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label="Notes", value=notes,
                    key=f"notes_{i}", label_visibility="collapsed"
                )

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]

            # 🔹 Safe POST request
            try:
                response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses, timeout=5)
                if response.status_code == 200:
                    st.success("✅ Expenses updated successfully!")
                else:
                    st.error(f"❌ Failed to update expenses. (Status {response.status_code})")
            except requests.exceptions.ConnectionError:
                st.error("❌ Backend server chal nahi raha. Pehle FastAPI start karo.")
            except requests.exceptions.Timeout:
                st.error("⚠️ Request timeout ho gayi.")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Error: {e}")
