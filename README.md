# ThousandEyes API Assistant

This project provides an automated solution for managing various entities such as tests and labels in the ThousandEyes platform through their API. The primary purpose of this script is to make the process of managing these entities more efficient.

## Features

Currently, the script supports managing agents for different types of tests in the ThousandEyes platform. It allows you to:

- Search for a list of tests by name.
- Retrieve and display the test details, along with the associated agents.
- Add or remove agents from the tests.

In the future, it will also support managing labels (creating, deleting, updating). This functionality is currently under development.

## Technology Stack

The script is written in Python and uses the requests module to interact with the ThousandEyes API.

## Status

The current version is 1.1. This version introduces several code improvements to make the script more modular and easier to maintain.

Label management functionality is planned for version 1.2.

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
python main.py
```

When prompted, enter your OAuth Bearer Token, which is obtained from your ThousandEyes user page in your dashboard. https://docs.thousandeyes.com/product-documentation/getting-started/getting-started-with-the-thousandeyes-api#authentication

Choose 1 to manage tests.

From the Test Management menu choose 1 to get a list of your tests or 4 to update your tests (create and deleting tests will be future functionality).


Enter a search term to search for the name of the tests you want to update. After the tests and their agents or the labels and their objects are displayed, choose whether you want to add or remove by entering 'add' or 'remove'. Then, enter the ID of the agent you would like to add or remove from the tests.

## Known issues 

If there are any known issues, they will be listed here.

## Getting help 

If you encounter any issues or have any questions about the script, please open an issue on GitHub.

## Credits and references 

1. [ThousandEyes API documentation](https://developer.thousandeyes.com/v6/)
