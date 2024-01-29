import os
from test_manager import manage_tests

def get_oauth_token():
    oauth_token = input("Please enter your OAuth Bearer Token: ")
    os.environ['OAUTH_TOKEN'] = oauth_token

def select_option():
    print("Select the option you want to perform")
    print("1. Manage Tests")
    print("2. Manage Labels")
    print("3. Other")
    option = int(input("Enter the option number: "))
    return option

def main():
    print("Welcome to the ThousandEyes API program!")
    get_oauth_token()

    while True:
        try:
            option = select_option()
            if option == 1:
                # Import and call the function to Manage Tests
                manage_tests()
            elif option == 2:
                # Here import and call the function related to Manage Labels
                pass
            elif option == 3:
                # Here import and call other functions
                pass
            else:
                print("Invalid option selected")
        except Exception as e:
            if str(e) == "Return to main menu":
                print("Returning to main menu...")
                continue
            else:
                raise e  # If the exception is not "Return to main menu", re-raise it

if __name__ == "__main__":
    main()