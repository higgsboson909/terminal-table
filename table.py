from rich.console import Console
from datetime import datetime
from rich.table import Table
from rich import box

def convert_24_to_12(time_24hr_str):
    time_object = datetime.strptime(time_24hr_str, "%H:%M")
    time_12hr_str = time_object.strftime("%I:%M")
    return time_12hr_str

def today():
    today = datetime.today().strftime("%A")
    return today


def single_table(day_data, day):

    table = Table(title=day, show_lines=False, row_styles=["reverse",""])

    table.add_column("Time", justify="left", style="cyan", no_wrap=True)
    table.add_column("Subject", justify="left", style="magenta")
    table.add_column("Teacher", justify="left", style="green")
    table.add_column("Room", justify="left", style="magenta")
   
    for lec in day_data:
        from_time =  convert_24_to_12(lec['from_time'])
        end_time =  convert_24_to_12(lec['end_time'])
        time = f"{from_time} - {end_time}"
        table.add_row(time, lec['course_name'], lec['faculty_name'], lec['room_id'])

    console = Console()
    console.print(table)


def full_view(timetable_data):
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for day_data in timetable_data:
        single_table(timetable_data[day_data], day_data)

def today_table(timetable_data):
    day = today()
    if day == "Saturday" or day == "Sunday":
        single_table(timetable_data['Monday'], 'Monday')
    else:
        single_table(timetable_data[day], day)
        
