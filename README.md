# Passkeep - A simple password management

Passkeep is a simple password management application available with interfaces such as a web-UI and CLI. It includes simple CRUD operations for your data and a password checker using pwnedpasswords.com API.
Passkeep is written in python3 utilizing flask, sqlite3 and pycipher3 for data management and encryption.

## Run

1. inspect the code if needed to check the security of your system.
2. when ready open a terminal in the current directory and use `chmod` command to give the `launch` script executable permissions which is necessary to run in most UNIX systems.
   eg. chmod +x ./launch
3. run the program using the `launch` script from the terminal.
4. you are good to go, from here you can select the interface which you want to use passkeep...
   (alternatively run the `launch` with extra arguments. 'cli' for command line UI || 'web' for web UI)
5. Another way is to run the script for each of the interfaces in their respective directories to run the program.

### NOTE: Passkeep is currently designed to run on UNIX and UNIX-like systems

- Enjoy! \*
