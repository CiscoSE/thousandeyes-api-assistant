import requests
import json
import os

# Prompt the user to enter their OAuth Bearer token
bearer_token = input("Enter your OAuth Bearer token: ")

# Temporarily store it as an environment variable
os.environ['BEARER_TOKEN'] = bearer_token

# Define the base URL
base_url = "https://api.thousandeyes.com/v6"

# Define the headers for your requests
headers = {
    "Authorization": f"Bearer {os.environ.get('BEARER_TOKEN')}",
    "Content-Type": "application/json",
}

# Main function
def main():
    while True:
        action = input("What would you like to do? Enter 'create', 'update', 'delete', or 'quit': ")

        if action == 'create':
            create_label()
        elif action == 'update':
            update_label()
        elif action == 'delete':
            delete_label()
        elif action == 'quit':
            print("You've chosen to quit. Goodbye!")
            break
        else:
            print("Invalid action. Please enter 'create', 'update', 'delete', or 'quit'.")

# Create a label function
def create_label():
    valid_types = ['tests', 'agents', 'endpoint_agents', 'dashboards']
    label_type = input("Enter the type of label you want to create (tests, agents, endpoint_agents, or dashboards): ")

    # Keep asking for input until a valid type is entered
    while label_type not in valid_types:
        print("Invalid label type.")
        label_type = input("Enter a valid type of label (tests, agents, endpoint_agents, or dashboards): ")

    label_name = input("Enter the name for the new label: ")

    # Define the URL for creating a new label
    create_url = f"{base_url}/groups/{label_type}/new.json"

    # Define the data for the new label based on the label type
    if label_type == 'tests':
        label_data = {"name": label_name, "tests": []}
    elif label_type == 'agents':
        label_data = {"name": label_name, "agents": []}
    elif label_type == 'endpoint_agents':
        label_data = {"name": label_name, "endpoint_agents": []}
    elif label_type == 'dashboards':
        label_data = {"name": label_name, "dashboards": []}
    else:
        print("Invalid label type.")
        return

    # Send a POST request to create the new label
    response = requests.post(create_url, headers=headers, data=json.dumps(label_data))

    # Check if the request was successful
    if response.status_code == 201:
        print(f"Successfully created a new {label_type} label named {label_name}.")
    else:
        print(f"Failed to create label Error: {response.text}")

def update_label():
    while True:
        labels = fetch_labels()
        if labels is None:
            break

        search_term = input("Enter a search term, leave blank to display all labels, or 'quit' to go back to the main menu: ")
        if search_term.lower() == 'quit':
            break

        display_labels(labels, search_term)

        while True:  # New loop for user_choice
            user_choice = input("Enter 'u' to update a label, 's' to do another search, or 'quit' to go back to the main menu: ")

            if user_choice.lower() == 'quit':
                return
            elif user_choice.lower() == 's':
                break  # This will break the inner loop and go back to the start of the outer loop
            elif user_choice.lower() == 'u':
                label_id = get_label_id()
                if label_id == 'quit':
                    return
                elif label_id == 's':
                    break  # This will break the inner loop and go back to the start of the outer loop

                label = fetch_label_details(label_id)
                if label is None:
                    continue  # This will continue the inner loop and re-prompt for user_choice

                item_type, label_name = get_label_type_and_name(label)

                action = get_action()
                if action == 'quit':
                    return
                elif action == 's':
                    break  # This will break the inner loop and go back to the start of the outer loop

                item_ids = get_item_ids()
                if item_ids == 'quit':
                    return
                elif item_ids == 's':
                    break  # This will break the inner loop and go back to the start of the outer loop

                success = perform_update(label_id, action, item_type, label_name, item_ids)
                if not success:
                    print(f"Failed to update label with ID {label_id}.")
                break  # If update was successful, break the inner loop and go back to the start of the outer loop
            else:
                print("Invalid choice. Please enter 'u' to update a label, 's' to do another search, or 'quit' to go back to the main menu.")

