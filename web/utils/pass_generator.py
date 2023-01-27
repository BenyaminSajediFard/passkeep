from random import choices, shuffle
from utils.pass_data import letters, numbers, symbols

# ------------------------ PASSWORD GENERATOR --------------------------- #
def gen_passwd(passed_data, weight_args):
    """Generates a password based on the given entries.
    Args:
        passed_data: data to generate the password construct. not considering the number or width of it.
        weight_args: usually two or three number of passed_data to calculate the random weight of generated password.
    """
    password_list = []
    for index, data in enumerate(passed_data):
        password_list += [*choices(data, k=weight_args[index])]
    return password_list


def stringify(pass_list):
    """Turns any builtin iterable to a string"""
    password = ""
    for i in pass_list:
        password += str(i)
    return password


# ------------------------ PASSWORD MANAGER --------------------------- #
def assemble_passwd(pass_level):
    """Generates a strong, random password that consists of upper and lower case letters, numbers and symbols into the pass_entry"""

    password_list = []

    if pass_level == "level-1":
        password_list = gen_passwd([letters, numbers], [4, 4])
    elif pass_level == "level-2":
        password_list = gen_passwd([letters, numbers, symbols], [4, 2, 2])
    elif pass_level == "level-3":
        password_list = gen_passwd([letters, numbers, symbols], [6, 3, 3])
    elif pass_level == "level-4":
        password_list = gen_passwd([letters, numbers, symbols], [16, 4, 4])
    elif pass_level == "level-5":
        password_list = gen_passwd([letters, numbers, symbols], [20, 10, 10])

    shuffle(password_list)
    return stringify(password_list)
