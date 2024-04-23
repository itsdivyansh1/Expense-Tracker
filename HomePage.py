import customtkinter as ctk
import matplotlib
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import tkinter.messagebox as messagebox
import mysql.connector

matplotlib.use('TkAgg')

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="expensetracker"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def insert_daily_expense(date, category, expense):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO daily_expenses (date, category, expense) VALUES (%s, %s, %s)"
        values = (date, category, expense)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

def insert_monthly_expense(category, expense):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO monthly_expenses (category, expense) VALUES (%s, %s)"
        values = (category, expense)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

def insert_category(category):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO categories (category_name) VALUES (%s)"
        values = (category,)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

def get_categories():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT category_name FROM categories"
        cursor.execute(query)
        results = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return results
    return []

def delete_category(category):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = "DELETE FROM categories WHERE category_name = %s"
        values = (category,)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Budget App")
        self.geometry("800x600")

        # Get monthly income
        self.monthly_income = self.get_monthly_income()
        self.total_spend = 0

        # Initialize categories
        self.categories = get_categories()
        self.recurring_categories = ["Rent", "Recharge", "Subscription"]

        # Initialize categories dictionary
        self.categories_expenses = {category: 0 for category in self.categories}

        # Create main tabs
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True)

        self.expense_tab = self.notebook.add("Daily Expenses")
        self.monthly_expenses_tab = self.notebook.add("Monthly Expenses")
        self.pie_chart_tab = self.notebook.add("Pie Chart")
        self.bar_chart_tab = self.notebook.add("Bar Chart")

        # Create frames
        self.expense_frame = ctk.CTkFrame(self.expense_tab)
        self.expense_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        self.pie_chart_frame = ctk.CTkFrame(self.pie_chart_tab)
        self.pie_chart_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        self.bar_chart_frame = ctk.CTkFrame(self.bar_chart_tab)
        self.bar_chart_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        self.monthly_expenses_frame = ctk.CTkFrame(self.monthly_expenses_tab)
        self.monthly_expenses_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # Create category tab
        self.category_tab = ctk.CTkTabview(self.expense_frame)
        self.category_tab.pack(side="right", padx=10, pady=10, fill="y", expand=False, anchor="ne")
        self.category_tab.add("Categories")

        # Create category list
        self.create_category_list()

        # Create expense input widgets
        self.create_expense_input_widgets()

        # Create pie chart
        self.create_pie_chart(self.pie_chart_frame)

        # Create bar chart
        self.create_bar_chart(self.bar_chart_frame)

        # Create recurring categories input widgets
        self.create_recurring_categories_input_widgets()

    def get_monthly_income(self):
        income_dialog = ctk.CTkInputDialog(text="Enter your monthly budget:", title="Monthly Budget")
        income = income_dialog.get_input()

        while not income or not income.isdigit():
            income_dialog = ctk.CTkInputDialog(text="Please enter a valid number for your monthly Budget:",
                                               title="Monthly Budget")
            income = income_dialog.get_input()

        return int(income)

    def create_expense_input_widgets(self):
        # Category and expense input
        category_label = ctk.CTkLabel(self.expense_frame, text="Category and Expense")
        category_label.pack(pady=10)

        self.category_combobox = ctk.CTkComboBox(self.expense_frame, values=self.categories, state="readonly")
        self.category_combobox.pack(pady=10)

        expense_entry = ctk.CTkEntry(self.expense_frame, placeholder_text="Expense")
        expense_entry.pack(pady=10)

        # Add daily expense button
        daily_expense_button = ctk.CTkButton(self.expense_frame, text="Add to Expense",
                                             command=self.add_daily_expense)
        daily_expense_button.pack(pady=10)

        # Add custom category button
        add_category_button = ctk.CTkButton(self.expense_frame, text="Add Category", command=self.add_custom_category)
        add_category_button.pack(pady=10)

        # Expense table
        self.expense_table = ctk.CTkTextbox(self.expense_frame, height=200)
        self.expense_table.bind("<Key>", lambda e: "break")
        self.expense_table.pack(pady=10, fill="both", expand=True)

        # Budget labels
        budget_frame = ctk.CTkFrame(self.expense_frame)
        budget_frame.pack(pady=10)

        income_label = ctk.CTkLabel(budget_frame, text=f"Budget: ₹{self.monthly_income}")
        income_label.pack(side="left", padx=10)

        self.total_spend_label = ctk.CTkLabel(budget_frame, text=f"Total Spend: ₹{self.total_spend}")
        self.total_spend_label.pack(side="left", padx=10)

        self.remaining_money_label = ctk.CTkLabel(budget_frame, text=f"Remaining: ₹{self.monthly_income - self.total_spend}")
        self.remaining_money_label.pack(side="left", padx=10)

        # Set expense entry and add expense button
        self.expense_entry = expense_entry
        self.add_expense_button = daily_expense_button

    def create_pie_chart(self, frame):
        self.pie_figure = Figure(figsize=(5, 5), dpi=100)
        self.pie_ax = self.pie_figure.add_subplot(111)
        self.pie_chart = FigureCanvasTkAgg(self.pie_figure, frame)
        self.pie_chart.get_tk_widget().pack(side="top", fill="both", expand=True)

    def create_bar_chart(self, frame):
        self.bar_figure = Figure(figsize=(5, 5), dpi=100)
        self.bar_ax = self.bar_figure.add_subplot(111)
        self.bar_chart = FigureCanvasTkAgg(self.bar_figure, frame)
        self.bar_chart.get_tk_widget().pack(side="top", fill="both", expand=True)

    def add_custom_category(self):
        custom_category = ctk.CTkInputDialog(text="Enter new category:", title="Add Category")
        category = custom_category.get_input()

        if category:
            insert_category(category)
            self.categories = get_categories()
            self.category_combobox.configure(require_redraw=True, values=self.categories)
            self.categories_expenses[category] = 0  # Add new category to categories_expenses
            self.add_category_frame(category)  # Add the new category frame

    def add_daily_expense(self):
        selected_category = self.category_combobox.get()
        expense = self.expense_entry.get()
        date = datetime.date.today()

        if selected_category and expense:
            total_expenses_today = float(expense)
            if total_expenses_today > self.monthly_income - self.total_spend:
                messagebox.showerror("Error",
                                     f"Your total expenses for today ({total_expenses_today}) exceed your remaining budget ({self.monthly_income - self.total_spend}). Please adjust your expenses accordingly.")
                return

            insert_daily_expense(date, selected_category, float(expense))
            self.expense_table.insert("end", f"{date}: {selected_category}: ₹{expense}\n")
            self.category_combobox.set("")
            self.expense_entry.delete(0, "end")
            self.update_pie_chart(date)
            self.update_bar_chart()
            self.update_total_spend(float(expense))
            self.update_remaining_money()

    def update_pie_chart(self, date):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT category, SUM(expense) AS total FROM daily_expenses WHERE date = %s GROUP BY category"
            values = (date,)
            cursor.execute(query, values)
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            budget_data = []
            categories = []
            total_budget = 0

            for category, expense in results:
                budget_data.append(expense)
                categories.append(category)
                total_budget += expense

            self.pie_ax.clear()
            self.pie_ax.pie(budget_data, labels=categories, autopct='%1.1f%%', startangle=90)
            self.pie_ax.axis('equal')
            self.pie_ax.set_title(f"Budget Allocation ({date})")
            self.pie_chart.draw()

    def update_bar_chart(self):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT date, category, SUM(expense) AS total FROM daily_expenses GROUP BY date, category ORDER BY date"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            dates = sorted(set([result[0] for result in results]))
            categories = set([result[1] for result in results])

            if not categories:
                self.bar_ax.clear()
                self.bar_chart.draw()
                return

            data = {category: [0 for _ in dates] for category in categories}
            for date, category, expense in results:
                date_index = dates.index(date)
                data[category][date_index] = expense

            self.bar_ax.clear()
            x = range(len(dates))
            bar_width = 0.8 / len(categories)
            bottom = [0] * len(dates)
            for i, category in enumerate(categories):
                self.bar_ax.bar(x, data[category], bar_width, bottom=bottom, label=category)
                for j in range(len(dates)):
                    bottom[j] += data[category][j]

            self.bar_ax.set_xticks(x)
            self.bar_ax.set_xticklabels([date.strftime("%Y-%m-%d") for date in dates], rotation=45, ha="right")
            self.bar_ax.set_xlabel("Date")
            self.bar_ax.set_ylabel("Expenses")
            self.bar_ax.set_title("Daily Expenses")
            self.bar_ax.legend()
            self.bar_chart.draw()

    def update_total_spend(self, expense):
        self.total_spend += expense
        self.total_spend_label.configure(text=f"Total Spend: ₹{self.total_spend}")

    def update_remaining_money(self):
        remaining_money = self.monthly_income - self.total_spend
        self.remaining_money_label.configure(text=f"Remaining: ₹{remaining_money}")

    def create_category_list(self):
        self.category_scrollable_frame = ctk.CTkScrollableFrame(self.category_tab.tab("Categories"),
                                                                label_text="Categories")
        self.category_scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.category_frames = []
        for category in self.categories:
            self.add_category_frame(category)

    def add_category_frame(self, category):
        delete_image = ctk.CTkImage(Image.open("assets/delete.png"))

        category_frame = ctk.CTkFrame(self.category_scrollable_frame)
        category_frame.pack(pady=10, padx=10, fill="x")

        category_label = ctk.CTkLabel(category_frame, text=category)
        category_label.pack(side="left", padx=10)

        delete_button = ctk.CTkButton(master=category_frame, image=delete_image, text="", fg_color="#ff2e38",
                                      hover_color="#b30009", width=16, height=16,
                                      command=lambda c=category: self.delete_category(c))
        delete_button.pack(side="right", padx=10)

        self.category_frames.append(category_frame)

    def delete_category(self, category):
        self.categories.remove(category)
        self.category_combobox.configure(require_redraw=True, values=self.categories)
        self.category_combobox.set("")  # Clear the combobox selection
        for category_frame in self.category_frames:
            category_label = category_frame.winfo_children()[0]
            if category_label.cget("text") == category:
                category_frame.destroy()
                self.category_frames.remove(category_frame)
                break
        del self.categories_expenses[category]
        delete_category(category)
        self.update_pie_chart(datetime.date.today())
        self.update_bar_chart()

    def create_recurring_categories_input_widgets(self):
        # Recurring category and expense input
        recurring_category_label = ctk.CTkLabel(self.monthly_expenses_frame, text="Recurring Category and Expense")
        recurring_category_label.pack(pady=10)

        self.recurring_category_combobox = ctk.CTkComboBox(self.monthly_expenses_frame,
                                                           values=self.recurring_categories, state="readonly")
        self.recurring_category_combobox.pack(pady=10)

        recurring_expense_entry = ctk.CTkEntry(self.monthly_expenses_frame, placeholder_text="Expense")
        recurring_expense_entry.pack(pady=10)

        # Add recurring expense button
        add_recurring_expense_button = ctk.CTkButton(self.monthly_expenses_frame, text="Add Recurring Expense",
                                                     command=self.add_recurring_expense)
        add_recurring_expense_button.pack(pady=10)

        # Add custom recurring category button
        add_recurring_category_button = ctk.CTkButton(self.monthly_expenses_frame, text="Add Recurring Category",
                                                      command=self.add_custom_recurring_category)
        add_recurring_category_button.pack(pady=10)

        # Monthly expenses table
        self.monthly_expenses_table = ctk.CTkTextbox(self.monthly_expenses_frame, height=200)
        self.monthly_expenses_table.pack(pady=10, fill="both", expand=True)

        # Set recurring expense entry and add recurring expense button
        self.recurring_expense_entry = recurring_expense_entry
        self.add_recurring_expense_button = add_recurring_expense_button

    def add_recurring_expense(self):
        selected_category = self.recurring_category_combobox.get()
        expense = self.recurring_expense_entry.get()

        if selected_category and expense:
            insert_monthly_expense(selected_category, float(expense))
            self.monthly_expenses_table.insert("end", f"{selected_category}: ₹{expense}\n")
            self.recurring_category_combobox.set("")
            self.recurring_expense_entry.delete(0, "end")

    def add_custom_recurring_category(self):
        custom_category = ctk.CTkInputDialog(text="Enter new recurring category:", title="Add Recurring Category")
        category = custom_category.get_input()

        if category:
            self.recurring_categories.append(category)
            self.recurring_category_combobox.configure(require_redraw=True, values=self.recurring_categories)

if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()