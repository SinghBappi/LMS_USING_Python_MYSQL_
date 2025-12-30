import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime
import time
import os
from tkinter import filedialog
import shutil

class LMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LMS Portal")
        self.root.geometry("1200x700")
        self.current_user = None
        
        # Create uploads directory if it doesn't exist
        self.uploads_dir = "assignment_uploads"
        if not os.path.exists(self.uploads_dir):
            os.makedirs(self.uploads_dir)
            
        self.connect_db()
        
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.show_login_screen()
    
    def connect_db(self):
        """Connect to MySQL database with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.connection = mysql.connector.connect(
                    host='localhost',
                    # user='root',
                    user='root',
                    # user='testuser',
                    port=3307,
                    # password='test123',
                    password='bappi',
                    database='test1'  # Changed to test1
                )
                if self.connection.is_connected():
                    print(f"Successfully connected to MySQL database 'test1' on port 3307")
                    return
            except Error as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    messagebox.showerror(
                        "Database Connection Error", 
                        f"Failed to connect after {max_retries} attempts.\n"
                        f"Error: {str(e)}\n\n"
                        "Please check:\n"
                        "• MySQL server is running\n"
                        "• Port 3307 is correct\n"
                        "• Database 'test1' exists\n"
                        "• Database credentials are valid"
                    )
                    self.root.quit()
    
    def ensure_connection(self):
        """Ensure database connection is active"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connect_db()
            return True
        except Error:
            return False
    
    def hash_password(self, password):
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def clear_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Show login screen"""
        self.clear_frame()
        
        # Title
        title_label = ttk.Label(self.main_frame, text="LMS Portal Login", 
                               font=('Arial', 20, 'bold'))
        title_label.pack(pady=20)
        
        # Login frame
        login_frame = ttk.Frame(self.main_frame)
        login_frame.pack(pady=50)
        
        # Username
        ttk.Label(login_frame, text="Username:", font=('Arial', 12)).grid(
            row=0, column=0, padx=10, pady=10, sticky='e')
        self.username_entry = ttk.Entry(login_frame, font=('Arial', 12), width=20)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Password
        ttk.Label(login_frame, text="Password:", font=('Arial', 12)).grid(
            row=1, column=0, padx=10, pady=10, sticky='e')
        self.password_entry = ttk.Entry(login_frame, font=('Arial', 12), 
                                       width=20, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Login button
        login_btn = ttk.Button(login_frame, text="Login", 
                              command=self.login, style='Accent.TButton')
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Register button
        register_btn = ttk.Button(login_frame, text="Register", 
                                 command=self.show_register_screen)
        register_btn.grid(row=3, column=0, columnspan=2)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
    
    def show_register_screen(self):
        """Show registration screen"""
        self.clear_frame()
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Register New Account", 
                               font=('Arial', 20, 'bold'))
        title_label.pack(pady=20)
        
        # Register frame
        register_frame = ttk.Frame(self.main_frame)
        register_frame.pack(pady=30)
        
        # Username
        ttk.Label(register_frame, text="Username:", font=('Arial', 12)).grid(
            row=0, column=0, padx=10, pady=10, sticky='e')
        self.reg_username_entry = ttk.Entry(register_frame, font=('Arial', 12), width=20)
        self.reg_username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Email
        ttk.Label(register_frame, text="Email:", font=('Arial', 12)).grid(
            row=1, column=0, padx=10, pady=10, sticky='e')
        self.reg_email_entry = ttk.Entry(register_frame, font=('Arial', 12), width=20)
        self.reg_email_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Password
        ttk.Label(register_frame, text="Password:", font=('Arial', 12)).grid(
            row=2, column=0, padx=10, pady=10, sticky='e')
        self.reg_password_entry = ttk.Entry(register_frame, font=('Arial', 12), 
                                           width=20, show='*')
        self.reg_password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Role
        ttk.Label(register_frame, text="Role:", font=('Arial', 12)).grid(
            row=3, column=0, padx=10, pady=10, sticky='e')
        self.role_var = tk.StringVar(value='student')
        role_combo = ttk.Combobox(register_frame, textvariable=self.role_var,
                                 values=['student', 'instructor'], state='readonly',
                                 font=('Arial', 12), width=18)
        role_combo.grid(row=3, column=1, padx=10, pady=10)
        
        # Buttons
        btn_frame = ttk.Frame(register_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        register_btn = ttk.Button(btn_frame, text="Register", 
                                 command=self.register_user)
        register_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = ttk.Button(btn_frame, text="Back to Login", 
                             command=self.show_login_screen)
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def login(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        hashed_password = self.hash_password(password)
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()
            
            if user:
                self.current_user = user
                messagebox.showinfo("Success", f"Welcome {user['username']}!")
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials!")
        except Error as e:
            messagebox.showerror("Database Error", f"Error during login: {e}")
    
    def register_user(self):
        """Handle user registration"""
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        role = self.role_var.get()
        
        if not all([username, email, password]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        hashed_password = self.hash_password(password)
        
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, email, hashed_password, role))
            self.connection.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.show_login_screen()
        except Error as e:
            messagebox.showerror("Database Error", f"Error during registration: {e}")
    
    def show_dashboard(self):
        """Show main dashboard based on user role"""
        self.clear_frame()
        
        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        welcome_label = ttk.Label(header_frame, 
                                 text=f"Welcome, {self.current_user['username']} ({self.current_user['role'].title()})",
                                 font=('Arial', 16, 'bold'))
        welcome_label.pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(header_frame, text="Logout", 
                               command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Create tabs based on user role
        if self.current_user['role'] == 'student':
            self.create_student_tabs()
        elif self.current_user['role'] == 'instructor':
            self.create_instructor_tabs()
        elif self.current_user['role'] == 'admin':
            self.create_admin_tabs()
    
    def create_student_tabs(self):
        """Create tabs for student"""
        # Courses Tab
        courses_tab = ttk.Frame(self.notebook)
        self.notebook.add(courses_tab, text="Available Courses")
        self.setup_courses_tab(courses_tab)
        
        # My Courses Tab
        my_courses_tab = ttk.Frame(self.notebook)
        self.notebook.add(my_courses_tab, text="My Courses")
        self.setup_my_courses_tab(my_courses_tab)
        
        # Assignments Tab
        assignments_tab = ttk.Frame(self.notebook)
        self.notebook.add(assignments_tab, text="Assignments")
        self.setup_assignments_tab(assignments_tab)
        
        # Grades Tab
        grades_tab = ttk.Frame(self.notebook)
        self.notebook.add(grades_tab, text="My Grades")
        self.setup_grades_tab(grades_tab)
    
    def create_instructor_tabs(self):
        """Create tabs for instructor"""
        # My Courses Tab
        my_courses_tab = ttk.Frame(self.notebook)
        self.notebook.add(my_courses_tab, text="My Courses")
        self.setup_instructor_courses_tab(my_courses_tab)
        
        # Create Course Tab
        create_course_tab = ttk.Frame(self.notebook)
        self.notebook.add(create_course_tab, text="Create Course")
        self.setup_create_course_tab(create_course_tab)
        
        # Assignments Tab
        assignments_tab = ttk.Frame(self.notebook)
        self.notebook.add(assignments_tab, text="Assignments")
        self.setup_instructor_assignments_tab(assignments_tab)
        
        # View Submissions Tab
        submissions_tab = ttk.Frame(self.notebook)
        self.notebook.add(submissions_tab, text="View Submissions")
        self.setup_instructor_submissions_tab(submissions_tab)
    
    def create_admin_tabs(self):
        """Create tabs for admin"""
        # Users Tab
        users_tab = ttk.Frame(self.notebook)
        self.notebook.add(users_tab, text="Manage Users")
        self.setup_users_tab(users_tab)
        
        # Courses Tab
        courses_tab = ttk.Frame(self.notebook)
        self.notebook.add(courses_tab, text="All Courses")
        self.setup_admin_courses_tab(courses_tab)

    # ========== STUDENT METHODS ==========
    
    def setup_courses_tab(self, parent):
        """Setup available courses tab for students"""
        # Refresh button
        refresh_btn = ttk.Button(parent, text="Refresh", 
                                command=lambda: self.load_courses(tree))
        refresh_btn.pack(pady=10)
        
        # Treeview for courses
        columns = ('ID', 'Title', 'Instructor', 'Description')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.column('Description', width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enroll button
        enroll_btn = ttk.Button(parent, text="Enroll in Selected Course", 
                               command=lambda: self.enroll_course(tree))
        enroll_btn.pack(pady=10)
        
        self.load_courses(tree)
    
    def load_courses(self, tree):
        """Load courses into treeview"""
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT c.*, u.username as instructor_name 
                FROM courses c 
                JOIN users u ON c.instructor_id = u.id
            """
            cursor.execute(query)
            courses = cursor.fetchall()
            
            for course in courses:
                tree.insert('', tk.END, values=(
                    course['id'],
                    course['title'],
                    course['instructor_name'],
                    course['description']
                ))
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading courses: {e}")
    
    def enroll_course(self, tree):
        """Enroll student in selected course"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to enroll")
            return
        
        course_id = tree.item(selected[0])['values'][0]
        
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)"
            cursor.execute(query, (self.current_user['id'], course_id))
            self.connection.commit()
            messagebox.showinfo("Success", "Enrolled in course successfully!")
        except Error as e:
            messagebox.showerror("Database Error", f"Error enrolling: {e}")
    
    def setup_my_courses_tab(self, parent):
        """Setup my courses tab for students"""
        # Treeview for enrolled courses
        columns = ('ID', 'Title', 'Instructor', 'Description')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.column('Description', width=300)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load data
        self.load_my_courses(tree)
    
    def load_my_courses(self, tree):
        """Load student's enrolled courses"""
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT c.*, u.username as instructor_name 
                FROM courses c 
                JOIN enrollments e ON c.id = e.course_id 
                JOIN users u ON c.instructor_id = u.id
                WHERE e.student_id = %s
            """
            cursor.execute(query, (self.current_user['id'],))
            courses = cursor.fetchall()
            
            for course in courses:
                tree.insert('', tk.END, values=(
                    course['id'],
                    course['title'],
                    course['instructor_name'],
                    course['description']
                ))
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading courses: {e}")
    
    def setup_assignments_tab(self, parent):
        """Setup assignments tab for students with file upload"""
        # Treeview for assignments
        columns = ('ID', 'Course', 'Title', 'Due Date', 'Description')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.column('Description', width=200)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Submission frame
        submission_frame = ttk.LabelFrame(parent, text="Submit Assignment", padding=10)
        submission_frame.pack(fill=tk.X, pady=10)
        
        # Text submission
        ttk.Label(submission_frame, text="Submission Text:").pack(anchor='w', pady=5)
        self.submission_text = scrolledtext.ScrolledText(submission_frame, height=4, width=80)
        self.submission_text.pack(pady=5, fill=tk.X)
        
        # File upload
        file_frame = ttk.Frame(submission_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Upload File:").pack(side=tk.LEFT, padx=5)
        self.file_path_label = ttk.Label(file_frame, text="No file selected")
        self.file_path_label.pack(side=tk.LEFT, padx=5)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        submit_btn = ttk.Button(submission_frame, text="Submit Assignment", 
                               command=lambda: self.submit_assignment(tree))
        submit_btn.pack(pady=10)
        
        self.load_student_assignments(tree)
        self.selected_file_path = None

    def browse_file(self):
        """Browse and select file for upload"""
        file_path = filedialog.askopenfilename(
            title="Select assignment file",
            filetypes=[("All files", "*.*"), ("PDF files", "*.pdf"), 
                      ("Word documents", "*.docx"), ("Text files", "*.txt")]
        )
        if file_path:
            self.selected_file_path = file_path
            self.file_path_label.config(text=os.path.basename(file_path))

    def submit_assignment(self, tree):
        """Submit assignment for student with file upload"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an assignment")
            return
        
        assignment_id = tree.item(selected[0])['values'][0]
        submission_text = self.submission_text.get('1.0', tk.END).strip()
        
        if not submission_text and not self.selected_file_path:
            messagebox.showwarning("Warning", "Please enter submission text or upload a file")
            return
        
        try:
            # Handle file upload
            file_path_in_db = None
            if self.selected_file_path:
                # Create unique filename
                filename = f"assignment_{assignment_id}_student_{self.current_user['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(self.selected_file_path)}"
                destination_path = os.path.join(self.uploads_dir, filename)
                
                # Copy file to uploads directory
                shutil.copy2(self.selected_file_path, destination_path)
                file_path_in_db = destination_path
            
            cursor = self.connection.cursor()
            query = """
                INSERT INTO submissions (assignment_id, student_id, submission_text, file_path) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (assignment_id, self.current_user['id'], submission_text, file_path_in_db))
            self.connection.commit()
            
            messagebox.showinfo("Success", "Assignment submitted successfully!")
            self.submission_text.delete('1.0', tk.END)
            self.file_path_label.config(text="No file selected")
            self.selected_file_path = None
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error submitting assignment: {e}")

    def load_student_assignments(self, tree):
        """Load assignments for student"""
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT a.*, c.title as course_title 
                FROM assignments a 
                JOIN courses c ON a.course_id = c.id 
                JOIN enrollments e ON c.id = e.course_id 
                WHERE e.student_id = %s
            """
            cursor.execute(query, (self.current_user['id'],))
            assignments = cursor.fetchall()
            
            for assignment in assignments:
                tree.insert('', tk.END, values=(
                    assignment['id'],
                    assignment['course_title'],
                    assignment['title'],
                    assignment['due_date'],
                    assignment['description']
                ))
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading assignments: {e}")

    def setup_grades_tab(self, parent):
        """Setup grades tab for students"""
        # Treeview for grades
        columns = ('Assignment', 'Course', 'Submitted Date', 'Score', 'Max Score', 'Status')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.column('Assignment', width=150)
        tree.column('Course', width=120)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load grades
        self.load_student_grades(tree)

    def load_student_grades(self, tree):
        """Load student's grades and submissions"""
        if not self.ensure_connection():
            return
            
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT s.*, a.title as assignment_title, a.max_score, 
                       c.title as course_title, a.due_date
                FROM submissions s
                JOIN assignments a ON s.assignment_id = a.id
                JOIN courses c ON a.course_id = c.id
                WHERE s.student_id = %s
                ORDER BY s.submitted_at DESC
            """
            cursor.execute(query, (self.current_user['id'],))
            submissions = cursor.fetchall()
        
            for submission in submissions:
                status = "Graded" if submission['score'] is not None else "Submitted"
                score = submission['score'] if submission['score'] is not None else "Not graded"
                
                tree.insert('', tk.END, values=(
                    submission['assignment_title'],
                    submission['course_title'],
                    submission['submitted_at'],
                    score,
                    submission['max_score'],
                    status
                ))
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading grades: {e}")

    # ========== INSTRUCTOR METHODS ==========
    
    def setup_instructor_courses_tab(self, parent):
        """Setup courses tab for instructor"""
        # Treeview for instructor's courses
        columns = ('ID', 'Title', 'Description', 'Created At')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.load_instructor_courses(tree)
    
    def load_instructor_courses(self, tree):
        """Load instructor's courses"""
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM courses WHERE instructor_id = %s"
            cursor.execute(query, (self.current_user['id'],))
            courses = cursor.fetchall()
            
            for course in courses:
                tree.insert('', tk.END, values=(
                    course['id'],
                    course['title'],
                    course['description'],
                    course['created_at']
                ))
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading courses: {e}")
    
    def setup_create_course_tab(self, parent):
        """Setup create course tab for instructor"""
        form_frame = ttk.Frame(parent)
        form_frame.pack(pady=50)
        
        # Title
        ttk.Label(form_frame, text="Course Title:", font=('Arial', 12)).grid(
            row=0, column=0, padx=10, pady=10, sticky='e')
        self.course_title_entry = ttk.Entry(form_frame, font=('Arial', 12), width=30)
        self.course_title_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Description
        ttk.Label(form_frame, text="Description:", font=('Arial', 12)).grid(
            row=1, column=0, padx=10, pady=10, sticky='ne')
        self.course_desc_text = scrolledtext.ScrolledText(form_frame, 
                                                         height=5, width=30)
        self.course_desc_text.grid(row=1, column=1, padx=10, pady=10)
        
        # Create button
        create_btn = ttk.Button(form_frame, text="Create Course", 
                               command=self.create_course)
        create_btn.grid(row=2, column=0, columnspan=2, pady=20)
    
    def create_course(self):
        """Create a new course"""
        title = self.course_title_entry.get().strip()
        description = self.course_desc_text.get('1.0', tk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter course title")
            return
        
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO courses (title, description, instructor_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (title, description, self.current_user['id']))
            self.connection.commit()
            messagebox.showinfo("Success", "Course created successfully!")
            self.course_title_entry.delete(0, tk.END)
            self.course_desc_text.delete('1.0', tk.END)
        except Error as e:
            messagebox.showerror("Database Error", f"Error creating course: {e}")

    def setup_instructor_assignments_tab(self, parent):
        """Setup complete assignments tab for instructor"""
        # Main frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Create Assignment
        create_frame = ttk.LabelFrame(main_frame, text="Create New Assignment", padding=10)
        create_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Course selection
        ttk.Label(create_frame, text="Course:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.course_var = tk.StringVar()
        self.course_combo = ttk.Combobox(create_frame, textvariable=self.course_var, state='readonly')
        self.course_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        # Assignment title
        ttk.Label(create_frame, text="Title:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.assignment_title_entry = ttk.Entry(create_frame, width=40)
        self.assignment_title_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Due date
        ttk.Label(create_frame, text="Due Date:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.due_date_entry = ttk.Entry(create_frame, width=40)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.due_date_entry.insert(0, "YYYY-MM-DD")
        
        # Description
        ttk.Label(create_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky='ne')
        self.assignment_desc_text = scrolledtext.ScrolledText(create_frame, height=4, width=40)
        self.assignment_desc_text.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        
        # Max score
        ttk.Label(create_frame, text="Max Score:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.max_score_entry = ttk.Entry(create_frame, width=40)
        self.max_score_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        self.max_score_entry.insert(0, "100")
        
        # Create button
        create_btn = ttk.Button(create_frame, text="Create Assignment", 
                               command=self.create_assignment)
        create_btn.grid(row=5, column=1, pady=10, sticky='e')
        
        # Right side - Existing Assignments
        list_frame = ttk.LabelFrame(main_frame, text="Existing Assignments", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for assignments
        columns = ('ID', 'Course', 'Title', 'Due Date', 'Max Score', 'Submissions')
        self.assignments_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.assignments_tree.heading(col, text=col)
            self.assignments_tree.column(col, width=100)
        
        self.assignments_tree.column('Title', width=150)
        self.assignments_tree.column('Course', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.assignments_tree.yview)
        self.assignments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.assignments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load data
        self.load_instructor_courses_combo()
        self.load_instructor_assignments()
    
    def load_instructor_courses_combo(self):
        """Load instructor's courses into combo box"""
        if not self.ensure_connection():
            return
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, title FROM courses WHERE instructor_id = %s"
            cursor.execute(query, (self.current_user['id'],))
            courses = cursor.fetchall()
            
            course_list = [f"{course['id']}: {course['title']}" for course in courses]
            self.course_combo['values'] = course_list
            
            if course_list:
                self.course_combo.set(course_list[0])
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading courses: {e}")

    def create_assignment(self):
        """Create a new assignment"""
        if not self.ensure_connection():
            return
            
        course_selection = self.course_var.get()
        title = self.assignment_title_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        description = self.assignment_desc_text.get('1.0', tk.END).strip()
        max_score = self.max_score_entry.get().strip()
        
        if not all([course_selection, title, due_date]):
            messagebox.showwarning("Warning", "Please fill all required fields")
            return
        
        try:
            # Extract course ID from selection
            course_id = course_selection.split(':')[0]
            
            cursor = self.connection.cursor()
            query = """
                INSERT INTO assignments (course_id, title, description, due_date, max_score) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (course_id, title, description, due_date, max_score))
            self.connection.commit()
            
            messagebox.showinfo("Success", "Assignment created successfully!")
            self.clear_assignment_form()
            self.load_instructor_assignments()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error creating assignment: {e}")

    def clear_assignment_form(self):
        """Clear the assignment creation form"""
        self.assignment_title_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, "YYYY-MM-DD")
        self.assignment_desc_text.delete('1.0', tk.END)
        self.max_score_entry.delete(0, tk.END)
        self.max_score_entry.insert(0, "100")

    def load_instructor_assignments(self):
        """Load instructor's assignments"""
        if not self.ensure_connection():
            return
            
        # Clear existing data
        for item in self.assignments_tree.get_children():
            self.assignments_tree.delete(item)
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT a.*, c.title as course_title,
                (SELECT COUNT(*) FROM submissions s WHERE s.assignment_id = a.id) as submission_count
                FROM assignments a 
                JOIN courses c ON a.course_id = c.id 
                WHERE c.instructor_id = %s
                ORDER BY a.created_at DESC
            """
            cursor.execute(query, (self.current_user['id'],))
            assignments = cursor.fetchall()
            
            for assignment in assignments:
                self.assignments_tree.insert('', tk.END, values=(
                    assignment['id'],
                    assignment['course_title'],
                    assignment['title'],
                    assignment['due_date'],
                    assignment['max_score'],
                    assignment['submission_count']
                ))
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading assignments: {e}")

    def setup_instructor_submissions_tab(self, parent):
        """Setup tab for instructors to view student submissions"""
        # Main frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(control_frame, text="Select Assignment:").pack(side=tk.LEFT, padx=5)
        
        self.submission_assignment_var = tk.StringVar()
        self.submission_assignment_combo = ttk.Combobox(control_frame, 
                                                       textvariable=self.submission_assignment_var, 
                                                       state='readonly', width=40)
        self.submission_assignment_combo.pack(side=tk.LEFT, padx=5)
        self.submission_assignment_combo.bind('<<ComboboxSelected>>', self.load_submissions)
        
        refresh_btn = ttk.Button(control_frame, text="Refresh", 
                                command=self.load_instructor_assignments_combo)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview for submissions
        columns = ('ID', 'Student', 'Submitted Date', 'Score', 'File', 'Status')
        self.submissions_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.submissions_tree.heading(col, text=col)
            self.submissions_tree.column(col, width=120)
        
        self.submissions_tree.column('Student', width=150)
        self.submissions_tree.column('File', width=200)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.submissions_tree.yview)
        self.submissions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.submissions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Grade frame
        grade_frame = ttk.LabelFrame(main_frame, text="Grade Submission", padding=10)
        grade_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(grade_frame, text="Score:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.grade_score_entry = ttk.Entry(grade_frame, width=10)
        self.grade_score_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(grade_frame, text="/").grid(row=0, column=2, padx=5, pady=5)
        
        self.max_score_label = ttk.Label(grade_frame, text="100")
        self.max_score_label.grid(row=0, column=3, padx=5, pady=5)
        
        grade_btn = ttk.Button(grade_frame, text="Submit Grade", command=self.submit_grade)
        grade_btn.grid(row=0, column=4, padx=10, pady=5)
        
        # View file button
        view_file_btn = ttk.Button(grade_frame, text="View Submission File", 
                                  command=self.view_submission_file)
        view_file_btn.grid(row=0, column=5, padx=10, pady=5)
        
        # Load assignments
        self.load_instructor_assignments_combo()

    def load_instructor_assignments_combo(self):
        """Load instructor's assignments into combo box for submissions"""
        if not self.ensure_connection():
            return
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT a.*, c.title as course_title 
                FROM assignments a 
                JOIN courses c ON a.course_id = c.id 
                WHERE c.instructor_id = %s
                ORDER BY a.created_at DESC
            """
            cursor.execute(query, (self.current_user['id'],))
            assignments = cursor.fetchall()
            
            assignment_list = [f"{assignment['id']}: {assignment['course_title']} - {assignment['title']}" 
                             for assignment in assignments]
            self.submission_assignment_combo['values'] = assignment_list
            
            if assignment_list:
                self.submission_assignment_combo.set(assignment_list[0])
                self.load_submissions()
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading assignments: {e}")

    def load_submissions(self, event=None):
        """Load submissions for selected assignment"""
        if not self.ensure_connection():
            return
            
        # Clear existing data
        for item in self.submissions_tree.get_children():
            self.submissions_tree.delete(item)
        
        assignment_selection = self.submission_assignment_var.get()
        if not assignment_selection:
            return
        
        try:
            assignment_id = assignment_selection.split(':')[0]
            
            # Get max score for the assignment
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT max_score FROM assignments WHERE id = %s"
            cursor.execute(query, (assignment_id,))
            assignment = cursor.fetchone()
            self.max_score_label.config(text=str(assignment['max_score']))
            
            # Get submissions
            query = """
                SELECT s.*, u.username as student_name, a.max_score
                FROM submissions s
                JOIN users u ON s.student_id = u.id
                JOIN assignments a ON s.assignment_id = a.id
                WHERE s.assignment_id = %s
                ORDER BY s.submitted_at DESC
            """
            cursor.execute(query, (assignment_id,))
            submissions = cursor.fetchall()
            
            for submission in submissions:
                has_file = "Yes" if submission['file_path'] else "No"
                status = "Graded" if submission['score'] is not None else "Pending"
                score = submission['score'] if submission['score'] is not None else "Not graded"
                
                self.submissions_tree.insert('', tk.END, values=(
                    submission['id'],
                    submission['student_name'],
                    submission['submitted_at'],
                    score,
                    has_file,
                    status
                ), tags=(submission['id'],))
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading submissions: {e}")

    def view_submission_file(self):
        """View the submitted file"""
        selected = self.submissions_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a submission")
            return
        
        submission_id = self.submissions_tree.item(selected[0])['tags'][0]
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT file_path FROM submissions WHERE id = %s"
            cursor.execute(query, (submission_id,))
            submission = cursor.fetchone()
            
            if submission['file_path'] and os.path.exists(submission['file_path']):
                os.startfile(submission['file_path'])  # This will open the file with default application
            else:
                messagebox.showinfo("Info", "No file was submitted for this assignment")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error viewing file: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def submit_grade(self):
        """Submit grade for selected submission"""
        selected = self.submissions_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a submission to grade")
            return
        
        submission_id = self.submissions_tree.item(selected[0])['tags'][0]
        score = self.grade_score_entry.get().strip()
        
        if not score:
            messagebox.showwarning("Warning", "Please enter a score")
            return
        
        try:
            score = float(score)
            cursor = self.connection.cursor()
            query = "UPDATE submissions SET score = %s WHERE id = %s"
            cursor.execute(query, (score, submission_id))
            self.connection.commit()
            
            messagebox.showinfo("Success", "Grade submitted successfully!")
            self.grade_score_entry.delete(0, tk.END)
            self.load_submissions()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for score")
        except Error as e:
            messagebox.showerror("Database Error", f"Error submitting grade: {e}")

    # ========== ADMIN METHODS ==========
    
    def setup_users_tab(self, parent):
        """Setup complete users management tab for admin with CRUD operations"""
        # Control frame
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Refresh button
        refresh_btn = ttk.Button(control_frame, text="Refresh", 
                                command=lambda: self.load_all_users(self.users_tree))
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Add user button
        add_user_btn = ttk.Button(control_frame, text="Add New User", 
                                 command=self.show_add_user_dialog)
        add_user_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview for users
        columns = ('ID', 'Username', 'Email', 'Role', 'Created At')
        self.users_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=120)
        
        self.users_tree.column('Email', width=150)
        self.users_tree.column('Username', width=100)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons frame
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill=tk.X, pady=10)
        
        edit_btn = ttk.Button(action_frame, text="Edit Selected User", 
                             command=self.edit_user)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(action_frame, text="Delete Selected User", 
                               command=self.delete_user)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Load users
        self.load_all_users(self.users_tree)

    def load_all_users(self, tree):
        """Load all users for admin"""
        if not self.ensure_connection():
            return
            
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users ORDER BY created_at DESC"
            cursor.execute(query)
            users = cursor.fetchall()
            
            for user in users:
                tree.insert('', tk.END, values=(
                    user['id'],
                    user['username'],
                    user['email'],
                    user['role'],
                    user['created_at']
                ))
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading users: {e}")

    def delete_user(self):
        """Delete selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        user_id = self.users_tree.item(selected[0])['values'][0]
        username = self.users_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?"):
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM users WHERE id = %s"
                cursor.execute(query, (user_id,))
                self.connection.commit()
                
                messagebox.showinfo("Success", "User deleted successfully!")
                self.load_all_users(self.users_tree)
                
            except Error as e:
                messagebox.showerror("Database Error", f"Error deleting user: {e}")

    def show_add_user_dialog(self):
        """Show dialog to add new user"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        username_entry = ttk.Entry(form_frame, width=20)
        username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        email_entry = ttk.Entry(form_frame, width=20)
        email_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        password_entry = ttk.Entry(form_frame, width=20, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        ttk.Label(form_frame, text="Role:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        role_var = tk.StringVar(value='student')
        role_combo = ttk.Combobox(form_frame, textvariable=role_var,
                                 values=['student', 'instructor', 'admin'], state='readonly')
        role_combo.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        def add_user():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get()
            
            if not all([username, email, password]):
                messagebox.showwarning("Warning", "Please fill all fields")
                return
            
            hashed_password = self.hash_password(password)
            
            try:
                cursor = self.connection.cursor()
                query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, email, hashed_password, role))
                self.connection.commit()
                
                messagebox.showinfo("Success", "User added successfully!")
                dialog.destroy()
                self.load_all_users(self.users_tree)
                
            except Error as e:
                messagebox.showerror("Database Error", f"Error adding user: {e}")
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        add_btn = ttk.Button(btn_frame, text="Add User", command=add_user)
        add_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def edit_user(self):
        """Edit selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return
        
        user_id = self.users_tree.item(selected[0])['values'][0]
        username = self.users_tree.item(selected[0])['values'][1]
        email = self.users_tree.item(selected[0])['values'][2]
        role = self.users_tree.item(selected[0])['values'][3]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit User")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        username_entry = ttk.Entry(form_frame, width=20)
        username_entry.insert(0, username)
        username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        email_entry = ttk.Entry(form_frame, width=20)
        email_entry.insert(0, email)
        email_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        ttk.Label(form_frame, text="New Password (leave blank to keep current):").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        password_entry = ttk.Entry(form_frame, width=20, show='*')
        password_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        ttk.Label(form_frame, text="Role:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        role_var = tk.StringVar(value=role)
        role_combo = ttk.Combobox(form_frame, textvariable=role_var,
                                 values=['student', 'instructor', 'admin'], state='readonly')
        role_combo.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        def update_user():
            new_username = username_entry.get().strip()
            new_email = email_entry.get().strip()
            new_password = password_entry.get().strip()
            new_role = role_var.get()
            
            if not all([new_username, new_email]):
                messagebox.showwarning("Warning", "Please fill all required fields")
                return
            
            try:
                cursor = self.connection.cursor()
                if new_password:
                    hashed_password = self.hash_password(new_password)
                    query = "UPDATE users SET username = %s, email = %s, password = %s, role = %s WHERE id = %s"
                    cursor.execute(query, (new_username, new_email, hashed_password, new_role, user_id))
                else:
                    query = "UPDATE users SET username = %s, email = %s, role = %s WHERE id = %s"
                    cursor.execute(query, (new_username, new_email, new_role, user_id))
                
                self.connection.commit()
                
                messagebox.showinfo("Success", "User updated successfully!")
                dialog.destroy()
                self.load_all_users(self.users_tree)
                
            except Error as e:
                messagebox.showerror("Database Error", f"Error updating user: {e}")
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        update_btn = ttk.Button(btn_frame, text="Update User", command=update_user)
        update_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def setup_admin_courses_tab(self, parent):
        """Setup courses management tab for admin"""
        ttk.Label(parent, text="Course Management - To be implemented", 
                 font=('Arial', 14)).pack(pady=50)
    
    def logout(self):
        """Logout user"""
        self.current_user = None
        self.show_login_screen()

def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Arial', 12, 'bold'))
    
    app = LMSApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()