import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("900x600")

        self.setup_style()
        self.setup_ui()
        self.create_tables()

    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('alt')

        # Define colors
        pastel_green = "#b6fcd5"
        pastel_yellow = "#fffac8"
        pastel_red = "#ffcccb"

        # Configure styles
        self.style.configure('TNotebook', background=pastel_yellow)
        self.style.configure('TNotebook.Tab', font=('Arial', 14, 'bold'), background=pastel_green)
        self.style.map('TNotebook.Tab', background=[('selected', pastel_red)])
        self.style.configure('TButton', font=('Arial', 12), padding=6, background=pastel_green)
        self.style.map('TButton', background=[('active', pastel_red)], foreground=[('active', 'black')])
        self.style.configure('Treeview.Heading', font=('Arial', 12, 'bold'), background=pastel_yellow)

        self.root.configure(bg=pastel_yellow)

    def setup_ui(self):
        tab_control = ttk.Notebook(self.root)

        self.book_tab = ttk.Frame(tab_control)
        self.borrower_tab = ttk.Frame(tab_control)
        self.borrow_tab = ttk.Frame(tab_control)
        self.return_tab = ttk.Frame(tab_control)

        tab_control.add(self.book_tab, text='Manage Books')
        tab_control.add(self.borrower_tab, text='Manage Borrowers')
        tab_control.add(self.borrow_tab, text='Borrow Book')
        tab_control.add(self.return_tab, text='Return Book')
        tab_control.pack(expand=1, fill='both')

        self.setup_book_tab()
        self.setup_borrower_tab()
        self.setup_borrow_tab()
        self.setup_return_tab()

    def create_tables(self):
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Books (
                    BookID TEXT PRIMARY KEY,
                    Title TEXT,
                    Author TEXT,
                    Status TEXT DEFAULT 'Available'
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Borrowers (
                    BorrowerID TEXT PRIMARY KEY,
                    LastName TEXT,
                    FirstName TEXT,
                    MiddleName TEXT,
                    Course TEXT,
                    ContactNumber TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Borrow (
                    BookID TEXT,
                    BorrowerID TEXT,
                    BorrowDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (BookID, BorrowerID),
                    FOREIGN KEY (BookID) REFERENCES Books(BookID),
                    FOREIGN KEY (BorrowerID) REFERENCES Borrowers(BorrowerID)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    Username TEXT PRIMARY KEY,
                    Password TEXT
                )
            """)

    def setup_book_tab(self):
        ttk.Label(self.book_tab, text="Book ID").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.book_tab, text="Title").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.book_tab, text="Author").grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.book_id = ttk.Entry(self.book_tab)
        self.book_title = ttk.Entry(self.book_tab)
        self.book_author = ttk.Entry(self.book_tab)

        self.book_id.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.book_title.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.book_author.grid(row=2, column=1, padx=10, pady=10, sticky="we")

        ttk.Button(self.book_tab, text="Add Book", command=self.add_book).grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.book_tree = ttk.Treeview(self.book_tab, columns=('BookID', 'Title', 'Author', 'Status'), show='headings')
        self.book_tree.heading('BookID', text='Book ID')
        self.book_tree.heading('Title', text='Title')
        self.book_tree.heading('Author', text='Author')
        self.book_tree.heading('Status', text='Status')
        self.book_tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.book_tab.grid_columnconfigure(1, weight=1)
        self.book_tab.grid_rowconfigure(4, weight=1)

        self.load_books()

    def setup_borrower_tab(self):
        ttk.Label(self.borrower_tab, text="Borrower ID").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.borrower_tab, text="Last Name").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.borrower_tab, text="First Name").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.borrower_tab, text="Middle Name").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.borrower_tab, text="Course").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.borrower_tab, text="Contact Number").grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.borrower_id = ttk.Entry(self.borrower_tab)
        self.borrower_lastname = ttk.Entry(self.borrower_tab)
        self.borrower_firstname = ttk.Entry(self.borrower_tab)
        self.borrower_middlename = ttk.Entry(self.borrower_tab)
        self.borrower_course = ttk.Entry(self.borrower_tab)
        self.borrower_contact = ttk.Entry(self.borrower_tab)

        self.borrower_id.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.borrower_lastname.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.borrower_firstname.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        self.borrower_middlename.grid(row=3, column=1, padx=10, pady=10, sticky="we")
        self.borrower_course.grid(row=4, column=1, padx=10, pady=10, sticky="we")
        self.borrower_contact.grid(row=5, column=1, padx=10, pady=10, sticky="we")

        ttk.Button(self.borrower_tab, text="Add Borrower", command=self.add_borrower).grid(row=6, column=0, padx=10, pady=10, columnspan=2)

        self.borrower_tree = ttk.Treeview(self.borrower_tab, columns=('BorrowerID', 'LastName', 'FirstName', 'MiddleName', 'Course', 'ContactNumber'), show='headings')
        self.borrower_tree.heading('BorrowerID', text='Borrower ID')
        self.borrower_tree.heading('LastName', text='Last Name')
        self.borrower_tree.heading('FirstName', text='First Name')
        self.borrower_tree.heading('MiddleName', text='Middle Name')
        self.borrower_tree.heading('Course', text='Course')
        self.borrower_tree.heading('ContactNumber', text='Contact Number')


        self.borrower_tree.column('BorrowerID', width=90)
        self.borrower_tree.column('LastName', width=140)
        self.borrower_tree.column('FirstName', width=140)
        self.borrower_tree.column('MiddleName', width=140)
        self.borrower_tree.column('Course', width=70)
        self.borrower_tree.column('ContactNumber', width=130)
        self.borrower_tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.borrower_tab.grid_columnconfigure(1, weight=1)
        self.borrower_tab.grid_rowconfigure(7, weight=1)

        self.load_borrowers()

    def setup_borrow_tab(self):
        ttk.Label(self.borrow_tab, text="Book ID").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Label(self.borrow_tab, text="Borrower ID").grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.borrow_book_id = ttk.Entry(self.borrow_tab)
        self.borrow_member_id = ttk.Entry(self.borrow_tab)

        self.borrow_book_id.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.borrow_member_id.grid(row=1, column=1, padx=10, pady=10, sticky="we")

        ttk.Button(self.borrow_tab, text="Borrow Book", command=self.borrow_book).grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        self.borrow_tab.grid_columnconfigure(1, weight=1)

    def setup_return_tab(self):
        ttk.Label(self.return_tab, text="Book ID").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.return_book_id = ttk.Entry(self.return_tab)
        self.return_book_id.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        ttk.Button(self.return_tab, text="Return Book", command=self.return_book).grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.return_tab.grid_columnconfigure(1, weight=1)

    def add_book(self):
        book_id = self.book_id.get()
        title = self.book_title.get()
        author = self.book_author.get()

        if not book_id or not title or not author:
            messagebox.showerror("Input Error", "All fields are required")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Books (BookID, Title, Author, Status) VALUES (?, ?, ?, 'Available')",
                               (book_id, title, author))
                conn.commit()
                messagebox.showinfo("Success", "Book added successfully")
                self.load_books()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Book ID already exists")

    def load_books(self):
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Books")
            rows = cursor.fetchall()

        self.book_tree.delete(*self.book_tree.get_children())
        for row in rows:
            self.book_tree.insert("", "end", values=row)

    def add_borrower(self):
        borrower_id = self.borrower_id.get()
        last_name = self.borrower_lastname.get()
        first_name = self.borrower_firstname.get()
        middle_name = self.borrower_middlename.get()
        course = self.borrower_course.get()
        contact = self.borrower_contact.get()

        if not borrower_id or not last_name or not first_name or not course or not contact:
            messagebox.showerror("Input Error", "All fields are required")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Borrowers (BorrowerID, LastName, FirstName, MiddleName, Course, ContactNumber) VALUES (?, ?, ?, ?, ?, ?)", (borrower_id, last_name, first_name, middle_name, course, contact))
                conn.commit()
                messagebox.showinfo("Success", "Borrower added successfully")
                self.load_borrowers()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Borrower ID already exists")

    def load_borrowers(self):
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Borrowers")
            rows = cursor.fetchall()

        self.borrower_tree.delete(*self.borrower_tree.get_children())
        for row in rows:
            self.borrower_tree.insert("", "end", values=row)

    def borrow_book(self):
        book_id = self.borrow_book_id.get()
        borrower_id = self.borrow_member_id.get()

        if not book_id or not borrower_id:
            messagebox.showerror("Input Error", "Both fields are required")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Borrow (BookID, BorrowerID) VALUES (?, ?)", (book_id, borrower_id))
                cursor.execute("UPDATE Books SET Status = 'Borrowed' WHERE BookID = ?", (book_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book borrowed successfully")
                self.load_books()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "This book is already borrowed or invalid Book/Borrower ID")

    def return_book(self):
        book_id = self.return_book_id.get()

        if not book_id:
            messagebox.showerror("Input Error", "Book ID is required")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Borrow WHERE BookID = ?", (book_id,))
            cursor.execute("UPDATE Books SET Status = 'Available' WHERE BookID = ?", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully")
            self.load_books()


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Register")
        self.root.geometry("400x300")

        self.setup_style()
        self.setup_ui()

    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('alt')

        # Define colors
        pastel_green = "#b6fcd5"
        pastel_yellow = "#fffac8"
        pastel_red = "#ffcccb"

        # Configure styles
        self.style.configure('TButton', font=('Arial', 10), padding=6, background=pastel_green)
        self.style.map('TButton', background=[('active', pastel_red)], foreground=[('active', 'black')])
        self.style.configure('TLabel', font=('Arial', 10), background=pastel_yellow)
        self.root.configure(bg=pastel_yellow)

    def setup_ui(self):
        self.username_label = ttk.Label(self.root, text="Username:")
        self.username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.pack(pady=10)

        self.password_label = ttk.Label(self.root, text="Password:")
        self.password_label.pack(pady=10)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ttk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = ttk.Button(self.root, text="Register", command=self.register)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Both fields are required")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
            row = cursor.fetchone()

        if row:
            self.root.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Input Error", "Both fields are required")
            return

        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "User registered successfully")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")


def main_app():
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()
