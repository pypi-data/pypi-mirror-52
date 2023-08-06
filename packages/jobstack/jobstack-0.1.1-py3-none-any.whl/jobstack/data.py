import csv
from pathlib import Path
import pendulum
from .common import User, JobStackError
from .project import Project, ProjectStage, Stage, Level
from .calendar import CalendarCollection, Calendar, Year




FY20 = Year('FY20', pendulum.datetime(2019, 8, 1), pendulum.datetime(2020, 7, 31))


def read_csv(pth, handler, header=True):
    with pth.open(mode='r') as fh_:
        csvreader = csv.reader(fh_, delimiter=',', quotechar='"')
        for index, row in enumerate(csvreader):
            if header is True and index == 0:
                continue
            handler(index, row)


def get_users(user_csv):
    users = []
    def _map_user(index, row):
        users.append(
            User(
                row[0],
                row[1],
                row[2],
                int(row[3])
            )
        )
    read_csv(user_csv, _map_user)
    return users


def build_projects(er_csv, users):
    projects = []

    def _map_project(index, row):
        priority, er_id, er_name, usr_name = row[:4]
        stages = row[4:]
        prj = Project(
            id=er_id.strip(),
            name=er_name.strip(),
            priority=float(priority)
        )
        #  print(row)
        #  print(f"{index} user: {usr_name}")
        prj.user = User.find_in(users, usr_name)

        for stage_index, stage_notation in enumerate(stages, 1):
            try:
                if not stage_notation:
                    continue
                stage = ProjectStage.parse(stage_notation, prj, users)
                if not prj.stages.is_empty and not prj.stages.head.stage.lt(stage.stage):
                    raise JobStackError(f"Stage {stage.stage} is out of sequence.\nLine: {index} Column: {4 + stage_index}")
                prj.stages.append(stage)
            except Exception as ex:
                raise JobStackError(f"{ex}\nLine: {index} Column: {4 + stage_index}")

        projects.append(prj)

    read_csv(er_csv, _map_project)

    projects.sort(key=lambda p: p.priority)

    return projects


def write_project_completion_dates():
    pass


def build_calendars(users):
    calendars = []

    for usr in users:
        c = Calendar(usr, FY20)
        c.build(36)
        calendars.append(c)
        #  print(c)

    return CalendarCollection(calendars)
