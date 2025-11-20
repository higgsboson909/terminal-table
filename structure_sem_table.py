import json


    
# Define the file path
file_path = 'data.json'

# Open the file and load the data
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print("a imported successfully:")
        print(f"The data type is: {type(data)}")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON from the file. Details: {e}")


def semester_table(source_data):
    # Initialize the new dictionary
    semester_table = {}
    semester_list = set()

    # 1. Iterate through the room-based timetable
    for room_id, days_data in source_data.get("timetable", {}).items():
        # 2. Iterate through the days of the week (Crucial: day_name is available here)
        program_list = set()
        for day_name, class_list in days_data.items():
            # 3. Iterate through the list of classes for that day
           
            for class_info in class_list:
                # Extract the key fields for the new structure
                semester_id = class_info.get("semester_id")
                program_name = class_info.get("program_name")
                section_name = class_info.get("section_name")

                semester_list.add(semester_id)
                
                # Copy class details, excluding the fields we are using as keys
                class_details = {
                    "from_time": class_info.get("from_time"),
                    "end_time": class_info.get("end_time"),
                    "course_name": class_info.get("course_name"),
                    "faculty_name": class_info.get("faculty_name"),
                    "room_id": class_info.get("room_id"),
                }

                # --- Build the four-level nested structure (Semester > Program > Section > Day) ---
                
                # Level 1: Semester ID
                if semester_id not in semester_table:
                    semester_table[semester_id] = {}
                
                # Level 2: Program Name
                if program_name not in semester_table[semester_id]:
                    semester_table[semester_id][program_name] = {}

                    
                # Level 3: Section Name
                if section_name not in semester_table[semester_id][program_name]:
                    semester_table[semester_id][program_name][section_name] = {}
                    
                # Level 4: Day Name
                if day_name not in semester_table[semester_id][program_name][section_name]:
                    semester_table[semester_id][program_name][section_name][day_name] = []
                
                # Append the core class details to the final list for that specific day
                semester_table[semester_id][program_name][section_name][day_name].append(class_details)

    # Wrap the new timetable with the original metadata
    final_output = {
        "status": source_data.get("status"),
        "timestamp": source_data.get("timestamp"),
        "current_info": source_data.get("current_info"),
        "semester_list": list(semester_list),
        "timetable_by_group":semester_table 
    }
 
    filename = 'semester_table_data.json'
    
    # Open the file in write mode ('w') and use json.dump() to write the data
    # The 'with' statement automatically handles file closing
    with open(filename, 'w') as json_file:
        json.dump(final_output, json_file, indent=4)

    print(f"Successfully wrote data to {filename}")   



