import os
import json

class Metadata:
    def __init__(self, metadata_file_name:str) -> None:
        self.metadata_file_name = metadata_file_name

    def get_value(self, keys: list[str]):
        """given a nested or direct keys to recive the value in a json file"""
        with open(self.metadata_file_name, 'r',encoding='utf-8') as file:
            data: dict = json.load(file)

        value = data
        for key in keys:
            value = value[key]
        return value
        
    def set_value(self, keys:list[str], new_value):
        with open(self.metadata_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Traverse through nested keys
        current_level = data
        for key in keys[:-1]:  # All keys except the last one
            current_level = current_level.get(key, {})
        last_key = keys[-1]
    
        # Update the value if the last key exists
        if last_key in current_level:
            current_level[last_key] = new_value

        with open(self.metadata_file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
