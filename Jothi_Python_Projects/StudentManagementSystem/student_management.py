# Student Management System
# A simple console project using Python and SQLite.
# This is a learning project, not a production login system.

import sqlite3
import hashlib
from pathlib import Path

DATABASE_FILE = Path(__file__).with_name("students.db")


def make_password_hash(password):
    # Store a hash instead of storing the password as plain text.
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def connect_database():
    return sqlite3.connect(DATABASE_FILE)


def create_tables():
    with connect_database() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('admin', 'staff'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                course TEXT NOT NULL,
                phone TEXT
            )
        """)

        # Add a demo admin account only when the users table is empty.
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ("admin", make_password_hash("admin123"), "admin")
            )


def register_user():
    print("\n--- Register a User ---")
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()
    role = input("Role (admin/staff): ").strip().lower()

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    if role not in ["admin", "staff"]:
        print("Please choose either admin or staff.")
        return

    try:
        with connect_database() as connection:
            connection.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, make_password_hash(password), role)
            )
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("That username already exists.")


def login():
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    password_hash = make_password_hash(password)

    with connect_database() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT username, role FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()

    if user is None:
        print("Incorrect username or password.")
        return None

    print("Welcome,", user[0] + "!")
    print("Your role is:", user[1])
    return {"username": user[0], "role": user[1]}


def add_student():
    print("\n--- Add Student ---")
    name = input("Student name: ").strip()
    age_text = input("Student age: ").strip()
    course = input("Course: ").strip()
    phone = input("Phone (optional): ").strip()

    if not name or not age_text or not course:
        print("Name, age, and course are required.")
        return

    try:
        age = int(age_text)
        if age <= 0:
            print("Age must be greater than zero.")
            return
    except ValueError:
        print("Please enter the age as a whole number.")
        return

    with connect_database() as connection:
        connection.execute(
            "INSERT INTO students (name, age, course, phone) VALUES (?, ?, ?, ?)",
            (name, age, course, phone)
        )

    print("Student added successfully.")


def view_students():
    with connect_database() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT student_id, name, age, course, phone FROM students ORDER BY student_id"
        )
        students = cursor.fetchall()

    print("\n--- Student List ---")
    if not students:
        print("No students have been added yet.")
        return

    print("-" * 65)
    print("{:<5} {:<20} {:<6} {:<18} {:<12}".format(
        "ID", "Name", "Age", "Course", "Phone"
    ))
    print("-" * 65)

    for student in students:
        print("{:<5} {:<20} {:<6} {:<18} {:<12}".format(
            student[0], student[1], student[2], student[3], student[4] or "-"
        ))


def update_student():
    view_students()
    student_id_text = input("\nEnter the ID to update: ").strip()

    try:
        student_id = int(student_id_text)
    except ValueError:
        print("Please enter a valid student ID.")
        return

    with connect_database() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,))
        if cursor.fetchone() is None:
            print("Student ID not found.")
            return

        name = input("New name: ").strip()
        age_text = input("New age: ").strip()
        course = input("New course: ").strip()
        phone = input("New phone (optional): ").strip()

        if not name or not age_text or not course:
            print("Name, age, and course are required.")
            return

        try:
            age = int(age_text)
            if age <= 0:
                print("Age must be greater than zero.")
                return
        except ValueError:
            print("Please enter the age as a whole number.")
            return

        cursor.execute(
            "UPDATE students SET name = ?, age = ?, course = ?, phone = ? WHERE student_id = ?",
            (name, age, course, phone, student_id)
        )

    print("Student details updated.")


def delete_student():
    view_students()
    student_id_text = input("\nEnter the ID to delete: ").strip()

    try:
        student_id = int(student_id_text)
    except ValueError:
        print("Please enter a valid student ID.")
        return

    confirm = input("Are you sure you want to delete this student? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Delete cancelled.")
        return

    with connect_database() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        if cursor.rowcount == 0:
            print("Student ID not found.")
        else:
            print("Student deleted successfully.")


def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. Add student")
        print("2. View students")
        print("3. Update student")
        print("4. Delete student")
        print("5. Register user")
        print("6. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            register_user()
        elif choice == "6":
            print("Logged out.")
            break
        else:
            print("Please choose a number from 1 to 6.")


def staff_menu():
    while True:
        print("\n=== Staff Menu (view only) ===")
        print("1. View students")
        print("2. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_students()
        elif choice == "2":
            print("Logged out.")
            break
        else:
            print("Please choose 1 or 2.")


def main():
    create_tables()
    print("Student Management System")
    print("First-time demo admin login: admin / admin123")

    while True:
        print("\nMain Menu")
        print("1. Login")
        print("2. Register user")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            user = login()
            if user is not None:
                if user["role"] == "admin":
                    admin_menu()
                else:
                    staff_menu()
        elif choice == "2":
            register_user()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except sqlite3.Error as error:
        print("A database problem occurred:", error)
