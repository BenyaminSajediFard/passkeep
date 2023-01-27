from werkzeug.security import check_password_hash, generate_password_hash

import passkeep_moderator as passkeep_moderator
from resources.users import create_users_table
from models.users import UserModel


def passkeep_manager():
    print(
        "\nI'm here to help you manage your passwords and easily interact with them.\nDuring the interactive shell read the options and provided, then choose the suitable one...\nEnjoy! 🤗"
    )
    username = input("\nEnter your username:\n>> ").casefold()
    create_users_table()
    if user := UserModel.find_by_username(username):
        print("\nUser was found. continuing...")
        passwd = input("\nenter your password:\n>> ")
        if check_password_hash(user.password, passwd):
            print("\nSigned in successfully.\ncontinuing...")
            passkeep_moderator.actions(user)
        print("\nFailed to sign in. Password did not match.")
        return
    user_creation = input(
        "\nUser was not found in database.\nCreate it now? [Y/n]\n>> "
    ).casefold()
    if user_creation == "y":
        passwd = input(
            "\nenter a safe password for your account:\n(password cannot be retrieved in case you forget it 😬)\n>> "
        )
        password = generate_password_hash(passwd)
        user = UserModel(username.casefold(), password)
        user.create_user()
        print("\nUser created successfully.\nContinuing...")
        passkeep_moderator.actions(user)
    print("\nUser creation aborted.\nquitting...")
    return


if __name__ == "__main__":
    passkeep_manager()