def fetch_labels():
    labels_url = f"{base_url}/groups.json"
    response = requests.get(labels_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve labels. Error: {response.text}")
        return None

    return response.json()['groups']

def display_labels(labels, search_term):
    # Filter the labels based on the search term
    labels = [label for label in labels if search_term in label['name']]

    # Sort the labels in alphabetical order by name
    labels = sorted(labels, key=lambda x: x['name'])

    # Display the list of existing labels
    for label in labels:
        detail_url = f"{base_url}/groups/{label['groupId']}.json"
        detail_response = requests.get(detail_url, headers=headers)

        if detail_response.status_code == 200 and detail_response.text.strip():
            detail = detail_response.json()

            # Get the groups for each label
            groups = detail.get('groups', [])

            for group in groups:
                print(f"Label ID: {group.get('groupId')}, Group Name: {group.get('name')}")

                if 'tests' in group:
                    for test in group['tests']:
                        print(f"  Test ID: {test.get('testId')}, Test Name: {test.get('testName')}")

                if 'agents' in group:
                    for agent in group['agents']:
                        print(f"  Agent ID: {agent.get('agentId')}")

                if 'endpointAgents' in group:
                    for endpoint_agent in group['endpointAgents']:
                        print(f"  Endpoint Agent ID: {endpoint_agent.get('endpointAgentId')}")

                if 'dashboardIds' in group:
                    for dashboard_id in group['dashboardIds']:
                        print(f"  Dashboard ID: {dashboard_id}")

        else:
            print(f"No details available for label with ID {label['groupId']}.")

def get_label_id():
    return input("Enter the ID of the label you want to update, 's' to do another search, or 'quit' to go back to the main menu: ")

def fetch_label_details(label_id):
    try:
        label_id = int(label_id)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

    # Fetch the latest data for the label
    detail_url = f"{base_url}/groups/{label_id}.json"
    detail_response = requests.get(detail_url, headers=headers)

    if detail_response.status_code != 200 or not detail_response.text.strip():
        print(f"No details available for label with ID {label_id}.")
        return None

    return detail_response.json()

def get_label_type_and_name(label):
    for group in label.get('groups', []):
        if 'tests' in group:
            return 'tests', group['name']
        if 'agents' in group:
            return 'agents', group['name']
        if 'endpointAgents' in group:
            return 'endpointAgents', group['name']
        if 'dashboardIds' in group:
            return 'dashboardIds', group['name']

def get_action():
    return input("Would you like to add or remove an item from the label? Enter 'add', 'remove', 's' to do another search, or 'quit' to go back to the main menu: ")

def get_item_ids():
    item_id = input("Enter a comma separated list of the IDs you want to add or remove from the label, 's' to do another search, or 'quit' to go back to the main menu: ")

    try:
        return [int(item.strip()) for item in item_id.split(",")]
    except ValueError:
        print("Invalid input. Please enter a comma-separated list of numbers.")
        return None

def perform_update(label_id, action, item_type, label_name, item_ids):
    array_name_mapping = {
        "tests": "tests",
        "agents": "agents",
        "endpoint_tests": "endpointTests",
        "endpoint_agents": "endpointAgents",
        "dashboards": "dashboardIds"
    }
    array_name = array_name_mapping[item_type]
    update_data = {"name": label_name}

    new_item_ids = [{f"{item_type[:-1]}Id": item_id} for item_id in item_ids]
    existing_item_ids = get_existing_item_ids(label_id, array_name)
    existing_item_ids_objects = [{f"{item_type[:-1]}Id": item_id} for item_id in existing_item_ids]

    if action == 'add':
        update_data[array_name] = existing_item_ids_objects + [item for item in new_item_ids if item not in existing_item_ids_objects]
    elif action == 'remove':
        update_data[array_name] = [item for item in existing_item_ids_objects if item not in new_item_ids]

    update_url = f"{base_url}/groups/{label_id}/update.json"
    response = requests.post(update_url, headers=headers, json=update_data)

    if response.status_code == 200:
        print(f"Successfully updated label with ID {label_id}.")
        return True
    else:
        print(f"Failed to update label with ID {label_id}. Error: {response.text}")
        return False

def get_existing_item_ids(label_id, array_name):
    detail_url = f"{base_url}/groups/{label_id}.json"
    detail_response = requests.get(detail_url, headers=headers)

    if detail_response.status_code == 200:
        detail_data = detail_response.json()
        existing_item_ids = [item[f"{array_name[:-1]}Id"] for item in detail_data["groups"][0][array_name]]
    else:
        print(f"Failed to get existing item IDs for label with ID {label_id}. Error: {detail_response.text}")
        existing_item_ids = []

    return existing_item_ids

# Delete a label function
def delete_label():
    # Retrieve the list of existing labels
    labels_url = f"{base_url}/groups.json"
    response = requests.get(labels_url, headers=headers)

    if response.status_code == 200:
        labels = response.json()['groups']

        # Sort the labels in alphabetical order by name
        labels = sorted(labels, key=lambda x: x['name'])

        # Display the list of existing labels
        for label in labels:
            print(f"ID: {str(label['groupId'])}, Type: {label['type']}, Name: {label['name']}")

        # Ask the user for the ID of the label they want to delete
        label_id = input("Enter the ID of the label you want to delete, or 'back' to return to the main menu: ")

        # Keep asking for input until a valid ID or 'back' is entered
        while not label_id.isdigit() and label_id != 'back':
            print("Invalid input.")
            label_id = input("Enter a valid ID or 'back': ")

        if label_id == 'back':
            return

        label_id = int(label_id)

        # Define the URL for deleting the label
        delete_url = f"{base_url}/groups/{label_id}/delete.json"

        # Send a DELETE request to delete the label
        response = requests.delete(delete_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 204:
            print(f"Successfully deleted label {label_id}.")
        else:
            print(f"Failed to delete label {label_id}. Error: {response.text}")
    else:
        print(f"Failed to retrieve labels. Error: {response.text}")
    pass

if __name__ == "__main__":
    main()
