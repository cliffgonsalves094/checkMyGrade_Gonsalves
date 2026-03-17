import csv
import hashlib
import os
import time

from models.course import Course
from models.professor import Professor
from models.student import Student
from structures.linked_list import LinkedList
from utils.csv_handler import append_to_csv, load_from_csv, save_to_csv

STUDENT_FILE = "data/students.csv"
COURSE_FILE = "data/Course.csv"
PROFESSOR_FILE = "data/Professor.csv"
LOGIN_FILE = "data/Login.csv"
LOGIN_HEADERS = ["User_id", "Password", "role"]

students = LinkedList()
courses = LinkedList()
professors = LinkedList()


# Load existing students
loaded_students = load_from_csv(STUDENT_FILE, Student)

for s in loaded_students:
    students.append(s)


# Load existing courses
loaded_courses = load_from_csv(COURSE_FILE, Course)

for c in loaded_courses:
    courses.append(c)


# Load existing professors
loaded_professors = load_from_csv(PROFESSOR_FILE, Professor)

for p in loaded_professors:
    professors.append(p)


def hash_password(user_id, password):
    raw = f"{user_id}:{password}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_logins():
    if not os.path.exists(LOGIN_FILE) or os.path.getsize(LOGIN_FILE) == 0:
        return []

    with open(LOGIN_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def register_user():
    user_id = input("User ID (email recommended): ").strip()
    if not user_id:
        print("User ID is required")
        return

    role_choice = input("Role (student/professor): ").strip().lower()
    if role_choice not in {"student", "professor", "admin"}:
        print("Invalid role")
        return

    password = input("Password: ")

    logins = load_logins()
    for row in logins:
        if row.get("User_id") == user_id and row.get("role") == role_choice:
            print("User already exists")
            return

    password_hash = hash_password(user_id, password)
    append_to_csv(LOGIN_FILE, [user_id, password_hash, role_choice], LOGIN_HEADERS)
    print("Registration successful")


def login(role):
    user_id = input("User ID: ").strip()
    password = input("Password: ")
    password_hash = hash_password(user_id, password)

    for row in load_logins():
        if row.get("User_id") == user_id and row.get("role") == role:
            if row.get("Password") == password_hash:
                print(f"Logged in as {role}")
                return True, user_id
            print("Incorrect password")
            return False, None

    print("User not found")
    return False, None


def export_all_to_folder(folder_name):
    if not folder_name:
        print("Folder name is required")
        return
    export_dir = os.path.join(os.getcwd(), folder_name)
    os.makedirs(export_dir, exist_ok=True)

    save_to_csv(os.path.join(export_dir, "students.csv"), students.to_list())
    save_to_csv(os.path.join(export_dir, "Course.csv"), courses.to_list())
    save_to_csv(os.path.join(export_dir, "Professor.csv"), professors.to_list())

    logins = load_logins()
    with open(os.path.join(export_dir, "Login.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(LOGIN_HEADERS)
        for row in logins:
            writer.writerow(
                [
                    row.get("User_id", ""),
                    row.get("Password", ""),
                    row.get("role", ""),
                ]
            )

    print(f"Exported all CSVs to {export_dir}")


def display_list(items):
    for item in items:
        print(", ".join(str(part) for part in item.to_list()))


def manage_courses():
    while True:
        print("\nCourse Menu")
        print("1 Add Course")
        print("2 Display Courses")
        print("3 Modify Course")
        print("4 Delete Course")
        print("0 Back")

        choice = input("Choice: ")

        if choice == "1":
            course_id = input("Course ID: ")
            course_name = input("Course name: ")
            description = input("Description: ")
            courses.append(Course(course_id, course_name, description))
            print("Course added")
        elif choice == "2":
            display_list(courses.to_list())
        elif choice == "3":
            course_id = input("Course ID to modify: ")
            course = courses.find_first(lambda c: c.course_id == course_id)
            if not course:
                print("Course not found")
                continue
            print("Press Enter to keep the current value.")
            course_name = input(f"Course name ({course.course_name}): ").strip()
            description = input(f"Description ({course.description}): ").strip()
            if course_name:
                course.course_name = course_name
            if description:
                course.description = description
            print("Course updated")
        elif choice == "4":
            course_id = input("Course ID to delete: ")
            if courses.remove_first(lambda c: c.course_id == course_id):
                print("Course deleted")
            else:
                print("Course not found")
        elif choice == "0":
            return
        else:
            print("Invalid choice")


def manage_professors():
    while True:
        print("\nProfessor Menu")
        print("1 Add Professor")
        print("2 Display Professors")
        print("3 Modify Professor")
        print("4 Delete Professor")
        print("0 Back")

        choice = input("Choice: ")

        if choice == "1":
            professor_id = input("Professor ID: ")
            name = input("Professor name: ")
            rank = input("Rank: ")
            course_id = input("Course ID: ")
            professors.append(Professor(professor_id, name, rank, course_id))
            print("Professor added")
        elif choice == "2":
            display_list(professors.to_list())
        elif choice == "3":
            professor_id = input("Professor ID to modify: ")
            professor = professors.find_first(
                lambda p: p.professor_id == professor_id
            )
            if not professor:
                print("Professor not found")
                continue
            print("Press Enter to keep the current value.")
            name = input(f"Professor name ({professor.name}): ").strip()
            rank = input(f"Rank ({professor.rank}): ").strip()
            course_id = input(f"Course ID ({professor.course_id}): ").strip()
            if name:
                professor.name = name
            if rank:
                professor.rank = rank
            if course_id:
                professor.course_id = course_id
            print("Professor updated")
        elif choice == "4":
            professor_id = input("Professor ID to delete: ")
            if professors.remove_first(
                lambda p: p.professor_id == professor_id
            ):
                print("Professor deleted")
            else:
                print("Professor not found")
        elif choice == "0":
            return
        else:
            print("Invalid choice")


logged_in_role = None
logged_in_user_id = None

while True:
    print("\nLogin Menu")
    print("1 Login as Student")
    print("2 Login as Professor")
    print("3 Register")
    print("4 Admin Login")
    print("0 Exit")

    login_choice = input("Choice: ")

    if login_choice == "1":
        ok, user_id = login("student")
        if ok:
            logged_in_role = "student"
            logged_in_user_id = user_id
            break
    elif login_choice == "2":
        ok, user_id = login("professor")
        if ok:
            logged_in_role = "professor"
            logged_in_user_id = user_id
            break
    elif login_choice == "3":
        register_user()
    elif login_choice == "4":
        ok, user_id = login("admin")
        if ok:
            logged_in_role = "admin"
            logged_in_user_id = user_id
            break
    elif login_choice == "0":
        raise SystemExit
    else:
        print("Invalid choice")


def student_menu():
    while True:
        print("\nStudent Menu")
        print("1 View All Courses")
        print("2 View All Professors")
        print("3 View My Details")
        print("0 Exit")

        choice = input("Choice: ")

        if choice == "1":
            display_list(courses.to_list())
        elif choice == "2":
            display_list(professors.to_list())
        elif choice == "3":
            student = students.find_first(lambda s: s.email == logged_in_user_id)
            if student:
                print(", ".join(str(part) for part in student.to_list()))
            else:
                print("Student record not found")
        elif choice == "0":
            return
        else:
            print("Invalid choice")


def professor_menu():
    grade_order = {
        "A+": 0,
        "A": 1,
        "A-": 2,
        "B+": 3,
        "B": 4,
        "B-": 5,
        "C+": 6,
        "C": 7,
        "C-": 8,
        "D": 9,
        "F": 10,
    }

    def save_report(prompt, content_lines):
        choice = input("Save report to file? (y/n): ").strip().lower()
        if choice != "y":
            return
        filename = input(prompt).strip()
        if not filename:
            print("Filename is required")
            return
        with open(filename, "w", newline="") as f:
            for line in content_lines:
                f.write(f"{line}\n")
        print(f"Report saved to {filename}")

    while True:
        print("\nProfessor Menu")
        print("1 View Sorted Results by Grade (Course)")
        print("2 Search Student Records")
        print("3 Course Statistics (Average/Median)")
        print("4 Generate Grade Reports")
        print("5 Import/Export All CSVs")
        print("0 Exit")

        choice = input("Choice: ")

        if choice == "1":
            course_id = input("Course ID: ").strip()
            course_students = [
                s for s in students.to_list() if s.course_id == course_id
            ]
            if not course_students:
                print("No students found for that course")
                continue
            course_students.sort(
                key=lambda s: (
                    grade_order.get(s.grade, 99),
                    -s.marks,
                    s.last_name,
                    s.first_name,
                )
            )
            display_list(course_students)
        elif choice == "2":
            email = input("Student email to search: ").strip()
            start = time.perf_counter()
            student = students.find_first(lambda s: s.email == email)
            elapsed_ms = (time.perf_counter() - start) * 1000
            if student:
                print(", ".join(str(part) for part in student.to_list()))
            else:
                print("Student record not found")
            print(f"Search time: {elapsed_ms:.3f} ms")
        elif choice == "3":
            course_id = input("Course ID: ").strip()
            course_students = [
                s for s in students.to_list() if s.course_id == course_id
            ]
            if not course_students:
                print("No students found for that course")
                continue
            marks = sorted(int(s.marks) for s in course_students)
            avg = sum(marks) / len(marks)
            mid = len(marks) // 2
            if len(marks) % 2 == 1:
                median = marks[mid]
            else:
                median = (marks[mid - 1] + marks[mid]) / 2
            print(f"Average score: {avg:.2f}")
            print(f"Median score: {median:.2f}")
        elif choice == "4":
            while True:
                print("\nReport Menu")
                print("1 Report by Course")
                print("2 Report by Professor")
                print("3 Report by Student")
                print("0 Back")

                report_choice = input("Choice: ")

                if report_choice == "1":
                    course_id = input("Course ID: ").strip()
                    course = courses.find_first(
                        lambda c: c.course_id == course_id
                    )
                    course_students = [
                        s for s in students.to_list()
                        if s.course_id == course_id
                    ]
                    report_lines = []
                    if course:
                        report_lines.append(
                            f"Course Report: {course.course_id} "
                            f"{course.course_name}"
                        )
                        report_lines.append(
                            f"Description: {course.description}"
                        )
                    else:
                        report_lines.append(f"Course Report: {course_id}")
                    print(f"\n{report_lines[0]}")
                    if len(report_lines) > 1:
                        print(report_lines[1])
                    if not course_students:
                        print("No students found for that course")
                        continue
                    course_students.sort(
                        key=lambda s: (s.last_name, s.first_name)
                    )
                    student_lines = [
                        ", ".join(str(part) for part in s.to_list())
                        for s in course_students
                    ]
                    for line in student_lines:
                        print(line)
                    save_report(
                        "Filename to save course report: ",
                        report_lines + student_lines,
                    )
                elif report_choice == "2":
                    professor_id = input("Professor ID: ").strip()
                    professor = professors.find_first(
                        lambda p: p.professor_id == professor_id
                    )
                    if not professor:
                        print("Professor not found")
                        continue
                    report_lines = [
                        f"Professor Report: {professor.professor_id} "
                        f"{professor.name}",
                        f"Course: {professor.course_id} "
                        f"Rank: {professor.rank}",
                    ]
                    print(f"\n{report_lines[0]}")
                    print(report_lines[1])
                    course_students = [
                        s for s in students.to_list()
                        if s.course_id == professor.course_id
                    ]
                    if not course_students:
                        print("No students found for that course")
                        continue
                    course_students.sort(
                        key=lambda s: (s.last_name, s.first_name)
                    )
                    student_lines = [
                        ", ".join(str(part) for part in s.to_list())
                        for s in course_students
                    ]
                    for line in student_lines:
                        print(line)
                    save_report(
                        "Filename to save professor report: ",
                        report_lines + student_lines,
                    )
                elif report_choice == "3":
                    email = input("Student email: ").strip()
                    student = students.find_first(lambda s: s.email == email)
                    if not student:
                        print("Student record not found")
                        continue
                    report_lines = [
                        f"Student Report: {student.first_name} "
                        f"{student.last_name}",
                        f"Course: {student.course_id} "
                        f"Grade: {student.grade} "
                        f"Marks: {student.marks}",
                    ]
                    print(f"\n{report_lines[0]}")
                    print(report_lines[1])
                    save_report(
                        "Filename to save student report: ",
                        report_lines,
                    )
                elif report_choice == "0":
                    break
                else:
                    print("Invalid choice")
        elif choice == "5":
            while True:
                print("\nImport/Export Menu")
                print("1 Import all CSVs")
                print("2 Export all CSVs")
                print("0 Back")

                ie_choice = input("Choice: ")

                if ie_choice == "1":
                    students.clear()
                    courses.clear()
                    professors.clear()

                    for s in load_from_csv(STUDENT_FILE, Student):
                        students.append(s)
                    for c in load_from_csv(COURSE_FILE, Course):
                        courses.append(c)
                    for p in load_from_csv(PROFESSOR_FILE, Professor):
                        professors.append(p)
                    logins = load_logins()

                    print(
                        "Imported students, courses, professors, and logins"
                    )
                elif ie_choice == "2":
                    folder_name = input(
                        "Folder name to export CSVs: "
                    ).strip()
                    export_all_to_folder(folder_name)
                elif ie_choice == "0":
                    break
                else:
                    print("Invalid choice")
        elif choice == "0":
            return
        else:
            print("Invalid choice")


def admin_menu():
    while True:

        print("\nCheckMyGrade System")
        print("1 Add Student")
        print("2 Display Students")
        print("3 Save Students")
        print("4 Modify Student")
        print("5 Manage Courses")
        print("6 Manage Professors")
        print("7 Import/Export All CSVs")
        print("8 Delete Student")
        print("0 Exit")

        choice = input("Choice: ")

        if choice == "1":

            email = input("Email: ")
            if not email:
                print("Email is required, and cannot be empty.")
                email = input("Email: ")
            first = input("First name: ")
            last = input("Last name: ")
            course = input("Course ID: ")
            grade = input("Grade: ")
            marks = input("Marks: ")

            s = Student(email, first, last, course, grade, marks)

            students.append(s)

        elif choice == "2":

            students.display()

        elif choice == "3":

            rt = save_to_csv(STUDENT_FILE, students.to_list())
            if rt:
                print("Students saved to CSV")

        elif choice == "4":

            email = input("Email of student to modify: ")
            student = students.find_first(lambda s: s.email == email)

            if not student:
                print("Student not found")
                continue

            print("Press Enter to keep the current value.")
            first = input(f"First name ({student.first_name}): ").strip()
            last = input(f"Last name ({student.last_name}): ").strip()
            course = input(f"Course ID ({student.course_id}): ").strip()
            grade = input(f"Grade ({student.grade}): ").strip()
            marks = input(f"Marks ({student.marks}): ").strip()

            if first:
                student.first_name = first
            if last:
                student.last_name = last
            if course:
                student.course_id = course
            if grade:
                student.grade = grade
            if marks:
                student.marks = int(marks)

            print("Student updated")

        elif choice == "5":

            manage_courses()

        elif choice == "6":

            manage_professors()

        elif choice == "7":

            while True:
                print("\nImport/Export Menu")
                print("1 Import all CSVs")
                print("2 Export all CSVs")
                print("0 Back")

                ie_choice = input("Choice: ")

                if ie_choice == "1":
                    students.clear()
                    courses.clear()
                    professors.clear()

                    for s in load_from_csv(STUDENT_FILE, Student):
                        students.append(s)
                    for c in load_from_csv(COURSE_FILE, Course):
                        courses.append(c)
                    for p in load_from_csv(PROFESSOR_FILE, Professor):
                        professors.append(p)
                    logins = load_logins()

                    print(
                        "Imported students, courses, professors, and logins"
                    )
                elif ie_choice == "2":
                    folder_name = input(
                        "Folder name to export CSVs: "
                    ).strip()
                    export_all_to_folder(folder_name)
                elif ie_choice == "0":
                    break
                else:
                    print("Invalid choice")

        elif choice == "8":
            email = input("Email: ")
            deleted = students.remove_first(lambda s: s.email == email)
            if deleted:
                print("Student deleted")
            else:
                print("Student not found")

        elif choice == "0":

            save_to_csv(STUDENT_FILE, students.to_list())
            save_to_csv(COURSE_FILE, courses.to_list())
            save_to_csv(PROFESSOR_FILE, professors.to_list())
            break


if logged_in_role == "student":
    student_menu()
elif logged_in_role == "professor":
    professor_menu()
else:
    admin_menu()
