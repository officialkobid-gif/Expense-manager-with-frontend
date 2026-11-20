
import json
import streamlit as st
from pathlib import Path

# ---------------- DATABASE ----------------

DATABASE = Path(__file__).parent / "expense.json"


def load_data():
    if DATABASE.exists():
        with open(DATABASE, "r") as fs:
            content = fs.read()
            if content.strip():
                return json.loads(content)

    return []


data = load_data()


def update():
    with open(DATABASE, "w") as fs:
        json.dump(data, fs, indent=4)


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Expense Manager",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Expense Manager")
st.caption("Manage your monthly balance and expenses.")

# ---------------- SIDEBAR ----------------

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Expense",
        "Update Data",
        "Search Expenses",
        "Show All Expenses"
    ]
)

# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.header("Your Dashboard")

    balance = data[0]["balan"] if data and "balan" in data[0] else 0

    expenses = data[1:] if data and "balan" in data[0] else data

    total = sum(int(item["amount"]) for item in expenses)

    remaining = balance - total

    col1, col2, col3 = st.columns(3)

    col1.metric("Monthly Balance", f"Rs. {balance}")
    col2.metric("Total Spending", f"Rs. {total}")
    col3.metric("Remaining Balance", f"Rs. {remaining}")

    st.divider()

    st.subheader("Recent Expenses")

    if expenses:
        st.dataframe(expenses, use_container_width=True)
    else:
        st.info("No expenses recorded yet.")

# ---------------- ADD EXPENSE ----------------

elif menu == "Add Expense":

    st.header("Add New Expense")

    with st.form("expense_form"):

        amount = st.number_input(
            "Enter amount",
            min_value=1,
            step=100
        )

        category = st.selectbox(
            "Select category",
            [
                "Food",
                "Education",
                "House",
                "Clothes",
                "Festival",
                "Transportation",
                "Health",
                "Others"
            ]
        )

        description = st.text_area("Description")

        submit = st.form_submit_button("Add Expense")

        if submit:

            info = {
                "amount": int(amount),
                "category": category,
                "description": description
            }

            data.append(info)
            update()

            st.success("Expense added successfully!")

# ---------------- UPDATE DATA ----------------

elif menu == "Update Data":

    st.header("Update Existing Data")

    expenses = data[1:] if data and "balan" in data[0] else data

    option = st.selectbox(
        "What do you want to update?",
        [
            "Monthly Balance",
            "Expense Category",
            "Expense Description",
            "Expense Amount"
        ]
    )

    if option == "Monthly Balance":

        current = data[0]["balan"] if data and "balan" in data[0] else 0

        new_balance = st.number_input(
            "New monthly balance",
            min_value=0,
            value=int(current),
            step=100
        )

        if st.button("Update Balance"):

            if data and "balan" in data[0]:
                data[0]["balan"] = int(new_balance)
            else:
                data.insert(0, {"balan": int(new_balance)})

            update()
            st.success("Balance updated successfully!")

    elif expenses:

        selected = st.selectbox(
            "Select expense",
            range(len(expenses)),
            format_func=lambda i: (
                f"{expenses[i]['category']} - "
                f"Rs. {expenses[i]['amount']} "
                f"({expenses[i]['description']})"
            )
        )

        item = expenses[selected]

        if option == "Expense Category":

            new_value = st.text_input(
                "New category",
                value=item["category"]
            )

        elif option == "Expense Description":

            new_value = st.text_area(
                "New description",
                value=item["description"]
            )

        else:

            new_value = st.number_input(
                "New amount",
                min_value=1,
                value=int(item["amount"]),
                step=100
            )

        if st.button("Save Changes"):

            if option == "Expense Category":
                item["category"] = new_value

            elif option == "Expense Description":
                item["description"] = new_value

            else:
                item["amount"] = int(new_value)

            update()
            st.success("Expense updated successfully!")

    else:
        st.info("No expenses available to update.")

# ---------------- SEARCH EXPENSES ----------------

elif menu == "Search Expenses":

    st.header("Search Your Expenses")

    choice = st.selectbox(
        "Choose search method",
        [
            "Category",
            "Amount",
            "Description",
            "Keyword"
        ]
    )

    expenses = data[1:] if data and "balan" in data[0] else data

    if choice == "Category":

        search = st.text_input("Enter category")

        if st.button("Search"):

            results = [
                item for item in expenses
                if search.strip().lower() == item["category"].lower()
            ]

            if results:
                st.success(f"Found {len(results)} result(s)")
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("No matching category found.")

    elif choice == "Amount":

        search = st.number_input(
            "Enter amount",
            min_value=0,
            step=100
        )

        if st.button("Search"):

            results = [
                item for item in expenses
                if int(item["amount"]) == search
            ]

            if results:
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("No matching amount found.")

    elif choice == "Description":

        search = st.text_input("Enter description")

        if st.button("Search"):

            results = [
                item for item in expenses
                if search.strip().lower() in item["description"].lower()
            ]

            if results:
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("No matching description found.")

    elif choice == "Keyword":

        search = st.text_input("Enter any keyword")

        if st.button("Search"):

            results = [
                item for item in expenses
                if search.strip().lower() in str(item).lower()
            ]

            if results:
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("No matching keyword found.")

# ---------------- SHOW ALL EXPENSES ----------------

elif menu == "Show All Expenses":

    st.header("All Your Expenses")

    if data:

        if "balan" in data[0]:
            st.metric("Monthly Balance", f"Rs. {data[0]['balan']}")

        expenses = data[1:] if "balan" in data[0] else data

        if expenses:
            st.dataframe(expenses, use_container_width=True)
        else:
            st.info("No expenses recorded yet.")

    else:
        st.info("Your database is empty.")
