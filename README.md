# ThousandEyes API Assistant

This project provides an automated solution for managing various entities such as tests and labels in the ThousandEyes platform through their API. The primary purpose of this script is to make the process of managing these entities more efficient and user-friendly.

## Features

The script now supports managing both tests and labels in the ThousandEyes platform. It allows you to:

- Get a list of all tests or labels.
- Create a new test or label.
- Delete an existing test or label.
- Update a test or label.

## Technology Stack

The script is written in Python and uses the requests module to interact with the ThousandEyes API.

## Status

The current version is 1.2. This version introduces label management functionality, making the script more versatile and useful.

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

Choose 1 to manage tests, or 2 to manage labels. From the Test or Label Management menu, you can choose to list, create, delete, or update entities.

## Known issues 

If there are any known issues, they will be listed here.

## Getting help 

If you encounter any issues or have any questions about the script, please open an issue on GitHub.

## Credits and references 

1. [ThousandEyes API documentation](https://developer.thousandeyes.com/v6/)
