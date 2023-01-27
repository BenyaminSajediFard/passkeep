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
def assemble_passwd():
    """Generates a strong, random password that consists of upper and lower case letters, numbers and symbols into the pass_entry"""

    password_list = []

    while not password_list:
        pass_level = input(
            "\nChoose a password difficulty level: (The stronger, the better)\n\n[I]ntuitive:  8chars, including alpha and num\n[S]ubtle:  8chars, including alpha, num and symbols\n[SE]cure:  12chars, including alpha, num and symbols\n[C]hallenge:  24chars, including alpha, num and symbols\n[E]xtreme:  48chars, including alpha, num and symbols\n>> "
        ).casefold()
        if pass_level == "i":
            password_list = gen_passwd([letters, numbers], [4, 4])
        elif pass_level == "s":
            password_list = gen_passwd([letters, numbers, symbols], [4, 2, 2])
        elif pass_level == "se":
            password_list = gen_passwd([letters, numbers, symbols], [6, 3, 3])
        elif pass_level == "c":
            password_list = gen_passwd([letters, numbers, symbols], [16, 4, 4])
        elif pass_level == "e":
            password_list = gen_passwd([letters, numbers, symbols], [20, 10, 10])
        else:
            print("\nwrong password level was chosen.\ngo again...")

    shuffle(password_list)
    return stringify(password_list)
