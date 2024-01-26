# ThousandEyes Test Manager

This project provides an automated solution for managing tests or labels in the ThousandEyes platform through their API. The primary purpose of this script is to make the process of adding and removing agents from tests, or adding, removing and updating labels more efficient.

The agent and test management processes can be a time-consuming task, especially when dealing with a large number of tests and agents. This script simplifies the process by automating it. 

You can manage agents for different types of tests in the ThousandEyes platform (currently only http-server & dns-server types). It allows you to search for a list of tests by name. Then it retrieves the test details, displays the agents for each test, and allows you to add or remove agents.

You can also create, delete, or update labels.

## Technology Stack

The scripts are written in Python and use the requests module to interact with the ThousandEyes API. The scripts are intended to be used as standalone programs.

## Status

The current version is 1.0.

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

Run the scripts:

```bash
python test_manager.py
```

or

```bash
python label_manager.py
```

When prompted, enter your OAuth Bearer Token, which is obtained from your ThousandEyes user page in your dashboard. https://docs.thousandeyes.com/product-documentation/getting-started/getting-started-with-the-thousandeyes-api#authentication

Enter a search term to search for the name of the tests or the labels you want to change. After the tests and their agents or the labels and their objects are displayed, choose whether you want to add or remove by entering 'add' or 'remove'. Then, enter the ID of the item you would like to add or remove from the tests or from the label you choose.

## Known issues 

If there are any known issues, they will be listed here.

## Getting help 

If you encounter any issues or have any questions about the script, please open an issue on GitHub.

## Credits and references 

1. [ThousandEyes API documentation](https://developer.thousandeyes.com/v6/)
