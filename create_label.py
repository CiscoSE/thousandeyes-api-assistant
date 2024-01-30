import os
import requests
from update_label import update_label
from config import base_url

def create_label():
    # List of supported label types
    label_types = ["agents", "tests", "endpoint-agents", "endpoint-tests", "dashboards"]
    
    print("Select the type of label you want to create:")
    for i, label_type in enumerate(label_types, start=1):
        print(f"{i}. {label_type}")

    while True:
        type_choice = input("Enter your choice (or 'b' to go back): ")
        if type_choice.lower() == 'b':
            return  # Return to the previous menu
        try:
            label_type = label_types[int(type_choice) - 1]
            break
        except (IndexError, ValueError):
            print("Invalid choice. Please enter a number between 1 and", len(label_types))

    label_name = input("Enter a name for the label: ")

    headers = {
        'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
        'Content-Type': 'application/json',
    }
    data = {
        'name': label_name,
    }
    response = requests.post(f"{base_url}/groups/{label_type}/new.json", headers=headers, json=data)

    if response.status_code == 201:  # 201 Created is standard response for successful HTTP POST requests
        label = response.json()['groups'][0]
        print(f"Label '{label['name']}' created successfully. ID: {label['groupId']}, Type: {label['type']}")
        print("Enter 'u' to update this label, or 'b' to go back to the label manager.")
        while True:
            next_action = input("Enter your choice: ")
            if next_action.lower() == 'b':
                return
            elif next_action.lower() == 'u':
                update_label(label['groupId'])
                break
            else:
                print("Invalid choice. Please enter 'u' or 'b'.")
    else:
        print("Error creating label: received status code", response.status_code)