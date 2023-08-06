import re
import pendulum
from pendulum.parsing import ParserError
from enum import Enum
from dataclasses import dataclass
from .common import User, JobStackError
from .colors import iter_colors
from .structs import DLLNode, DLinkedList


class IEnum(Enum):

    @classmethod
    def get(cls, name):
        for ename, evalue in cls.__members__.items():
            if name == ename:
                return evalue
        raise JobStackError(f"`{name}` is not a {cls} value.")

    def gt(self, othr):
        return self.value > othr.value

    def lt(self, othr):
        return self.value < othr.value

    def __str__(self):
        return self.name


class Stage(IEnum):

    BA = 1
    DEV = 2
    QA = 3
    UAT = 4
    INSTALL = 5
    INST = 5
    SUPPORT = 6
    SUP = 6


class Status(IEnum):
    Open = 1
    O = 1
    Completed = 2
    C = 2
    Delayed = 3
    D = 3


class Level(Enum):
    xsmall = 0
    XS = 0
    small = 1
    SM = 1
    medium = 2
    MD = 2
    large = 3
    LG = 3
    xlarge = 4
    XL = 4


class ProjectBucket(DLLNode):

    def __init__(self, project, stage, user, bucket_count, status, start_date=None, merge=None):
        self.project = project
        self.stage = stage
        self.user = user
        self.bucket_count = bucket_count
        self.status = status
        self.start_date = start_date
        self.merge = merge

    def __str__(self):
        return f"{self.project.id} ({self.stage}) {self.project.priority}"


# using this to normalize dates
current_timezone = pendulum.now().tzinfo


def parse_bucket_notation(notation):
    """
    2019-10-13/1/1/1/1/>

    """
    segments = notation.split('/')
    start_date = None
    merge = None
    try:
        start_date = pendulum.parse(segments[0], tz=current_timezone)
        #  start_date.tzinfo = current_timezone
    except ParserError as ex:
        pass

    if segments[-1] in '<>':
        merge = segments[-1]

    if start_date:
        segments = segments[1:]

    if merge:
        segments = segments[:-1]

    return segments, start_date, merge



class ProjectStage(DLLNode):

    def __init__(self, project, stage, user, buckets, status):
        self.project = project
        self.stage = stage
        self.user = user
        self.buckets = DLinkedList(ProjectBucket)
        self.buckets.append_list(buckets)
        self.status = status
        self.assigned_weekdates = None

    def __str__(self):
        return f"{self.project.id} ({self.stage})"

    @staticmethod
    def parse(notation, project, users):
        """Parse the following string notation:
            [STAGE]:[USER_ABBR]:[BUCKETS]:[STATUS]
        Example:
            BA:MGE:1/2/1:O
        """
        sections = notation.split(":")

        if len(sections) != 4:
            raise JobStackError(f"Stage notation invalid! 4 segments are required, found {len(sections)} in '{notation}'")

        stage, user, buckets, status = sections

        stage = Stage.get(stage)
        user = User.find_in(users, user)
        status = Status.get(status)
        bucket_info, start_date, merge = parse_bucket_notation(buckets)
        buckets = [ProjectBucket(project, stage, user, int(i), status, start_date=start_date, merge=merge) for i in bucket_info]

        return ProjectStage(project, stage, user, buckets, status)


class ProjectMeta:

    def __init__(self):
        pass


class Project:

    def __init__(self, id, name, priority):
        self.meta = ProjectMeta()
        self.meta.color = next(iter_colors)
        self.id = id
        self.name = name
        self.priority = priority
        self.user = None
        self.stages = DLinkedList(ProjectStage)

    def end_week(self):
        bucket = None
        stage = self.stages.last()
        if stage:
            bucket = stage.buckets.last()
        if bucket:
            return bucket.assigned_weekdates
        raise JobStackError(f"{self.id} has no buckets.")

    @property
    def team(self):
        s = set()
        for stage in self.stages:
            s.add(stage.user)
        return s

    def __repr__(self):
        return f"<Project id='{self.id}' name='{self.name}'>"



if __name__ == '__main__':

    mark = User('Mark')
    p = Project('FY19-000345', 'Some project')

    p.set_stage(Stage.BA, Level.small, mark)
    p.set_stage(Stage.DEV, Level.small, mark)
    p.set_stage(Stage.QA, Level.small, mark)
    p.set_stage(Stage.UAT, Level.small, mark)
    p.set_stage(Stage.INSTALL, Level.small, mark)
    p.set_stage(Stage.SUPPORT, Level.small, mark)
