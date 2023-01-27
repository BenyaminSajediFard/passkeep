def query_data_all(connection):
    print()
    user_data = connection.select_data()
    if not user_data:
        print("No data currently stored in database.")
    else:
        for info in user_data:
            item_id, item_source, item_password = info
            print(f"{item_id} => {item_source}: {item_password}")


def query_data(connection):
    source = input(
        "\nEnter the source or parts of it that you remember:\n>> "
    ).casefold()
    exact_count = 0
    possible_count = 0
    print()
    query_result = connection.select_data("source", source)
    if query_result:
        exact_count = 1 if query_data else 0

    # in case of not finding exact search term
    all_data = connection.select_data()
    if not all_data:
        print("No data was found in your database.")
        return

    found_data = list(filter(lambda x: source in x[1], all_data))
    possible_count = len(found_data)
    if exact_count:
        possible_count -= 1
    print("\nmatching items:")
    for index, item in enumerate(found_data):
        print(f"  {index+1}: {item[1]} ")
    print("were found.\n")
    return exact_count, possible_count
