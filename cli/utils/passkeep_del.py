def delete_entry(connection):
    all_data = connection.select_data()
    if not all_data:
        print("\nNo data was found in your database.\nexiting deletion mode...")
        return
    source = input(
        "\nEnter the source or parts of it that you remember\n(leave empty to retrieve all sources)\n>> "
    ).casefold()
    print()
    if not source:
        print("\nall current entries:")
        for index, item in enumerate(all_data):
            print(f"  {index+1}: {item[1]}")
        sources = all_data
    else:
        sources = list(filter(lambda x: source in x[1], all_data))

    if (list_length := len(sources)) > 1:
        if len(all_data) == list_length:
            print(
                "\nAll items in database are selected.\n#Warning: choosing `all` will result in permanent data lose."
            )
        else:
            print("\nmatching items:")
            for index, item in enumerate(sources):
                print(f"  [{index+1}]=> {item[1]}: {item[2]}")
            print("were found.\n")
    elif len(sources) == 1:
        print(f"matching item:\n  [1]=> {sources[0][1]}: {sources[0][2]}\nwas found.\n")
    print("\nDelete options: 0) cancel | 1,3,4) multi | all")
    user_input = input(">> ")
    if user_input == "0":
        print("\nOperation was canceled by user.\nexiting deletion mode...")
        return
    elif user_input == "all":
        print(
            "\nWill delete every entry currently in database. do you confirm this action? [Y/n]"
        )
        delete_confirm = input(">> ")
        if delete_confirm == "y":
            connection.delete_data()
            print("\nDatabase has been wiped out. deletion was successfully completed.")
            return
        print("\nOperation was cancelled.")
        return
    elif len(user_input) == 1:
        selected_item = sources[int(user_input) - 1]
        connection.delete_data("source", selected_item[1])
        print("\nselected item was deleted successfully.")
    elif len(user_input) > 1:
        print(
            f"\nWill delete entries {user_input} from database.\nDo you confirm multiple deletion? [Y/n]"
        )
        delete_confirm = input(">> ").casefold()
        if delete_confirm == "y":
            deletion_list = user_input.split(",")
            for item in deletion_list:
                index = int(item) - 1
                connection.delete_data("source", sources[index][1])
            print("\nselected items was deleted successfully.")
            return
    else:
        print("\nWrong input.")
        return
