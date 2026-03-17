class Course:
    CSV_HEADERS = ["Course_id", "Course_name", "Description"]
    UNIQUE_KEYS = ["course_id"]

    def __init__(self, course_id, course_name, description):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description

    def display_course(self):
        print(self.course_id, self.course_name, self.description)

    def to_list(self):
        return [self.course_id, self.course_name, self.description]
