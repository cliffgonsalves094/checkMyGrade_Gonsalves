class Professor:
    CSV_HEADERS = ["Professor_id", "Professor Name", "Rank", "Course.id"]
    UNIQUE_KEYS = ["professor_id"]

    def __init__(self, professor_id, name, rank, course_id):
        self.professor_id = professor_id
        self.name = name
        self.rank = rank
        self.course_id = course_id

    def display_professor(self):
        print(self.professor_id, self.name, self.rank, self.course_id)

    def to_list(self):
        return [
            self.professor_id,
            self.name,
            self.rank,
            self.course_id
        ]
