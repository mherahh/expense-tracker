import streamlit as st
from db import BaseDB, ExpenseDB, BudgetDB
from datetime import datetime
import pandas as pd
import plotly.express as px
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

def Initialize_db():
    if "budget_db" not in st.session_state:
        st.session_state.budget_db = BudgetDB()
        st.session_state.budget_db.initialize_db()  #why do this?
    if "expense_db" not in st.session_state:
        st.session_state.expense_db = ExpenseDB()
        st.session_state.expense_db.initialize_db()


def set_budget():
    if "show_budget" not in st.session_state:
        st.session_state.show_budget = False
    if st.sidebar.button("Set Budget",key="set_budget", help="Enter your budget"):
        st.session_state.show_budget = not st.session_state.show_budget

    if st.session_state.show_budget:
        with st.sidebar.form(key="budget_form"):
            amount = st.number_input("Amount", min_value=0)
            month = st.selectbox("Month", months, key= "set_budget_selector" )
            
            col1,col2 = st.columns([1,1])
            submit_button = col1.form_submit_button("Submit")
            cancel_button = col2.form_submit_button("Cancel")

            if submit_button:
                st.session_state.budget_db.set_budget(amount,month)
                st.success("Budget added  successfully!")
                st.session_state.show_budget = False  # Hide form after submission

            elif cancel_button:
                st.session_state.show_budget= False


def select_month():
    st.sidebar.markdown("<h3 style='text-align: center;'>Select a Month</h3>", unsafe_allow_html=True)
    return  st.sidebar.selectbox("Month", months,key="main_month")
    
def display_budget(selected_month):
    original = st.session_state.budget_db.get_og_budget(selected_month)[0]
    remains = st.session_state.budget_db.get_budget(selected_month)
    if remains:   # not None
        remains = remains[0]  # extract number from tuple
    else:
        remains = 0

    if remains < 0:
        color = "#F54927"
    else:
        color = "#2E86C1"

    st.markdown(
        f"""
        <div style="text-align:center;">
            <h4 style="text-align:center; color:gray;">Set Budget</h4>
            <h1 style="text-align:center; font-size:80px; color:#555;">{original} PKR</h1>
            <h4 style="text-align:center; color:gray;">Remaining Budget</h4>
            <h1 style="text-align:center; font-size:80px; color:{color};">{remains}</h1>

        </div>
        """,
        unsafe_allow_html=True
    )


def display_expense(df):
    st.markdown("\n") 
    st.markdown("<h4 style='text-align: center; color:gray;'>Expenses </h4>", unsafe_allow_html=True)
    st.markdown("\n")
    st.dataframe(df)


def add_expense(df):
    if "show_addExpense" not in st.session_state:
        st.session_state.show_addExpense = False

    if st.sidebar.button("Add expense", key="add_button", help="Add Expense"):
        st.session_state.show_addExpense = not st.session_state.show_addExpense  # Toggle form visibility

    if st.session_state.show_addExpense:
        with st.sidebar.form(key="expense_form"):
            date = st.date_input("Date" , key="expense_date")

            amount = st.number_input("Amount", min_value=0)    #STARTING FROM .0
            month = st.session_state.main_month
            category = st.selectbox("Category", ["Food", "Grocery", "Transport", "Rent", "Medical", "Bills", "Others"])

            col1,col2 = st.columns([1,1])
            submit_button = col1.form_submit_button("Submit")
            cancel_button = col2.form_submit_button("Cancel")
            
            if submit_button:
                budget = st.session_state.budget_db.get_og_budget(month)
                budget = budget[0]
                if budget == 0:
                    st.error(f"Set Budget for {month} first!")

                else:
                    st.session_state.expense_db.add_expense(date,amount,month,category)
                    st.session_state.budget_db.update_budget_amount(month, amount, increase=False)
                    st.success("Expense added successfully!")
                    st.session_state.show_addExpense = False  # Hide form after submission

            elif cancel_button:
                st.session_state.show_addExpense = False

