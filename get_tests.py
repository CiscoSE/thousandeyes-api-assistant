import os
import requests
from config import base_url

class GoBackException(Exception):
    pass

def get_tests(search_term='', print_tests=True):
    if not search_term:
            search_term = input("Enter a search term for the name of the tests (or 'b' to go back): ")
    
    if search_term.lower() == 'b':
        raise GoBackException

    headers = {
        'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
    }
    response = requests.get(f'{base_url}/tests.json', headers=headers)
    
    if response.status_code != 200:
        print("Error making request: received status code", response.status_code)
        return

    data = response.json()
    
    matching_tests = [test for test in data['test'] if search_term.lower() in test['testName'].lower()]
    
    if print_tests:
        if matching_tests:
            print("Tests matching search term:")
            for test in matching_tests:
                print(f"{test['testName']} (ID: {test['testId']}) (Type: {test['type']})")
        else:
            print("No tests found matching search term")
        return []
    
    return matching_tests