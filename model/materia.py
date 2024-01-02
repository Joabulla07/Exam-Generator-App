class Subject:
    def __init__(
        self,
        grade,
        subject_name,
        day_1,
        day_2,
        correlative_number="0",
        date_assigned=None,
    ):
        self.grade = grade
        self.subject_name = subject_name
        self.correlative_number = correlative_number
        self.day_1 = day_1
        self.day_2 = day_2
        self.date_assigned = date_assigned

    def __repr__(self) -> str:
        return (
            f"Subject Name: {self.subject_name}, Grade: {self.grade}, "
            f"Correlative Number: {self.correlative_number}, Preference Day one: {self.day_1}"
        )
