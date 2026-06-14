import json
import os


class FileHandler:
    """
    handles saving and loading data to/from JSON files.
    """
    
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self._ensure_folder_exists()
    
    def _ensure_folder_exists(self):
        """Create data folder if it doesn't exist"""
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
    
    def save(self, filename, data_list):
        """Save list of objects to json file"""
        try:
            filepath = os.path.join(self.data_folder, filename)
            dict_list = [item.to_dict() for item in data_list]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(dict_list, f, indent=2)
            
            return True
        except IOError as e:
            print(f"Error: Could not save to {filename} - {e}")
            return False
    
    def load(self, filename, cls):
        """Load objects from a JSON file"""
        try:
            filepath = os.path.join(self.data_folder, filename)
            
            if not os.path.exists(filepath):
                return []
            
            with open(filepath, 'r', encoding='utf-8') as f:
                dict_list = json.load(f)
            
            return [cls.from_dict(item) for item in dict_list]
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {filename}")
            return []
        except IOError as e:
            print(f"Error: Could not read {filename} - {e}")
            return []