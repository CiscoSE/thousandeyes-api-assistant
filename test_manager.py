import os
import requests
import json
from concurrent.futures import ThreadPoolExecutor
import threading
import time

# add_agent function
def add_agent(testId, agentIds, testType, test):
    # Define the URL for the current test
    test_url = f"{base_url}/tests/{testType}/{testId}/update.json"

    # Define the data for the current test
    if testType == 'dns-server':
        test_data = {
            "agents": [{"agentId": agentId} for agentId in agentIds],
            "interval": test["interval"],
            "domain": test["domain"]
        }
    elif testType == 'http-server':
        test_data = {
            "agents": [{"agentId": agentId} for agentId in agentIds],
            "interval": test["interval"],
            "url": test["url"]
        }

    # Send a POST request to update the agents for the current test
    for _ in range(3):  # Try up to 3 times
        response = requests.post(test_url, headers=headers, data=json.dumps(test_data))
        if response.status_code == 200:
            print(f"\nSuccessfully updated agents for {testId}.")
            break
        else:
            print(f"\nFailed to update agents for {testId}. Error: {response.text}. Retrying...")
    else:
        print(f"\nFailed to update agents for {testId} after 3 attempts.")

# remove_agent function
def remove_agent(testId, agentIds, testType, test):
    # Define the URL for the current test
    test_url = f"{base_url}/tests/{testType}/{testId}/update.json"

    # Define the data for the current test
    if testType == 'dns-server':
        test_data = {
            "agents": [{"agentId": agentId} for agentId in agentIds],
            "interval": test["interval"],
            "domain": test["domain"]
        }
    elif testType == 'http-server':
        test_data = {
            "agents": [{"agentId": agentId} for agentId in agentIds],
            "interval": test["interval"],
            "url": test["url"]
        }

    # Send a POST request to update the agents for the current test
    for _ in range(3):  # Try up to 3 times
        response = requests.post(test_url, headers=headers, data=json.dumps(test_data))
        if response.status_code == 200:
            print(f"\nSuccessfully removed agent from {testId}.")
            break
        else:
            print(f"\nFailed to remove agent from {testId}. Error: {response.text}. Retrying...")
    else:
        print(f"\nFailed to remove agent from {testId} after 3 attempts.")

# Define a function to add or remove an agent
def update_agent(action, testId, agentIds, testType, test):
    if action == 'add':
        add_agent(testId, agentIds, testType, test)
    elif action == 'remove':
        remove_agent(testId, agentIds, testType, test)

# Define a function for a progress indicator
def print_dots(stop_event):
    while not stop_event.is_set():
        print('.', end='', flush=True)
        time.sleep(1)

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

class QuitException(Exception): pass

