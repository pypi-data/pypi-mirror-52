import uuid


class JobStackError(Exception):
    pass


def temp_id():
    return str(uuid.uuid4())[-12:]


class User:
    def __init__(self, last, first, abbr, weekly_buckets):
        self.first_name = first
        self.last_name = last
        self.abbr = abbr
        self.weekly_buckets = weekly_buckets
        self.temp_id = temp_id()

    def __hash__(self):
        return hash(f"{self.first_name}{self.last_name}{self.abbr}")

    @property
    def name(self):
        return f"{self.first_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def reverse_name(self):
        return f"{self.last_name}, {self.first_name}"

    def __eq__(self, othr):
        #  return self.full_name == self.full_name
        return self is othr or self.abbr == othr or self.full_name == othr or self.reverse_name == othr

    def __str__(self):
        return self.name

    @staticmethod
    def find_in(user_list, value):
        for usr in user_list:
            if usr == value:
                return usr
        raise JobStackError(f"User `{value}` not found in list.")
