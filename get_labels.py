import os
import requests
from config import base_url

class GoBackException(Exception):
    pass

def get_labels(search_term='', print_labels=True):
    if not search_term:
        search_term = input("Enter a search term for the name of the labels (or 'b' to go back): ")
    
    if search_term.lower() == 'b':
        raise GoBackException

    headers = {
        'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
    }
    response = requests.get(f'{base_url}/groups.json', headers=headers)
    
    if response.status_code != 200:
        print("Error making request: received status code", response.status_code)
        return []

    data = response.json()
    
    matching_labels = [label for label in data['groups'] if search_term.lower() in label['name'].lower()]
    
    if print_labels:
        if matching_labels:
            print("Labels matching search term:")
            for label in matching_labels:
                print(f"{label['name']} (ID: {label['groupId']}) (Type: {label['type']})")
        else:
            print("No labels found matching search term")
    
    return matching_labels