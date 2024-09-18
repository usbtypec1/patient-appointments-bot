class PatientTooOldError(Exception):

    def __init__(self, *args, max_age_in_years: int):
        super().__init__(*args)
        self.max_age_in_years = max_age_in_years


class PatientNameContainsPunctuationError(Exception):
    pass


class InvalidBirthDateError(Exception):
    pass
