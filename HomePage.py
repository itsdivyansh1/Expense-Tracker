import customtkinter as ctk
import matplotlib
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')


class ExpenseTracker(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("800x600")

        # Get monthly income
        self.monthly_income = self.get_monthly_income()

        # Initialize categories
        self.categories = ["Shopping", "Entertainment", "Utilities"]

        # Create main tabs
        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(fill="both", expand=True)

        self.expense_tab = self.notebook.add("Expenses")
        self.pie_chart_tab = self.notebook.add("Pie Chart")
        self.bar_chart_tab = self.notebook.add("Bar Chart")

        # Create frames
        self.expense_frame = ctk.CTkFrame(self.expense_tab)
        self.expense_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        self.pie_chart_frame = ctk.CTkFrame(self.pie_chart_tab)
        self.pie_chart_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        self.bar_chart_frame = ctk.CTkFrame(self.bar_chart_tab)
        self.bar_chart_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # Create category tab
        # Create category tab
        self.category_tab = ctk.CTkTabview(self.expense_frame)
        self.category_tab.pack(side="right", padx=10, pady=10, fill="y", expand=False, anchor="ne")  # Modified pack parameters
        self.category_tab.add("Categories")

        # Create category list
        self.create_category_list()


        # Display monthly income
        income_label = ctk.CTkLabel(self.expense_frame, text=f"Monthly Income: ${self.monthly_income}")
        income_label.pack(pady=10)

        # Create input widgets for expenses
        self.create_expense_input_widgets()

        # Create pie chart
        self.create_pie_chart(self.pie_chart_frame)

        # Create bar chart
        self.create_bar_chart(self.bar_chart_frame)

        # Initialize categories dictionary
        self.categories_expenses = {}

    def get_monthly_income(self):
        income_dialog = ctk.CTkInputDialog(text="Enter your monthly income:", title="Monthly Income")
        income = income_dialog.get_input()

        while not income or not income.isdigit():
            income_dialog = ctk.CTkInputDialog(text="Please enter a valid number for your monthly income:",
                                               title="Monthly Income")
            income = income_dialog.get_input()

        return int(income)

    def create_expense_input_widgets(self):
        # Category and expense input
        category_label = ctk.CTkLabel(self.expense_frame, text="Category and Expense")
        category_label.pack(pady=10)

        self.categories = ["Shopping", "Entertainment", "Utilities"]
        self.category_combobox = ctk.CTkComboBox(self.expense_frame, values=self.categories, state="readonly")
        self.category_combobox.pack(pady=10)

        expense_entry = ctk.CTkEntry(self.expense_frame, placeholder_text="Expense")
        expense_entry.pack(pady=10)

        # Add expense button
        add_expense_button = ctk.CTkButton(self.expense_frame, text="Add Expense", command=self.add_expense)
        add_expense_button.pack(pady=10)

        # Add custom category button
        add_category_button = ctk.CTkButton(self.expense_frame, text="Add Category", command=self.add_custom_category)
        add_category_button.pack(pady=10)

        # Expense table
        self.expense_table = ctk.CTkTextbox(self.expense_frame, height=200)
        self.expense_table.pack(pady=10, fill="both", expand=True)

        # Set expense entry and add expense button
        self.expense_entry = expense_entry
        self.add_expense_button = add_expense_button

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
            self.categories.append(category)
            self.category_combobox.configure(require_redraw=True, values=self.categories)

    def add_expense(self):
        selected_category = self.category_combobox.get()
        expense = self.expense_entry.get()

        if selected_category and expense:
            self.categories_expenses[selected_category] = self.categories_expenses.get(selected_category, 0) + float(
                expense)
            self.expense_table.insert("end", f"{selected_category}: ${expense}\n")
            self.category_combobox.set("")
            self.expense_entry.delete(0, "end")
            self.update_pie_chart()
            self.update_bar_chart()

    def update_pie_chart(self):
        budget_data = []
        categories = []
        self.total_budget = 0

        for category, expense in self.categories_expenses.items():
            budget_data.append(expense)
            categories.append(category)
            self.total_budget += expense

        self.pie_ax.clear()
        self.pie_ax.pie(budget_data, labels=categories, autopct='%1.1f%%', startangle=90)
        self.pie_ax.axis('equal')
        self.pie_ax.set_title("Budget Allocation")
        self.pie_chart.draw()

    def update_bar_chart(self):
        categories = list(self.categories_expenses.keys())
        expenses = list(self.categories_expenses.values())

        self.bar_ax.clear()
        self.bar_ax.bar(categories, expenses)
        self.bar_ax.set_xlabel("Categories")
        self.bar_ax.set_ylabel("Expenses")
        self.bar_ax.set_title("Category Expenses")
        self.bar_chart.draw()

    def create_category_list(self):
        self.category_scrollable_frame = ctk.CTkScrollableFrame(self.category_tab.tab("Categories"), label_text="Categories")
        self.category_scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.category_frames = []
        for category in self.categories:
            self.add_category_frame(category)

    def add_category_frame(self, category):
        # delete_image = ImageTk.PhotoImage(Image.open("./delete.png").resize((16, 16)))
        delete_image = ctk.CTkImage(Image.open("assets/delete.png"))

        category_frame = ctk.CTkFrame(self.category_scrollable_frame)
        category_frame.pack(pady=10, padx=10, fill="x")

        category_label = ctk.CTkLabel(category_frame, text=category)
        category_label.pack(side="left", padx=10)

        delete_button = ctk.CTkButton(master=category_frame, image=delete_image, text="", fg_color="#ff2e38", hover_color="#b30009", width=16, height=16, command=lambda c=category: self.delete_category(c))
        delete_button.pack(side="right", padx=10)

        self.category_frames.append(category_frame)

    def delete_category(self, category):
        self.categories.remove(category)
        self.category_combobox.configure(require_redraw=True, values=self.categories)
        for category_frame in self.category_frames:
            category_label = category_frame.winfo_children()[0]
            if category_label.cget("text") == category:
                category_frame.destroy()
                self.category_frames.remove(category_frame)
                break
        del self.categories_expenses[category]
        self.update_pie_chart()
        self.update_bar_chart()

    def add_custom_category(self):
        custom_category = ctk.CTkInputDialog(text="Enter new category:", title="Add Category")
        category = custom_category.get_input()

        if category:
            self.categories.append(category)
            self.category_combobox.configure(require_redraw=True, values=self.categories)
            self.add_category_frame(category)


if __name__ == "__main__":
    app = ExpenseTracker()
    app.mainloop()

