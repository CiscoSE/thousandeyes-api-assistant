from get_tests import get_tests, GoBackException
from create_test import create_test
from delete_test import delete_test
from update_tests import update_tests

def manage_tests():
    print("What would you like to do with your tests?")
    print("1. Get a list of tests")
    print("2. Create a test")
    print("3. Delete a test")
    print("4. Update a test")
    print("5. Go back to main menu")

    option = int(input("Enter the option number: "))
    
    try:
        if option == 1:
            get_tests()
        elif option == 2:
            create_test()
        elif option == 3:
            delete_test()
        elif option == 4:
            update_tests()
        elif option == 5:
            raise GoBackException("Return to main menu")
        else:
            print("Invalid option selected")
    except GoBackException:
        raise GoBackException("Return to main menu")