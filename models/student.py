class Student:
    CSV_HEADERS = [
        "email",
        "first_name",
        "last_name",
        "course_id",
        "grade",
        "marks",
    ]
    UNIQUE_KEYS = ["email"]

    def __init__(self, email, first_name, last_name, course_id, grade, marks):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.grade = grade
        self.marks = int(marks)

    def display_record(self):
        print(self.email, self.first_name, self.last_name,
              self.course_id, self.grade, self.marks)

    def to_list(self):
        return [
            self.email,
            self.first_name,
            self.last_name,
            self.course_id,
            self.grade,
            self.marks
        ]
