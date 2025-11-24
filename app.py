import os
import json
from choose import getChoices
from request import download_json_file
from structure_sem_table import semester_table

JSON_URL = "https://griffin-k.github.io/Time-Table-Actions/read-data.json" 

def data(): 
    file_path = "./data.json"

    if os.path.isfile(file_path):
        # print(f"The file '{file_path}' exists and is a regular file.")
        return True
    else:
        print(f"The file '{file_path}' does not exist or is not a regular file.")
        return False 

def semester_data():
    file_path = "./semester_table_data.json"

    if os.path.isfile(file_path):
        # print(f"The file '{file_path}' exists and is a regular file.")
        return True
    else:
        print(f"The file '{file_path}' does not exist or its not a regualr file.")
        return False

raw_data_exists = data()
semester_data_exists = semester_data()

def get_data(raw_data_exists, semester_data_exists):
    if (not raw_data_exists):
        download_json_file(JSON_URL, "data.json")


    if (not semester_data_exists):
        # Define the file name
        filename = 'data.json'

        # Open the file and load the JSON data
        try:
            with open(filename, 'r') as file:
                data = json.load(file)

            semester_table(data)
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from the file. Details: {e}")


