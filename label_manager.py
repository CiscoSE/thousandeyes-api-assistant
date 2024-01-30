from get_labels import get_labels
from create_label import create_label
from delete_label import delete_label
from update_label import update_label

def manage_labels():
    while True:
        print("\nLabel Manager Menu:")
        print("1. List Labels")
        print("2. Create a Label")
        print("3. Delete a Label")
        print("4. Update a Label")
        print("5. Go back to the main menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            get_labels()
        elif choice == '2':
            create_label()
        elif choice == '3':
            delete_label()
        elif choice == '4':
            update_label()
        elif choice == '5':
            break  # Exit the loop to go back to the main menu
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")