# Expense Tracker Application

#### Video Demo: https://youtu.be/H6_zTRlAWog?si=QGW07U494Fvtwx2q

#### WebApp Link: https://expensetracker101.streamlit.app/

#### Description: 
Expense Tracker is a personal finance management application built using Python, Streamlit, SQLite, Pandas, and Plotly. The application 
allows users to set monthly budgets, record expenses, modify existing entries, delete expenses, and visualize spending patterns through interactive charts.
Users can:
- Set budget
- Add, edit or remove expenses
- View insights of spendings
- Download it in csv format


#### Project Structure

- app.py

This file contains the Streamlit user interface and application logic.
Responsibilities include:
Rendering the dashboard
Handling user interactions
Displaying charts and tables
Managing forms for adding, editing, and deleting expenses
Communicating with the database layer

- db.py

This file contains all database-related functionality. The project uses SQLite for persistent storage.
The database layer is organized using object-oriented programming and consists of three classes:

BaseDB:
Creating database connections
Committing transactions
Closing connections

ExpenseDB:
Creating the expenses table
Adding expenses
Viewing expenses
Updating expenses
Deleting expenses
Retrieving individual expense records

BudgetDB:
Creating the budget table
Setting monthly budgets
Retrieving budget information
Updating remaining budget values
