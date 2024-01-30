import os
import requests
import json
from config import base_url

def create_test():
    test_types = [
        "agent-to-server", "agent-to-agent", "bgp", "http-server", "page-load", 
        "web-transactions", "ftp-server", "dns-trace", "dns-server", "dns-dnssec", 
        "sip-server", "voice"
    ]
    
    print("Choose a test type from the following list:")
    for i, test_type in enumerate(test_types, start=1):
        print(f"{i}. {test_type}")
    
    test_type_choice = int(input("Enter the number of your choice: "))
    # Ensure the user's choice is within the correct range
    if test_type_choice not in range(1, len(test_types) + 1):
        print("Invalid choice. Please enter a number corresponding to a test type.")
        return
    
    test_type = test_types[test_type_choice - 1]
    test_name = input("Enter a name for your test: ")

    intervals_in_seconds = [60, 120, 300, 600, 900, 1800, 3600]
    print("Choose an interval from the following list (in minutes):")
    for i, interval in enumerate(intervals_in_seconds, start=1):
        print(f"{i}. {interval//60}")  # Convert seconds to minutes for display

    interval_choice = int(input("Enter the number of your choice: "))
    # Ensure the user's choice is within the correct range
    if interval_choice not in range(1, len(intervals_in_seconds) + 1):
        print("Invalid choice. Please enter a number corresponding to an interval.")
        return

    interval = intervals_in_seconds[interval_choice - 1]  # The interval in seconds

    # Dictionary to store test attributes
    test_attributes = {}

    # Common required attributes for all tests
    common_attributes = {
        'testName': test_name,
        'agents': [{'agentId': int(input("Enter agent ID: "))}],
        'interval': interval
    }

    test_attributes.update(common_attributes)

    if test_type in ["agent-to-server", "http-server", "ftp-server"]:
        test_attributes['server'] = input("Enter server IP or FQDN: ")

    elif test_type == "agent-to-agent":
        test_attributes['targetAgentId'] = int(input("Enter target agent ID: "))

    elif test_type in ["dns-server", "dns-trace"]:
        test_attributes['dnsServers'] = [{'serverName': input("Enter FQDN of server: ")}]
        test_attributes['domain'] = input("Enter domain: ")

    elif test_type in ["http-server", "page-load", "web-transactions"]:
        test_attributes['url'] = input("Enter URL: ")

    elif test_type == "web-transactions":
        test_attributes['transactionScript'] = input("Enter transaction script: ")

    elif test_type == "ftp-server":
        test_attributes.update({
            'password': input("Enter password: "),
            'requestType': input("Enter request type (Download, Upload, List): "),
            'username': input("Enter username: "),
        })

    elif test_type == "sip-server":
        test_attributes.update({
            'port': int(input("Enter port: ")),
            'sipRegistrar': input("Enter SIP registrar: "),
            'targetSipCredentials': {
                'port': int(input("Enter target SIP credentials port: ")),
                'sipRegistrar': input("Enter target SIP registrar: ")
            }
        })

    elif test_type == "voice":
        test_attributes['targetAgentId'] = int(input("Enter target agent ID: "))

    # Make the API request to create the test
    headers = {
        'Authorization': 'Bearer ' + os.environ['OAUTH_TOKEN'],
        'Content-Type': 'application/json'
    }
    response = requests.post(f'{base_url}/tests/{test_type}/new.json', headers=headers, data=json.dumps(test_attributes))

    if response.status_code != 201:
        print("Error making request: received status code", response.status_code)
        return

    print("Test created successfully!")