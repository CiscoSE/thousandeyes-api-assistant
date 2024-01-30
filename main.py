import os
from test_manager import manage_tests
from label_manager import manage_labels

def get_oauth_token():
    oauth_token = input("Please enter your OAuth Bearer Token: ")
    os.environ['OAUTH_TOKEN'] = oauth_token

def select_option():
    print("Select the option you want to perform")
    print("1. Manage Tests")
    print("2. Manage Labels")
    print("3. Future...")
    print("4. Exit")
    option = int(input("Enter the option number: "))
    return option

def main():
    print("Welcome to the ThousandEyes API Assistant!")
    get_oauth_token()

    while True:
        try:
            option = select_option()
            if option == 1:
                # Import and call the function to Manage Tests
                manage_tests()
            elif option == 2:
                # Iport and call the function related to Manage Labels
                manage_labels()
            elif option == 3:
                # Here import and call other functions
                pass
            elif option == 4:
                print("Exiting program...")
                break
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