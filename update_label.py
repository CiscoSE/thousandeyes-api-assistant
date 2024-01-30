import os
import requests
from get_labels import get_labels

def get_label_details(groupId):
    headers = {
        'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
        'Content-Type': 'application/json',
    }
    response = requests.get(f"https://api.thousandeyes.com/v6/groups/{groupId}.json", headers=headers)
    return response.json()['groups'][0]

def update_label():
    while True:
        label_name = input("Enter a label name to search (or 'b' to go back): ")
        if label_name.lower() == 'b':
            return  # Return to the previous menu
        labels = get_labels(label_name)
        if labels:
            print(f"Found {len(labels)} labels:")
            for label in labels:
                print(f"Name: {label['name']}, ID: {label['groupId']}, Type: {label['type']}")
                label_details = get_label_details(label['groupId'])
                print(f"Details for label '{label['name']}' (ID: {label['groupId']})")
                
                if label['type'] == 'tests':
                    for test in label_details['tests']:
                        print(f"\tTest Name: {test['testName']} (ID: {test['testId']})")
                elif label['type'] == 'agents':
                    for agent in label_details['agents']:
                        print(f"\tAgent Name: {agent['agentName']} (ID: {agent['agentId']})")
                elif label['type'] == 'endpoint-agents':
                    for agent in label_details['endpointAgents']:
                        print(f"\tEndpoint Agent Name: {agent['agentName']} (ID: {agent['agentId']})")
                elif label['type'] == 'endpoint-tests':
                    for test in label_details['endpointTests']:
                        print(f"\tEndpoint Test Name: {test['testName']} (ID: {test['testId']})")
                elif label['type'] == 'dashboards':
                    for dashboard in label_details['dashboards']:
                        print(f"\tDashboard Name: {dashboard['dashboardName']} (ID: {dashboard['dashboardId']})")
        else:
            print("No labels found. Please try again.")

        while True:
            action = input("Enter 'a' to add an object, 'r' to remove an object, or 's'  to do another search: ")
            if action.lower() == 'a':
                update_action = "add"
                break
            elif action.lower() == 'r':
                update_action = "remove"
                break
            elif action.lower() == 's':
                break  # Break the inner loop to go back to the start of the outer loop
            else:
                print("Invalid choice. Please enter 'a', 'r', or 's'.")

        if action.lower() == 's':
            continue  # Continue to the start of the outer loop

        while True:
            label_search_again = False
            label_id = input("Enter the ID of the label you want to update (or 's' to do another search): ")
            if label_id.lower() == 's':
                label_search_again = True
                break  # Break the inner loop to go back to the start of the outer loop
            try:
                label_id = int(label_id)
                label = get_label_details(label_id)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
            except IndexError:
                print("No label with this ID found. Please try again.")

        if label_search_again:
            continue  # Continue to the start of the outer loop

        while True:
            object_search_again = False
            object_id = input("Enter the ID of the object you want to " + update_action + " (or 's' to do another search): ")
            if object_id.lower() == 's':
                object_search_again = True
                break  # Break the inner loop to go back to the start of the outer loop
            try:
                object_id = int(object_id)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        if object_search_again:
            continue  # Continue to the start of the outer loop

        # Update the label here
        headers = {
            'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
            'Content-Type': 'application/json',
        }

        object_type = label['type']
        if object_type == 'tests':
            objects = [{"testId": obj['testId']} for obj in label['tests']]
        elif object_type == 'agents':
            objects = [{"agentId": obj['agentId']} for obj in label['agents']]
        elif object_type == 'endpoint-agents':
            objects = [{"agentId": obj['agentId']} for obj in label['endpointAgents']]
        elif object_type == 'endpoint-tests':
            objects = [{"testId": obj['testId']} for obj in label['endpointTests']]
        elif object_type == 'dashboards':
            objects = [{"dashboardId": obj['dashboardId']} for obj in label['dashboards']]

        if update_action == 'add':
            if object_type in ['tests', 'endpoint-tests']:
                objects.append({'testId': object_id})
            else:
                objects.append({'agentId': object_id})
        else:
            objects = [obj for obj in objects if list(obj.values())[0] != object_id]

        data = {
            'name': label['name'],  # Include the label name in the request body
            object_type: objects
        }

        response = requests.post(f"https://api.thousandeyes.com/v6/groups/{label_id}/update.json", headers=headers, json=data)

        if response.status_code == 200:
            print("Label updated successfully.")
        else:
            print("Error updating label: received status code", response.status_code)