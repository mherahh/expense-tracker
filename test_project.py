import pytest
from db import ExpenseDB, BudgetDB


@pytest.fixture
def expense_db():
    """Initialised ExpenseDB backed by an in-memory SQLite database."""
    db = ExpenseDB(db_path=":memory:")
    db.initialize_db()
    yield db
    db.close()


@pytest.fixture
def budget_db():
    """Initialised BudgetDB backed by an in-memory SQLite database."""
    db = BudgetDB(db_path=":memory:")
    db.initialize_db()
    yield db
    db.close()


# ──────────────────────────────────────────────
# Test 1 — Add and retrieve an expense
# ──────────────────────────────────────────────

def test_add_and_view_expense(expense_db):
    """
    Adding an expense and viewing it for the correct month should return
    exactly one row with matching fields.
    """
    expense_db.add_expense("2024-06-15", 500, "June", "Food")

    rows = expense_db.view_expenses("June")

    assert len(rows) == 1, "Expected exactly one expense for June"

    _id, date, amount, month, category = rows[0]
    assert date == "2024-06-15"
    assert amount == 500
    assert month == "June"
    assert category == "Food"


# ──────────────────────────────────────────────
# Test 2 — Delete an expense and verify removal
# ──────────────────────────────────────────────

def test_delete_expense(expense_db):
    """
    After deleting an expense by ID, get_expense should return None
    and the month view should be empty.
    """
    expense_db.add_expense("2024-06-20", 200, "June", "Transport")

    rows = expense_db.view_expenses("June")
    expense_id = rows[0][0]           # grab auto-generated ID

    expense_db.delete_expense(expense_id)

    assert expense_db.get_expense(expense_id) is None, \
        "Deleted expense should not be retrievable"
    assert expense_db.view_expenses("June") == [], \
        "Month view should be empty after deletion"


# ──────────────────────────────────────────────
# Test 3 — Update an expense
# ──────────────────────────────────────────────

def test_update_expense(expense_db):
    """
    Updating amount, date, month, and category should persist correctly
    and be reflected by get_expense.
    """
    expense_db.add_expense("2024-06-01", 100, "June", "Food")
    expense_id = expense_db.view_expenses("June")[0][0]

    expense_db.update_expense(expense_id, "2024-07-10", 999, "July", "Bills")

    updated = expense_db.get_expense(expense_id)
    assert updated is not None
    _id, date, amount, month, category = updated
    assert date == "2024-07-10"
    assert amount == 999
    assert month == "July"
    assert category == "Bills"


# ──────────────────────────────────────────────
# Test 4 — Set budget and verify remaining balance
# ──────────────────────────────────────────────

def test_set_budget_and_get_remaining(budget_db):
    """
    Setting a budget of 10 000 for June and then deducting 3 000 should
    leave a remaining balance of 7 000. The original amount must stay at
    10 000 regardless of deductions.
    """
    budget_db.set_budget(10_000, "June")
    budget_db.update_budget_amount("June", 3_000, increase=False)

    remaining = budget_db.get_budget("June")[0]
    original  = budget_db.get_og_budget("June")[0]

    assert remaining == 7_000, f"Expected 7000, got {remaining}"
    assert original  == 10_000, "Original budget must not change after a deduction"


# ──────────────────────────────────────────────
# Test 5 — Overwrite budget resets both columns
# ──────────────────────────────────────────────

def test_overwrite_budget_resets_original(budget_db):
    """
    Setting a budget a second time for the same month (e.g. a correction)
    should update BOTH the remaining amount AND the original_amount to the
    new value — no stale original should remain from the first entry.
    """
    budget_db.set_budget(5_000, "July")
    budget_db.update_budget_amount("July", 1_000, increase=False)  # spend 1 000

    # Overwrite with a new budget of 8 000
    budget_db.set_budget(8_000, "July")

    remaining = budget_db.get_budget("July")[0]
    original  = budget_db.get_og_budget("July")[0]

    assert remaining == 8_000, \
        f"Remaining should reset to 8000 after overwrite, got {remaining}"
    assert original == 8_000, \
        f"Original should reset to 8000 after overwrite, got {original}"
