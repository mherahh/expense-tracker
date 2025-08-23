import sqlite3

class BaseDB:
    def __init__(self, db_path='expense_tracker.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


class ExpenseDB(BaseDB): 
    def initialize_db(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS expenses(
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                date TEXT, 
                                amount INTEGER, 
                                month TEXT,
                                category TEXT
                            )
                            """)
        
        self.commit()


    def add_expense(self, date,amount,month, category):
        self.cursor.execute("INSERT INTO  expenses (date,amount,month, category) VALUES (?,?,?,?)", (date,amount,month,category))
        self.commit()

    def view_expenses(self, month):
        self.cursor.execute("SELECT * FROM expenses WHERE month=?",(month,))
        return self.cursor.fetchall()
 
    def update_expense(self, expense_id, new_date, new_amount,new_month, new_category):
        self.cursor.execute("UPDATE expenses SET date=?, amount=?, month=?, category=? WHERE id=?",(new_date,new_amount,new_month, new_category,expense_id))
        self.commit()

    def delete_expense(self, expense_id):
        current = self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self.commit()

    def get_expense(self, expense_id):
        self.cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
        row = self.cursor.fetchone()
        print("DEBUG: row returned =", row)  # or use st.write
        return row

class BudgetDB(BaseDB):
    def initialize_db(self):

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS budget(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            amount INTEGER DEFAULT 0,
                            month TEXT
                            )
                            """)
        self.commit()
    
    def set_budget(self, amount, month):
        #check if it exists
        self.cursor.execute("SELECT * FROM budget WHERE month=?", (month,))
        exists = self.cursor.fetchone()
        
        if exists:
            self.cursor.execute("UPDATE budget SET amount=? WHERE month=?",(amount,month))
        else:
            self.cursor.execute("INSERT INTO budget (amount, month) VALUES  (?, ?)", (amount, month))
        
        self.commit()


    def get_budget(self, month):
        self.cursor.execute("SELECT amount FROM budget WHERE month=?", (month,))
        result =  self.cursor.fetchone()
        if result is None:
            return (0,)
        return result
    
    def update_budget_amount(self, month, money,increase=False):
        if increase:
            self.cursor.execute("UPDATE budget SET amount = amount + ? WHERE month=?", (money,month))
        else:
            self.cursor.execute("UPDATE budget SET amount = amount - ? WHERE month=?", (money,month))
        self.commit()
        print("Budget updated")



