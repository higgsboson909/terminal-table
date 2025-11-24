from choose import getChoices
from choose import load_data
from app import raw_data_exists
from app import semester_data_exists
from app import get_data
from table import today_table 
from table import full_view
from choose import get_table_data
import sys



def main():
    get_data(raw_data_exists, semester_data_exists) 
    data = load_data()

    # Clear screen
    print("\033[2J\033[H", end="")

    print("Hello from ttable!")
    print()
    choices = getChoices(data)
    timetable_data = get_table_data(choices, data)
    
    if(len(sys.argv) > 1):
        view = sys.argv[1]
        if (view == "-f"):
            full_view(timetable_data)
    elif (len(sys.argv) == 1):
        today_table(timetable_data)


if __name__ == "__main__":
    main()
