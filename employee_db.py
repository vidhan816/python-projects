import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


# ---------- Database Connection ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="Your_password",  # Change to your MySQL password
        database="employee_db"
    )


# ---------- Authentication Window ----------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Employee Management System")
        self.root.geometry("350x250")

        tk.Label(root, text="Username:", font=('Arial', 12)).pack(pady=5)
        self.username = tk.Entry(root)
        self.username.pack(pady=5)

        tk.Label(root, text="Password:", font=('Arial', 12)).pack(pady=5)
        self.password = tk.Entry(root, show="*")
        self.password.pack(pady=5)

        tk.Button(root, text="Login", command=self.login, bg="blue", fg="white").pack(pady=15)

    def login(self):
        uname = self.username.get()
        pwd = self.password.get()

        if not uname or not pwd:
            messagebox.showerror("Error", "All fields are required")
            return

        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
        row = cur.fetchone()
        conn.close()

        if row:
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Invalid username or password")


# ---------- Main Employee Management ----------
class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("900x500")

        # ---------- Variables ----------
        self.id = tk.StringVar()
        self.name = tk.StringVar()
        self.age = tk.StringVar()
        self.gender = tk.StringVar()
        self.dept = tk.StringVar()
        self.salary = tk.StringVar()
        self.search = tk.StringVar()

        # ---------- Title ----------
        title = tk.Label(root, text="Employee Management System", font=("Arial", 20, "bold"), bg="blue", fg="white")
        title.pack(side=tk.TOP, fill=tk.X)

        # ---------- Form Frame ----------
        form_frame = tk.Frame(root, bd=2, relief=tk.RIDGE, padx=10, pady=10)
        form_frame.place(x=20, y=60, width=400, height=400)

        tk.Label(form_frame, text="Name", font=('Arial', 12)).grid(row=0, column=0, pady=5)
        tk.Entry(form_frame, textvariable=self.name, font=('Arial', 12)).grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Age", font=('Arial', 12)).grid(row=1, column=0, pady=5)
        tk.Entry(form_frame, textvariable=self.age, font=('Arial', 12)).grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Gender", font=('Arial', 12)).grid(row=2, column=0, pady=5)
        gender_cb = ttk.Combobox(form_frame, textvariable=self.gender, values=["Male", "Female"], font=('Arial', 12))
        gender_cb.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Department", font=('Arial', 12)).grid(row=3, column=0, pady=5)
        tk.Entry(form_frame, textvariable=self.dept, font=('Arial', 12)).grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="Salary", font=('Arial', 12)).grid(row=4, column=0, pady=5)
        tk.Entry(form_frame, textvariable=self.salary, font=('Arial', 12)).grid(row=4, column=1, pady=5)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=5, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Add", width=10, command=self.add_employee).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", width=10, command=self.update_employee).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", width=10, command=self.delete_employee).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", width=10, command=self.clear_form).grid(row=0, column=3, padx=5)

        # ---------- Search Frame ----------
        search_frame = tk.Frame(root)
        search_frame.place(x=450, y=60, width=420)

        tk.Label(search_frame, text="Search by Name", font=('Arial', 12)).grid(row=0, column=0)
        tk.Entry(search_frame, textvariable=self.search, font=('Arial', 12)).grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_employee).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Show All", command=self.fetch_data).grid(row=0, column=3, padx=5)

        # ---------- Table ----------
        table_frame = tk.Frame(root, bd=2, relief=tk.RIDGE)
        table_frame.place(x=450, y=100, width=420, height=360)

        self.employee_table = ttk.Treeview(table_frame, columns=("id", "name", "age", "gender", "dept", "salary"),
                                           show='headings')
        for col in self.employee_table["columns"]:
            self.employee_table.heading(col, text=col.capitalize())
            self.employee_table.column(col, width=70)
        self.employee_table.pack(fill=tk.BOTH, expand=1)
        self.employee_table.bind("<ButtonRelease-1>", self.get_selected_row)

        self.fetch_data()

    # ---------- CRUD Functions ----------
    def add_employee(self):
        if self.name.get() == "" or self.age.get() == "" or self.salary.get() == "":
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO employees (name, age, gender, department, salary) VALUES (%s, %s, %s, %s, %s)",
                        (self.name.get(), self.age.get(), self.gender.get(), self.dept.get(), self.salary.get()))
            conn.commit()
            conn.close()
            self.fetch_data()
            self.clear_form()
            messagebox.showinfo("Success", "Employee added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    def fetch_data(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees")
        rows = cur.fetchall()
        conn.close()

        self.employee_table.delete(*self.employee_table.get_children())
        for row in rows:
            self.employee_table.insert("", tk.END, values=row)

    def get_selected_row(self, ev):
        row = self.employee_table.focus()
        data = self.employee_table.item(row)
        row_data = data["values"]
        if row_data:
            self.id.set(row_data[0])
            self.name.set(row_data[1])
            self.age.set(row_data[2])
            self.gender.set(row_data[3])
            self.dept.set(row_data[4])
            self.salary.set(row_data[5])

    def update_employee(self):
        if self.id.get() == "":
            messagebox.showerror("Error", "Select an employee to update")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("UPDATE employees SET name=%s, age=%s, gender=%s, department=%s, salary=%s WHERE id=%s",
                    (self.name.get(), self.age.get(), self.gender.get(), self.dept.get(), self.salary.get(),
                     self.id.get()))
        conn.commit()
        conn.close()
        self.fetch_data()
        self.clear_form()
        messagebox.showinfo("Success", "Record updated successfully")

    def delete_employee(self):
        if self.id.get() == "":
            messagebox.showerror("Error", "Select an employee to delete")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=%s", (self.id.get(),))
        conn.commit()
        conn.close()
        self.fetch_data()
        self.clear_form()
        messagebox.showinfo("Deleted", "Employee deleted successfully")

    def search_employee(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE name LIKE %s", ("%" + self.search.get() + "%",))
        rows = cur.fetchall()
        conn.close()

        self.employee_table.delete(*self.employee_table.get_children())
        for row in rows:
            self.employee_table.insert("", tk.END, values=row)

    def clear_form(self):
        self.id.set("")
        self.name.set("")
        self.age.set("")
        self.gender.set("")
        self.dept.set("")
        self.salary.set("")


# ---------- Launch App ----------
def main_app():
    root = tk.Tk()
    EmployeeApp(root)
    root.mainloop()


if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()