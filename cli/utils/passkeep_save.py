from utils.pass_generator import assemble_passwd


def save_action(connection):
    source = ""
    password = ""

    while not source:
        source = input(
            "\nEnter a source for your password (e.g reddit.com/sign-in or reddit)\n>> "
        )
        password = assemble_passwd()

    while True:
        usr_approval = input(
            f"\nSource ==> {source.casefold()}\nNew password ==> {str(password)}\nApproved? [Y/n]\n>> "
        ).casefold()
        if usr_approval == "y":
            repeated_entry = connection.select_data("source", source)
            if repeated_entry:
                print(
                    "\nAlready saved a source with the same name.\ntry with another name"
                )
                return None
            print("\nInfo approved.\nsubmitting the data...")
            return connection.insert_data(source, password)
        usr_actions = int(
            input(
                "\nChoose an action:\n[1] edit source\n[2] edit password\n[3] go to pass-generation\n[4] continue\n[5] exit\n>> "
            )
        )
        if usr_actions == 1:
            source = input(
                f"\nSource is currently set to: {source}\nEnter new source >> "
            )
            continue
        elif usr_actions == 2:
            password = input(
                f"\nPassword is currently set to: {password}\nEnter new Password >> "
            )
            continue
        elif usr_actions == 3:
            password = assemble_passwd()
            continue
        elif usr_actions == 4:
            print("\nInfo approved.\nsubmitting the data...")
            return connection.insert_data(source, password)
        elif usr_actions == 5:
            print("\nExiting save mode...")
            return False