try:
    while True:
        # Ask the user to search for test names containing a word
        name_search = input("Enter the name of the tests to search for, or 'quit' to exit: ")

        if name_search.lower() == 'quit':
            print("You've chosen to quit. Goodbye!")
            raise QuitException

        # Send a GET request to retrieve the tests with the given label
        response = requests.get(f"{base_url}/tests.json", headers=headers)

        # Start a thread for the progress indicator
        stop_event = threading.Event()
        dot_thread = threading.Thread(target=print_dots, args=(stop_event,))
        dot_thread.start()

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract the tests
            tests = [test for test in data["test"] if name_search in test["testName"]]

            # Prepare a dictionary to hold test and agent data
            test_agents_dict = {}

            # Iterate through the tests
            for test in tests:
                # Define the URL for the current test details
                test_detail_url = f"{base_url}/tests/{test['testId']}.json"

                # Send a GET request to retrieve the current test details
                response = requests.get(test_detail_url, headers=headers)

                if response.status_code == 200:
                    # Parse the JSON response
                    test_detail_data = response.json()

                    # Extract the agent IDs and names for each test
                    agents = [{"agentId": agent["agentId"], "agentName": agent["agentName"]} for agent in test_detail_data["test"][0]["agents"]]

                    # Check the test type and prepare the test data accordingly
                    if test['type'] == 'dns-server':
                        test_data = {
                            "testName": test['testName'],
                            "testType": test['type'],
                            "agents": agents,
                            "interval": test_detail_data["test"][0]["interval"],
                            "domain": test_detail_data["test"][0]["domain"],
                        }
                    elif test['type'] == 'http-server':
                        test_data = {
                            "testName": test['testName'],
                            "testType": test['type'],
                            "agents": agents,
                            "interval": test_detail_data["test"][0]["interval"],
                            "url": test_detail_data["test"][0]["url"],
                        }

                    # Add the test and its data to the dictionary
                    test_agents_dict[test['testId']] = test_data
                else:
                    print(f"\nFailed to retrieve agents for {test['testName']}. Error: {response.text}")

            # Stop the progress indicator
            stop_event.set()
            dot_thread.join()

            # Display all tests and their agents
            for testId, testData in test_agents_dict.items():
                print(f"\nTest {testData['testName']} (ID: {testId}) has the following agents:")
                for agent in testData["agents"]:
                    print(f"  ID: {agent['agentId']}, Name: {agent['agentName']}")
                print()

            # Create a ThreadPoolExecutor
            executor = ThreadPoolExecutor(max_workers=10)

            while True:
                # Ask the user whether they want to add or remove an agent, or quit
                action = input("Do you want to add or remove an agent from these tests, do another search, or quit the script? Enter 'add', 'remove', 'search', or 'quit': ")

                if action == 'add':
                    # Prompt the user to enter the agent ID and name they would like to add
                    new_agent_id = input("Enter the ID of the agent you would like to add to these tests, or 'back' to return to the previous menu: ")

                    # Check if the user wants to go back
                    if new_agent_id.lower() == 'back':
                        continue

                    new_agent_id = int(new_agent_id)  # Convert the input to an integer

                    # Start a thread for the progress indicator
                    stop_event = threading.Event()
                    dot_thread = threading.Thread(target=print_dots, args=(stop_event,))
                    dot_thread.start()

                    # Iterate over all tests and add the new agent to each test
                    for testId, testData in test_agents_dict.items():
                        # Add the new agent to the list of agents
                        testData["agents"].append({"agentId": new_agent_id})

                        # Submit the update_agent function to the executor
                        executor.submit(update_agent, 'add', testId, [agent["agentId"] for agent in testData["agents"]], testData['testType'], testData)

                    # Wait for all tasks to complete
                    executor.shutdown(wait=True)

                    # Stop the progress indicator
                    stop_event.set()
                    dot_thread.join()

                    # Break out of the inner loop to return to the search dialogue
                    break

                elif action == 'remove':
                    # Prompt the user to enter the agent ID they would like to remove
                    removed_agent_id = input("Enter the ID of the agent you would like to remove from these tests, or 'back' to return to the previous menu: ")

                    # Check if the user wants to go back
                    if removed_agent_id.lower() == 'back':
                        continue

                    removed_agent_id = int(removed_agent_id)  # Convert the input to an integer

                    # Start a thread for the progress indicator
                    stop_event = threading.Event()
                    dot_thread = threading.Thread(target=print_dots, args=(stop_event,))
                    dot_thread.start()

                    # Iterate over all tests and remove the specified agent from each test
                    for testId, testData in  test_agents_dict.items():
                        # Remove the agent from the list of agents
                        testData["agents"] = [agent for agent in testData["agents"] if agent["agentId"] != removed_agent_id]

                        # Submit the update_agent function to the executor
                        executor.submit(update_agent, 'remove', testId, [agent["agentId"] for agent in testData["agents"]], testData['testType'], testData)

                    # Wait for all tasks to complete
                    executor.shutdown(wait=True)

                    # Stop the progress indicator
                    stop_event.set()
                    dot_thread.join()

                    # Break out of the inner loop to return to the search dialogue
                    break

                elif action == 'quit':
                    print("You've chosen to quit. Goodbye!")
                    executor.shutdown(wait=True)
                    raise QuitException

                elif action == 'search':
                    print("Starting a new search...")
                    break

                else:
                    print("Invalid action. Please enter 'add', 'remove', 'search', or 'quit'.")
                    # Make sure to clean up the executor when you are done
                    executor.shutdown()
        else:
            print(f"Failed to retrieve tests. Error: {response.text}")
except QuitException:
    pass