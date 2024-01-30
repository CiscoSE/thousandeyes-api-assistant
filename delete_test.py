import os
import requests
from get_tests import get_tests, GoBackException

def delete_test():
    while True:
        search_term = input("Enter a search term to find the tests you want to delete (or 'b' to go back to the main menu): ")
        if search_term.lower() == 'b':
            raise Exception("Return to main menu")  # Raise an exception to go back to the main menu

        matching_tests = get_tests(search_term, print_tests=False)

        if not matching_tests:
            print("No tests found matching search term")
            continue  # Skip the rest of this iteration and start the next one

        # Print the matching tests
        print("Tests matching search term:")
        for test in matching_tests:
            print(f"{test['testName']} (ID: {test['testId']}) (Type: {test['type']})")

        delete_choice = input("Enter the Test ID to delete or 's' to do another search: ")
        if delete_choice.lower() == 's':
            continue

        # Get the test details
        headers = {
            'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
        }
        response = requests.get(f"https://api.thousandeyes.com/v6/tests/{delete_choice}.json", headers=headers)
        if response.status_code == 200:  # 200 OK means the request was successful
            test_details = response.json()
            test_type = test_details['test'][0]['type']

            # Delete the test
            response = requests.delete(f"https://api.thousandeyes.com/v6/tests/{test_type}/{delete_choice}/delete.json", headers=headers)
            if response.status_code == 204:  # 204 No Content is standard response for successful HTTP DELETE requests
                print(f"Test with ID {delete_choice} deleted successfully.")
            else:
                print("Error deleting test: received status code", response.status_code)
        else:
            print("Invalid Test ID.")