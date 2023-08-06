"""JobStack

Usage:
  jobstack  --users=<filepath> --projects=<filepath> --output=<filepath>

Options:
  -h --help       Show this help doc.
  -v --version    Show application version.

"""
import csv
from pathlib import Path
from importlib.resources import read_text
import importlib.resources as resrc
from jinja2 import Template, FileSystemLoader, PackageLoader, Environment, select_autoescape
from docopt import docopt
from .common import User, JobStackError
from .calendar import CalendarCollection, Calendar, Year
from .project import Project, Status, Stage, Level
from . import data


def distribute_projects(projects, calendars):
    # We're assuming project have been sorted by priority
    for project in projects:

        current_week = None

        for stage in project.stages:

            if stage.status is Status.Completed:
                continue

            calendar = calendars.get_by_user(stage.user)

            for bucket_index, stage_bucket in enumerate(stage.buckets):
                if bucket_index == 0:
                    print(f"{project.id} {stage.stage} start date: {stage_bucket.start_date}")
                    start_week = calendar.find_week_by_date(stage_bucket.start_date)
                    print(f"{project.id} {stage.stage} start week: {start_week} ({current_week})")
                    if (start_week and not current_week) or (start_week and start_week.weekdates > current_week):
                        current_week = start_week.prev.weekdates
                    #  print(f"{project.id} {stage.stage} start week: {current_week}")
                calendar_bucket = calendar.find_first_bucket(greater_than=current_week)

                if not calendar_bucket:
                    raise JobStackError(f"{project.id} - {stage.stage} - {stage.user} - could not find a bucket any time after {current_week}!")

                current_week = calendar_bucket.week.weekdates
                calendar_bucket.set_content(stage_bucket)

                if stage_bucket.bucket_count > 1:
                    for i in range(0, stage_bucket.bucket_count - 1):
                        calendar_bucket = calendar_bucket.next
                        while calendar_bucket is None:
                            # current week now needs to move to next week
                            calendar_bucket = calendar.find_first_bucket(greater_than=current_week)
                            current_week = calendar_bucket.week.weekdates
                        calendar_bucket.set_content(stage_bucket)


def build_html(projects, calendars, users):
    print('building html...')

    #  with resrc.path('jobstack.resources', 'calendar.html') as f:
    #      loader = FileSystemLoader(str(f.parent))
    env = Environment(
        loader=PackageLoader('jobstack', 'resources'),
        autoescape=select_autoescape(['html'])
    )
    #  template = Template(read_text('jobstack.resources', 'calendar.html'))
    template = env.get_template('calendar.html')
    return template.render(projs=projects, cals=calendars, users=users)


def save_output(filepath, content):
    with filepath.open(mode='w') as fh_:
        fh_.write(content)


def main():
    try:
        args = docopt(__doc__, version="jobstack v0.1")

        project_csv = Path(args['--projects']).resolve()
        user_csv = Path(args['--users']).resolve()
        output_html = Path(args['--output']).resolve()

        users = data.get_users(user_csv)
        calendars = data.build_calendars(users)
        projects = data.build_projects(project_csv, users)

        distribute_projects(projects, calendars)

        projects.sort(key=lambda x: x.end_week())

        save_output(output_html,  build_html(projects, calendars, users))

    except JobStackError as ex:
        print(ex)
    except Exception as ex:
        import traceback
        traceback.print_exc()
        print(ex)
