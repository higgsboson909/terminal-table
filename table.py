from rich.console import Console
from datetime import datetime, timedelta
from rich.table import Table
from rich import box

def convert_24_to_12(time_24hr_str):
    time_object = datetime.strptime(time_24hr_str, "%H:%M")
    time_12hr_str = time_object.strftime("%I:%M")
    return time_12hr_str

def today():
    today = datetime.today().strftime("%A")
    return today

def next_day():
    today = datetime.today()
    # Corrected usage
    tomorrow = today + timedelta(days=1)
    next_day_name = tomorrow.strftime('%A')
    return next_day_name

def single_table(day_data, day):
    
    # table = Table(title=day, show_lines=False, row_styles=["reverse",""])
    
    # selected
    # table = Table(
    #     title=f"[bold]{day}[/bold ]",
    #     show_lines=False,
    #     header_style="bold cyan",
    #     border_style="magenta",
    #     title_style="bold italic cyan reverse",
    #     box=box.ROUNDED
    # )

    
    # selected
    table = Table(
        title=f"[bold green]{day}[/bold green]",
        header_style="bold black on green",
        border_style="bright_green",
        show_header=True,
        show_lines=True,
        box=box.ROUNDED,
    )


    table.add_column("Time", justify="center", style="cyan", no_wrap=True)
    table.add_column("Subject", justify="center", style="magenta")
    table.add_column("Teacher", justify="center", style="green")
    table.add_column("Room", justify="center", style="magenta")
    table.add_section() 

# Sort day_data by 'from_time'
    sorted_day_data = sorted(
        day_data,
        key=lambda lec: tuple(map(int, lec['from_time'].split(':')))
    )

    for lec in sorted_day_data:
        from_time = convert_24_to_12(lec['from_time'])
        end_time = convert_24_to_12(lec['end_time'])
        time = f"{from_time} - {end_time}"
        table.add_row(time, lec['course_name'], lec['faculty_name'], lec['room_id'])

    console = Console()
    console.print(table)
    print()


def full_view(timetable_data):
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for day_data in ordered_days:
        if day_data in timetable_data:
            single_table(timetable_data[day_data], day_data)

def oneday_table(arg, timetable_data):
    days_dict = {'mon': "Monday", 'tue': "Tuesday", 'wed': "Wednesday", 'thu': "Thursday", 'fri': "Friday", 'sat': "Saturday", 'sun': "Sunday"}

    if(arg == "-t"):
        day = today()
        if day == "Sunday":
            print("Bhai! Kya chahta hai?\nIt's Sunday today")
        elif day in timetable_data:
            single_table(timetable_data[day], day)
        else:
            print(f"No class on {day}!")
    
    elif(arg == "-n"):
        day = next_day()
        if day == "Sunday":
            print("Bhai! Kya chahta hai?\nIt's Sunday tomorrow")
        elif day in timetable_data:
            single_table(timetable_data[day], day)
        else:
            print(f"No class on {day}!")

    elif(arg in days_dict):
        day = days_dict[arg]
        if day in timetable_data:
            single_table(timetable_data[day], day)
        elif day == "Sunday":
            print("Bhai! Kya chahta hai?\nIt's Sunday tomorrow")
        else:
            print(f"No class on {day}!")
