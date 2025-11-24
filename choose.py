import json
import os.path
from table import full_view
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

def load_data():
    data = {}
    filename = 'semester_table_data.json'
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from the file. Details: {e}")
    return data
    

def get_semester_list(data):
    semester_list = []
    try:
        for semester in data.get('timetable_by_group'):
            semester_list.append(semester)

    except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from the file. Details: {e}")
    return semester_list



answers = {}  # store selected results

def ask_choice(label, options, pref):
    """
    Ask a choice question and display only the selected result afterward.
    """
    result = choice(
        message=f"{label}:",
        options=options,
        default=pref,
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

def getChoices(data):

    pref = None
    if os.path.isfile('pref.json'):
        with open('pref.json', 'r') as json_file:
            pref = json.load(json_file)
    else:
        with open("pref.json", 'w') as json_file:
            json.dump({
                "semester": "",
                "program": "",
                "section": ""
            }, json_file, indent=4)
        pref =  {
            "semester": "",
            "program": "",
            "section": ""
        }



    choices = {}
    # print(pref)

    semester_options = []
    semester_list = get_semester_list(data)
    for s in semester_list:
        a = []
        a.append(s)
        a.append(s)
        a = tuple(a)
        semester_options.append(a)

    semester = ask_choice(
        "Semester",
        semester_options,
        pref['semester']
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
        program_options,
        pref['program']
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
        section_options,
        pref['section']
    )

    choices['section'] = section

    with open("pref.json", 'w') as json_file:
        json.dump(choices, json_file, indent=4)

    return choices

    
def get_table_data(choices, data):

    semester = choices['semester']
    program = choices['program']
    section= choices['section']
    try:
        # Navigate the nested dictionary structure using the three chosen keys
        timetable_details = data['timetable_by_group'][semester][program][section]
        return timetable_details 

    except KeyError as e:
        print(f"\nError: Could not find data for the selection. Missing key: {e}")
