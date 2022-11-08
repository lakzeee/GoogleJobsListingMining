import json

def dicts_to_json(data_list, file_name):
    with open(file_name, "w") as out:
        json.dump(data_list, out)
        print(f"{file_name} is saved.")