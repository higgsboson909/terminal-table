from rich.console import Console
from rich.table import Table
from rich import box

def single_table(day_data, day):

    table = Table(title=day, show_lines=False, row_styles=["reverse",""])

    table.add_column("Time", justify="left", style="cyan", no_wrap=True)
    table.add_column("Subject", justify="left", style="magenta")
    table.add_column("Teacher", justify="left", style="green")
    table.add_column("Room", justify="left", style="magenta")
   
    for lec in day_data:
        time = f"{lec['from_time']} - {lec['end_time']}"
        table.add_row(time, lec['course_name'], lec['faculty_name'], lec['room_id'])

    console = Console()
    console.print(table)


def full_view(timetable_data):
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for day_data in timetable_data:
        single_table(timetable_data[day_data], day_data)
