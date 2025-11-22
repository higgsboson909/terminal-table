import json
from prompt_toolkit.filters import is_done
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.styles import Style
import os

style = Style.from_dict(
    {
        "frame.border": "#ff4444",
        "selected-option": "bold",
        # ('noreverse' because the default toolbar style uses 'reverse')
        "bottom-toolbar": "#ffffff bg:#333333 noreverse",
    }
)

filename = 'semester_table_data.json'

semester_list = []
try:
    with open(filename, 'r') as file:
        data = json.load(file)
        for semester in data.get('timetable_by_group'):
            semester_list.append(semester)

except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON from the file. Details: {e}")


answers = {}  # store selected results

def ask_choice(label, options):
    """
    Ask a choice question and display only the selected result afterward.
    """
    result = choice(
        message=f"{label}:",
        options=options,
        show_frame=~is_done,
        style=style,
        bottom_toolbar=HTML(
            " Press <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept."
        ),
    )

    # Save the result (store the human-readable text)
    answers[label] = dict(options)[result]

    # Clear screen
    print("\033[2J\033[H", end="")

    # Show all previously selected items
    for k, v in answers.items():
        print(f"{k}: {v}")

    print()  # spacing
    return result

def getChoices():

    choices = {}

    semester_options = []
    for s in semester_list:
        a = []
        a.append(s)
        a.append(s)
        a = tuple(a)
        semester_options.append(a)

    semester = ask_choice(
        "Semester",
        semester_options
    )
    choices['semester'] = semester
    

    program_options = []
    for p in data['timetable_by_group'][semester]:
        a = []
        a.append(p)
        a.append(p)
        a = tuple(a)
        program_options.append(a)

    program = ask_choice(
        "Program",
        program_options
    )
    choices['program'] = program

    section_options = []
    for p in data['timetable_by_group'][semester][program]:
        a = []
        a.append(p)
        a.append(p)
        a = tuple(a)
        section_options.append(a)

    section = ask_choice(
        "Section",
        section_options
    )

    choices['section'] = section
    print(choices)
    return choices
    
def get_timetable(choices):

    semester = choices['semester']
    program = choices['program']
    section= choices['section']

    try:
        # Navigate the nested dictionary structure using the three chosen keys
        timetable_details = data['timetable_by_group'][semester][program][section]

        for day, lectures in timetable_details.items():
            print(day)
            for lec in lectures:
                print(lec)
            # print(lectures)

        # --- Step 2: Print or process the retrieved data ---
        # print("\n--- Final Timetable Details ---")
        # print(f"Details for {semester}, {program}, Section {section}:")
        #
        # # Check if the details is a dictionary (common for timetable data)
        # if isinstance(timetable_details, dict):
        #     # Print each key/value pair in the details (e.g., 'course', 'time', 'room')
        #     for key, value in timetable_details.items():
        #         print(f"  **{key.capitalize()}:** {value}")
        # else:
        #     # Handle cases where the final section value is just a simple string or list
        #     print(timetable_details)

        # print(timetable_details)
    except KeyError as e:
        print(f"\nError: Could not find data for the selection. Missing key: {e}")
