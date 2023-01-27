import os
import sys

from utils import passkeep_get
from utils import passkeep_save
from utils import passkeep_del
from models.connection import ConnectionModel


def actions(user):
    iterated = False
    user_action = 0
    conn = ConnectionModel(user)
    while True:
        print(
            f"\nChoose an action to start PassKeeping:\n\tActive user: {user.username}\n\n[1] generate and store new password,\n[2] retrieve and view all saved sources,\n[3] search and retrieve a source by name,\n[4] search for a source and delete the entry,\n[5] quit"
            if not iterated
            else "\n--anything else?\n1) generate,  2) get-all,  3) search,  4) delete,  5) quit"
        )
        iterated = True
        user_action = input(">> ")
        if user_action == "1" or user_action == "":
            save_res = passkeep_save.save_action(conn)
            print(
                "\nSuccess.\nYour requested data was submitted successfully. you can use retrieval actions to view the password at anytime..."
                if save_res
                else "\nNo action was done."
            )
        elif user_action == "2":
            passkeep_get.query_data_all(conn)
        elif user_action == "3":
            result_count = passkeep_get.query_data(conn)
            print(
                f"found {result_count[0]} exact matching and {result_count[1]} estimated items."
            ) if result_count else print("Nothing found.")
        elif user_action == "4":
            passkeep_del.delete_entry(conn)
        elif user_action == user.username or user_action == "rmusr":
            print(
                "\nThis will delete the user's database, including all it's data. (WARNING: action cannot be undone!)\nDo you want to continue? [Y/n]"
            )
            user_response = input(">> ").casefold()
            if user_response == "y":
                os.remove(f"database/.files/{user.dbname}.db")
                print("User was deleted successfully.")
                return
            continue
        else:
            conn.close_connection()
            print("\nhave a good day... 😊")
            sys.exit(0)