def edit_expense(df):
    if "show_editExpense" not in st.session_state:
        st.session_state.show_editExpense = False

    if st.sidebar.button("Edit expense", key="edit_button", help="Edit Expense"):
        st.session_state.show_editExpense = not st.session_state.show_editExpense  # Toggle form visibility

    if st.session_state.show_editExpense:
        with st.sidebar.form(key="edit_expense_form"):
            
            expense_id= st.selectbox("Select expense ID to edit:", df['ID'].tolist())
            date = st.date_input("Date", value=datetime.now())
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")   
            month = date.strftime("%B")     
            category = st.selectbox("Category", ["Food", "Grocery", "Transport", "Rent", "Medical", "Bills", "Others"])

            col1,col2 = st.columns([1,1])
            submit_button = col1.form_submit_button("Submit")
            cancel_button = col2.form_submit_button("Cancel")

            if submit_button:
                    date_str = date.strftime("%Y-%m-%d")
                    
                    previous_expense = st.session_state.expense_db.get_expense(expense_id)
                    if previous_expense is not None:
                        previous_expense_amount = previous_expense[2]
                        previous_expense_month = previous_expense[3]
                    else:
                        st.error("No expense found")
                        return

                    st.session_state.budget_db.update_budget_amount(previous_expense_month, previous_expense_amount, increase=True)
                    
                    st.session_state.expense_db.update_expense(expense_id,date_str,amount, month, category)
                    st.session_state.budget_db.update_budget_amount(month, amount, increase=False)

                    st.success("Expense updated successfully!")
                    st.session_state.show_editExpense = False  # Hide form after submission
       

            elif cancel_button:
                st.session_state.show_editExpense = False

def remove_expense(df):
    if "show_removeExpense" not in st.session_state:
        st.session_state.show_removeExpense = False
            
    if st.sidebar.button("Remove expense", key="remove_button", help="Remove Expense"):
        st.session_state.show_removeExpense = not st.session_state.show_removeExpense

    if st.session_state.show_removeExpense:
        with st.sidebar.form(key="Remove expense"):

            expense_id= st.selectbox("Select expense ID to delete:", df['ID'].tolist())

            col1,col2 = st.columns([1,1])
            submit_button = col1.form_submit_button("Submit")
            cancel_button = col2.form_submit_button("Cancel")

            expense = st.session_state.expense_db.get_expense(expense_id)

            if expense:
                amount = expense[2]
                month = expense[3]

            if submit_button:
                st.session_state.budget_db.update_budget_amount(month, amount, increase=True)
                st.session_state.expense_db.delete_expense(expense_id)
                st.success(f"Expense {expense_id} deleted!")
                st.session_state.show_removeExpense = False
               
            elif cancel_button:
                st.session_state.show_removeExpense = False


def expense_breakdown(month, df):
    st.markdown("<h4 style='text-align: center; color:gray;'>Expense Breakdown </h4>", unsafe_allow_html=True)
    fig = px.pie(df, values="Amount", names="Category")
    st.plotly_chart(fig)

def top_spending(month, df):
    top_category = df.groupby("Category")["Amount"].sum().idxmax()
    top_amount = df.groupby("Category")["Amount"].sum().max()
    st.markdown(f"""<h5 style='text-align: center; color:gray;'>
                        The highest spending category for this month is {top_category}, with total spending upto {top_amount} PKR
                         </h5>
    """, unsafe_allow_html=True)

def general_scatter(df):
    st.markdown("<h4 style='text-align: center; color:gray;'>Spendings over the month </h4>", unsafe_allow_html=True)
    fig = px.scatter(
        df,
        x=df['Date'],
        y=df['Amount'],
        color=df['Category'],
        size=df['Amount'],
        title="Spendings over the month"
    )
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    st.plotly_chart(fig)


def download_report(df, selected_month):
    if df.empty:
        st.warning("No expenses available to download.")
        return
    
    csv = df.to_csv(index=False).encode("utf=8")

    st.download_button(
        label = "Download CSV Report",
        data = csv,
        file_name=f"{selected_month}_expenses.csv",
        mime="text/csv"
    )


def main():
    Initialize_db()
    selected_month = select_month()
    rows = st.session_state.expense_db.view_expenses(selected_month)
    df = pd.DataFrame(rows, columns=['ID', 'Date', 'Amount','Month', 'Category'])

    st.sidebar.markdown("<h3 style='text-align: center;'>Settings</h3>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Overview", "Insights"])
    with tab1:
        set_budget()
        add_expense(df)
        edit_expense(df)
        remove_expense(df)
        display_budget(selected_month)
        display_expense(df)
        download_report(df, selected_month)
    with tab2:
        if df.empty:
            st.warning("No expenses found for this month.")
        else:
            general_scatter(df)
            expense_breakdown(selected_month, df)
            top_spending(selected_month,df)




##done subtracting expense from budget, testing remains

if __name__ == "__main__":
    main()