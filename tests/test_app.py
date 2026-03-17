import os
import tempfile
import time
import unittest

from models.course import Course
from models.professor import Professor
from models.student import Student
from structures.linked_list import LinkedList
from utils.csv_handler import load_from_csv, save_to_csv


class TestStudentRecords(unittest.TestCase):
    def _make_students(self, count):
        students = []
        for i in range(count):
            students.append(
                Student(
                    f"student{i}@example.com",
                    f"First{i}",
                    f"Last{i}",
                    f"COURSE-{i % 5}",
                    "A" if i % 2 == 0 else "B",
                    50 + (i % 51),
                )
            )
        return students

    def test_add_delete_modify_students_with_1000_records(self):
        print("Running test_add_delete_modify_students_with_1000_records")
        students = LinkedList()
        for s in self._make_students(1000):
            students.append(s)

        self.assertEqual(len(students.to_list()), 1000)

        target = students.find_first(lambda s: s.email == "student10@example.com")
        self.assertIsNotNone(target)
        target.grade = "A+"
        target.marks = 99

        removed = students.remove_first(
            lambda s: s.email == "student20@example.com"
        )
        self.assertTrue(removed)
        self.assertEqual(len(students.to_list()), 999)

    def test_load_previous_csv_and_search_timing(self):
        print("Running test_load_previous_csv_and_search_timing")
        data_file = os.path.join("data", "students.csv")
        if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
            self.skipTest("data/students.csv not found or empty")

        loaded = load_from_csv(data_file, Student)
        self.assertTrue(len(loaded) > 0)

        start = time.perf_counter()
        match = None
        for s in loaded:
            if s.email == loaded[0].email:
                match = s
                break
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"Search time (CSV load): {elapsed_ms:.3f} ms")
        self.assertIsNotNone(match)

    def test_sort_students_by_marks_and_email_with_timing(self):
        print("Running test_sort_students_by_marks_and_email_with_timing")
        students = self._make_students(1000)

        start = time.perf_counter()
        by_marks_asc = sorted(students, key=lambda s: int(s.marks))
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"Sort by marks ascending: {elapsed_ms:.3f} ms")
        self.assertEqual(by_marks_asc[0].marks, min(s.marks for s in students))

        start = time.perf_counter()
        by_marks_desc = sorted(
            students, key=lambda s: int(s.marks), reverse=True
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"Sort by marks descending: {elapsed_ms:.3f} ms")
        self.assertEqual(by_marks_desc[0].marks, max(s.marks for s in students))

        start = time.perf_counter()
        by_email_asc = sorted(students, key=lambda s: s.email)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"Sort by email ascending: {elapsed_ms:.3f} ms")
        self.assertEqual(by_email_asc[0].email, min(s.email for s in students))

        start = time.perf_counter()
        by_email_desc = sorted(students, key=lambda s: s.email, reverse=True)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"Sort by email descending: {elapsed_ms:.3f} ms")
        self.assertEqual(by_email_desc[0].email, max(s.email for s in students))

    def test_save_and_load_1000_records(self):
        print("Running test_save_and_load_1000_records")
        students = self._make_students(1000)
        with tempfile.TemporaryDirectory() as temp_dir:
            path = os.path.join(temp_dir, "students.csv")
            save_to_csv(path, students)
            loaded = load_from_csv(path, Student)
            self.assertEqual(len(loaded), 1000)


class TestCourseRecords(unittest.TestCase):
    def test_add_delete_modify_course(self):
        print("Running test_add_delete_modify_course")
        courses = LinkedList()
        courses.append(Course("C-1", "Math", "Core math"))
        courses.append(Course("C-2", "History", "World history"))

        target = courses.find_first(lambda c: c.course_id == "C-1")
        self.assertIsNotNone(target)
        target.course_name = "Advanced Math"
        target.description = "Updated description"

        removed = courses.remove_first(lambda c: c.course_id == "C-2")
        self.assertTrue(removed)
        self.assertEqual(len(courses.to_list()), 1)


class TestProfessorRecords(unittest.TestCase):
    def test_add_delete_modify_professor(self):
        print("Running test_add_delete_modify_professor")
        professors = LinkedList()
        professors.append(Professor("P-1", "Ada Lovelace", "Senior", "C-1"))
        professors.append(Professor("P-2", "Alan Turing", "Junior", "C-2"))

        target = professors.find_first(lambda p: p.professor_id == "P-1")
        self.assertIsNotNone(target)
        target.rank = "Lead"
        target.course_id = "C-3"

        removed = professors.remove_first(lambda p: p.professor_id == "P-2")
        self.assertTrue(removed)
        self.assertEqual(len(professors.to_list()), 1)


if __name__ == "__main__":
    unittest.main()
