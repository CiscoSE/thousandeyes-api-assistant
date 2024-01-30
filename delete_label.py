import os
import requests
from get_labels import get_labels
from config import base_url

def get_label_details(groupId):
    headers = {
        'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
        'Content-Type': 'application/json',
    }
    response = requests.get(f"{base_url}/groups/{groupId}.json", headers=headers)
    return response.json()['groups'][0]

def delete_label():
    while True:
        label_name = input("Enter a label name to search (or 'b' to go back): ")
        if label_name.lower() == 'b':
            return  # Return to the previous menu
        labels = get_labels(label_name, print_labels=False)
        if labels:
            print(f"Found {len(labels)} labels:")
            for label in labels:
                print(f"Name: {label['name']}, ID: {label['groupId']}, Type: {label['type']}")
                label_details = get_label_details(label['groupId'])

                if 'tests' in label_details:
                    for test in label_details['tests']:
                        print(f"\tTest Name: {test['testName']} (ID: {test['testId']})")
                if 'agents' in label_details:
                    for agent in label_details['agents']:
                        print(f"\tAgent Name: {agent['agentName']} (ID: {agent['agentId']})")
                if 'endpointAgents' in label_details:
                    for agent in label_details['endpointAgents']:
                        print(f"\tEndpoint Agent Name: {agent['agentName']} (ID: {agent['agentId']})")
                if 'endpointTests' in label_details:
                    for test in label_details['endpointTests']:
                        print(f"\tEndpoint Test Name: {test['testName']} (ID: {test['testId']})")
                if 'dashboards' in label_details:
                    for dashboard in label_details['dashboards']:
                        print(f"\tDashboard Name: {dashboard['dashboardName']} (ID: {dashboard['dashboardId']})")
        else:
            print("No labels found. Please try again.")

        while True:
            search_again = False
            label_id = input("Enter the ID of the label you want to delete (or 's' to do another search): ")
            if label_id.lower() == 's':
                search_again = True
                break  # Break the inner loop to go back to the start of the outer loop
            try:
                label_id = int(label_id)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
            except IndexError:
                print("No label with this ID found. Please try again.")

        if search_again:
            continue # Continue to the start of the outer loop

        # Delete the label here
        headers = {
            'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
            'Content-Type': 'application/json',
        }

        response = requests.post(f"{base_url}/groups/{label_id}/delete.json", headers=headers)

        if response.status_code == 204:
            print("Label deleted successfully.")
        else:
            print("Error deleting label: received status code", response.status_code)