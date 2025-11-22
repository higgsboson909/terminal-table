from choose import getChoices

from table import today_table 
from table import full_view
from choose import get_table_data

def main():
    
    print("Hello from terminal-table!")
    print()
    choices = getChoices()
    timetable_data = get_table_data(choices)
    full_view(timetable_data)
    today_table(timetable_data)


if __name__ == "__main__":
    main()
