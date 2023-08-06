import pendulum
from .common import User, JobStackError
from .structs import DLLNode, DLinkedList


class Quarter:

    def __init__(self, year, num, start, end):
        self.year = year
        self.number = num
        self.start = start
        self.end = end

    def contains(self, date):
        return self.start <= date and self.end >=date

    def next_quarter(self):
        return Quarter(
            self.year,
            self.number + 1,
            self.end.add(months=1).start_of('month'),
            self.end.add(months=3).end_of('month')
        )

    def __str__(self):
        return f"Q{self.number}"

    def __format__(self, fmt):
        if fmt == "A":
            return f"{self} {self.start:MM/DD/YYYY}-{self.end:MM/DD/YYYY}"
        elif fmt == "YA":
            return f"{self.year}-{self}"
        else:
            return str(self)

class Year:

    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.init_quarters()

    def init_quarters(self):
        self.q1 = q1 = Quarter(
            self,
            1,
            self.start.start_of('month'),
            self.start.add(months=2).end_of('month')
        )
        self.q2 = q2 = q1.next_quarter()
        self.q3 = q3 = q2.next_quarter()
        self.q4 = q3.next_quarter()

    def find_quarter(self, date):
        for quarter in (self.q1, self.q2, self.q3, self.q4):
            if quarter.contains(date):
                return quarter

    def __str__(self):
        return self.name

    def __format__(self, fmt):
        if fmt == "A":
            return f"{self} {self.start:MM/DD/YYYY}-{self.end:MM/DD/YYYY}"
        else:
            return str(self)


class WeekDates:

    def __init__(self, start_date=None, monday=None, friday=None):
        if start_date and not monday and not friday:
            self.monday = m = start_date.start_of('week')
            self.friday = m.add(days=4)
        elif monday and friday and not start_date:
            self.monday = monday
            self.friday = friday
        else:
            raise JobStackError('Invalid week parameters.')

    def set_quarter(self, year):
        self.quarter = year.find_quarter(self.friday)

    def next(self):
        next_monday = self.monday.add(weeks=1)
        next_friday = self.friday.add(weeks=1)
        return WeekDates(monday=next_monday, friday=next_friday)

    def contains(self, day):
        return self.monday <= day and self.friday >= day

    def __eq__(self, othr):
        return self.monday == othr.monday and self.friday == othr.friday

    def __gt__(self, othr):
        return self.monday > othr.monday and self.friday > othr.friday

    def __lt__(self, othr):
        return self.monday < othr.monday and self.friday < othr.friday

    def __le__(self, othr):
        return self.monday <= othr.monday and self.friday <= othr.friday

    def __str__(self):
        return f"{self.monday:MM/DD/YYYY} - {self.friday:MM/DD/YYYY}"

    def __format__(self, fmt):
        if fmt == 'A':
            return f"{self.quarter:YA} ({self})"
        else:
            return str(self)


class Bucket(DLLNode):

    def __init__(self, number, week):
        self.number = number
        self.week = week
        self.content = None
        self.user = ""

    @property
    def is_empty(self):
        return self.content is None

    def set_content(self, stage_bucket):
        self.content = stage_bucket
        self.user = stage_bucket.user
        stage_bucket.assigned_weekdates = self.week.weekdates

    def __str__(self):
        return str(self.number)


class Week(DLLNode):

    def __init__(self, calendar, week, count):
        self.calendar = calendar
        self.weekdates = week
        self.buckets = DLinkedList(Bucket)
        self.buckets.append_list([Bucket(i, self) for i in range(0, count)])

    def header(self):
        return self

    def __eq__(self, othr):
        return self.weekdates == othr.weekdates


class Calendar:

    def __init__(self, user, fiscal_year, starts=pendulum.now()):
        self.fiscal_year = fiscal_year
        self.user = user
        self.start_week = WeekDates(start_date=starts)
        self.weeks = DLinkedList(Week)

    def build(self, no_of_weeks):
        current_week = self.start_week
        current_week.set_quarter(self.fiscal_year)
        for i in range(0, no_of_weeks):
            self.weeks.append(Week(self, current_week, self.user.weekly_buckets))
            current_week = current_week.next()
            current_week.set_quarter(self.fiscal_year)

    def header(self):
        return self.user

    def iter_weeks(self):
        yield self.user
        for wk in self.weeks:
            yield wk

    def find_first_bucket(self, greater_than=None, week_is=None):
        for wk in self.weeks:
            if greater_than and wk.weekdates <= greater_than:
                continue
            if week_is and wk.weekdates != week_is:
                continue
            for bucket in wk.buckets:
                if bucket.is_empty:
                    return bucket

    def find_bucket_after(self, this_bucket):
        for wk in self.weeks:
            for bucket in wk.buckets:
                if this_bucket is bucket:
                    return bucket.next

    def find_week_by_date(self, date):
        if date is None:
            return
        #  import pdb;pdb.set_trace()
        for wk in self.weeks:
            print(f"{wk.weekdates}")
            if wk.weekdates.contains(date):
                return wk

    def find_week(self, week):
        for wk in self.weeks:
            if wk == week:
                return wk

    def __repr__(self):
        return f"<Calendar user='{self.user}'>"


class CalendarCollection:

    def __init__(self, calendars):
        self.calendars = calendars

    def get_by_user(self, user):
        for c in self.calendars:
            if c.user == user:
                return c

    def __iter__(self):
        weeks = []
        for calendar in self.calendars:
            weeks.append(calendar.iter_weeks())

        for cross_section in zip(*weeks):
            yield cross_section
