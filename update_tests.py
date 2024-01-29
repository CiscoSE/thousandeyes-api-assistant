import os
import requests
import json
from get_tests import get_tests
import concurrent.futures
import itertools
import threading
import time

class LoadingIndicator: # The API is a bit slow when updating tests, so this creates a simple Loading indicator

    def __init__(self, message="Loading"):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.running = False
        self.thread = None
        self.message = message

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._spin)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _spin(self):
        while self.running:
            print(f"{self.message}... {next(self.spinner)}", end='\r')
            time.sleep(0.1)
        # Clear the line and print "Done" when finished loading
        print(f"{self.message}... Done" + ' ' * 10, end='\r')

def update_test(test, agent_id, action, headers):
    test_id = test['testId']
    response = requests.get(f'https://api.thousandeyes.com/v6/tests/{test_id}.json', headers=headers)
    if response.status_code != 200:
        print(f"Error getting details for test {test_id}: received status code", response.status_code)
        return

    test_detail = response.json()
    agents = test_detail['test'][0]['agents']

    if action == 'add':
        # Add the new agent to the list
        agents.append({"agentId": agent_id})
    elif action == 'remove':
        # Remove the agent from the list
        agents = [agent for agent in agents if agent['agentId'] != agent_id]
    else:
        print(f"Invalid action {action}, skipping test {test_id}")
        return

    body = {
        "agents": agents
    }

    test_type = test['type']
    response = requests.post(f'https://api.thousandeyes.com/v6/tests/{test_type}/{test_id}/update.json', headers=headers, data=json.dumps(body))

    if response.status_code != 200:
        print(f"Error updating test {test_id}: received status code", response.status_code)
    else:
        print(f"Successfully updated test {test_id}")


def update_tests():
    while True:  # This loop will continue until the user chooses to stop
        search_term = input("Enter a search term to find the tests you want to update (or 'b' to go back to the main menu): ")
        if search_term.lower() == 'b':
            raise Exception("Return to main menu")  # Raise an exception to go back to the main menu

        matching_tests = get_tests(search_term, print_tests=False)

        if not matching_tests:
            print("No tests found matching search term")
            continue  # Skip the rest of this iteration and start the next one

        headers = {
            'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
            'Content-Type': 'application/json',  
        }

        print("Matching tests and their agents:")
        for test in matching_tests:
            test_id = test['testId']
            response = requests.get(f'https://api.thousandeyes.com/v6/tests/{test_id}.json', headers=headers)
            if response.status_code != 200:
                print(f"Error getting details for test {test_id}: received status code", response.status_code)
                continue

            test_detail = response.json()
            agents = test_detail['test'][0]['agents']

            print(f"Test Name: {test['testName']}, Test ID: {test_id}")
            for agent in agents:
                print(f"\tAgent Name: {agent['agentName']}, Agent ID: {agent['agentId']}")

        action = input("Would you like to add or remove an agent, or perform a new search? Enter 'add', 'remove', or 'new': ")
        if action == 'add':
            print("You will be adding an agent to the list of tests.")
        elif action == 'remove':
            print("You will be removing an agent from the list of tests.")
        elif action == 'new':
            continue

        while True:  # This loop will continue until the user enters a valid agent ID or chooses to go back
            agent_id_input = input("Enter the ID of the agent to add or remove (or 'b' to go back): ")
            if agent_id_input.lower() == 'b':
                break  # If the user enters 'b', stop this loop and go back to the action prompt
            
            try:
                agent_id = int(agent_id_input)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue  # If the user enters an invalid number, continue to the next iteration of this loop

            loading_indicator = LoadingIndicator(message="Updating tests")
            loading_indicator.start()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                        executor.map(update_test, matching_tests, [agent_id]*len(matching_tests), [action]*len(matching_tests), [headers]*len(matching_tests))

            loading_indicator.stop()

            print("Finished updating tests.")
            break  # If we've gotten this far, the user entered a valid agent ID, so we can stop this loop