class Grade:

    def __init__(self, grade_id, grade, mark_range):
        self.grade_id = grade_id
        self.grade = grade
        self.mark_range = mark_range

    def display_grade(self):
        print(self.grade_id, self.grade, self.mark_range)