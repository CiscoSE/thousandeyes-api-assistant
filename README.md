# ThousandEyes Test Manager

This project provides an automated solution for managing tests in the ThousandEyes platform through their API. The primary purpose of this script is to make the process of adding and removing agents from tests more efficient. 

The agent management process can be a time-consuming task, especially when dealing with a large number of tests and agents. This script simplifies the process by automating it. 

You can manage agents for different types of tests in the ThousandEyes platform (currently only http-server & dns-server types). It allows you to search for a list of tests by name. Then it retrieves the test details, displays the agents for each test, and allows you to add or remove agents.

## Technology Stack

The script is written in Python and uses the requests module to interact with the ThousandEyes API. The script is intended to be used as a standalone program.

## Status

The current version of the script is 1.0.

## Installation 

Make sure you have Python installed on your machine.

Clone the repository:

```bash
git clone https://github.com/CiscoSE/thousandeyes-api-assistant.git
cd thousandeyes-api-assistant
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage 

Run the script:

```bash
python agent_manager.py
```

When prompted, enter your OAuth Bearer Token, which is obtained from your ThousandEyes user page in your dashboard. https://docs.thousandeyes.com/product-documentation/getting-started/getting-started-with-the-thousandeyes-api#authentication

Enter a search term to search for the name of the tests you want to change. After the tests and their agents are displayed, choose whether you want to add or remove an agent by entering 'add' or 'remove'. Then, enter the ID of the agent you would like to add or remove.

## Known issues 

If there are any known issues, they will be listed here.

## Getting help 

If you encounter any issues or have any questions about the script, please open an issue on GitHub.

## Credits and references 

1. [ThousandEyes API documentation](https://developer.thousandeyes.com/v6/)
