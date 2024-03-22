import hashlib
import os
import random
import string
from cryptography.fernet import Fernet
from getpass import getpass
from app.database_handler import DatabaseHandler

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

class PasswordManager:
    """
    Initializes the PasswordManager class
    with a DatabaseHandler instance.
    """
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def process_login(self):
        """
        Handles the login process for the password manager.
        """
        print('-' * 30)
        print("\tPassword Manager Login".expandtabs(4))
        print('-' * 30)

        get_mpass = self.db_handler.get_master_pass()
        if get_mpass is not None:
            mpass = getpass("Master Password: ")
            while not mpass:
                clear_screen()
                print('-' * 30)
                print("\tPassword Manager Login".expandtabs(4))
                print('-' * 30)
                mpass = getpass("Master Password: ")
            
            # Hashes the master password using SHA3-256 algorithm.
            hashed_mpass = hashlib.sha3_256(mpass.encode()).hexdigest()
            if hashed_mpass == get_mpass:
                print("\n> Logged in!\n")
                self.process_menu()
            else:
                print("\n> Incorrect Master Password!\n")
                exit(1)
        else:
            mpass = getpass("Create Master Password: ")
            while not mpass:
                clear_screen()
                print('-' * 30)
                print("\tPassword Manager Login".expandtabs(4))
                print('-' * 30)
                mpass = getpass("Create Master Password: ")
            
            re_mpass = getpass("Retype Master Password: ")
            if mpass == re_mpass:
                # Hashes the master password using SHA3-256 algorithm.
                hashed_mpass = hashlib.sha3_256(mpass.encode()).hexdigest()
                # Generate a Fernet key and decode it to a string
                fernet_key = Fernet.generate_key().decode()
                print('')
                self.db_handler.store_secrets(hashed_mpass, fernet_key)
                print("> Master Password created!\n")
                self.process_menu()
            else:
                print("\n> Passwords did not match!\n")
                exit(1)

    def process_menu(self):
        """
        Displays the main menu and handles user choices.
        """
        while True:
            print('-' * 30)
            print("\tPassword Manager Menu".expandtabs(4))
            print('-' * 30)
            print("\t1. Add Login".expandtabs(3))
            print("\t2. Find Login".expandtabs(3))
            print("\t3. List Websites".expandtabs(3))
            print("\t4. Remove Login".expandtabs(3))
            print("\t5. Generate Password".expandtabs(3))
            print("\t6. Change Master Password".expandtabs(3))
            print("\t7. Erase All Data".expandtabs(3))
            print("\tQ. Log Out".expandtabs(3))
            print('-' * 30)

            choice = input(": ").strip().lower()
            clear_screen()

            if choice == '1':
                self.add_login()
                print('')
            elif choice == '2':
                self.find_login()
                print('')
            elif choice == '3':
                self.list_sites()
                print('')
            elif choice == '4':
                self.remove_login()
                print('')
            elif choice == '5':
                self.generate_password()
                print('')
            elif choice == '6':
                self.change_master_pass()
                print('')
            elif choice == '7':
                self.erase_data()
                print('')
                exit()
            elif choice == 'q':
                exit()
            else:
                pass

    def add_login(self):
        """
        Allows the user to add login credentials
        for a website.
        """
        print('-' * 30)
        print("\tAdd Login".expandtabs(10))
        print('-' * 30)

        website_name = input("Website Name: ").strip().replace(' ', '_')
        while not website_name:
            clear_screen()
            print('-' * 30)
            print("\tAdd Login".expandtabs(10))
            print('-' * 30)
            website_name = input("Website Name: ").strip().replace(' ', '_')

        username = input("Username: ").strip()
        password = input("Password: ").strip()
        fernet_key = self.db_handler.get_fernet_key()
        # Encrypt the password using the Fernet key
        password_enc = Fernet(fernet_key.encode()).encrypt(password.encode()).decode()
        website_url = input("Website URI: ").strip()
        print('')
        self.db_handler.store_creds(website_name, username, password_enc, website_url)
        print("> Login info added!")

    def find_login(self):
        """
        Allows the user to find login credentials
        for a specific website.
        """
        print('-' * 30)
        print("\tFind Login".expandtabs(10))
        print('-' * 30)

        website_name = input("Website Name: ").strip().replace(' ', '_')
        res = self.db_handler.find_creds(website_name)
        if res is not None:
            print(f"Username: {res[1]}")
            fernet_key = self.db_handler.get_fernet_key()
            # Decrypt the encrypted password retrieved from the database
            password_dec = Fernet(fernet_key.encode()).decrypt(res[2].encode()).decode()
            print(f"Password: {password_dec}")
            print(f"Website URI: {res[3]}")
        else:
            print("\n> No login found!")

    def list_sites(self):
        """
        Lists all the websites for which
        login credentials are stored.
        """
        print('-' * 30)
        print("\tWebsites List".expandtabs(8))
        print('-' * 30)

        res = self.db_handler.list_sites()
        if res is not None:
            for id, row in enumerate(res, start=1):
                print(f"{id}. {row}")
        else:
            print("\n> No website listed!")

    def remove_login(self):
        """
        Allows the user to remove login credentials
        for a specific website.
        """
        print('-' * 30)
        print("\tRemove Login".expandtabs(9))
        print('-' * 30)

        website_name = input("Website Name: ").strip().replace(' ', '_')
        res = self.db_handler.find_creds(website_name)
        if res is not None:
            self.db_handler.drop_creds(website_name)
            print("\n> Login info removed!")
        else:
            print("\n> No login found!")

    def generate_password(self):
        """
        Generates a random password for the user.
        """
        print('-' * 30)
        print("\tGenerate Password".expandtabs(6))
        print('-' * 30)

        pass_length = input("Password Length: ")
        try:
            pass_length = int(pass_length) if pass_length else 8
            if pass_length < 8:
                pass_length = 8
        except ValueError:
            print("\n> Invalid password length!")
            return

        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*"
        character_set = lowercase_letters + uppercase_letters + digits + symbols

        password = [
            random.choice(lowercase_letters),
            random.choice(uppercase_letters),
            random.choice(digits),
            random.choice(symbols)
        ]

        password.extend(random.choice(character_set) for _ in range(pass_length - 4))
        random.shuffle(password)
        print("\n> Password:", ''.join(password))

    def change_master_pass(self):
        """
        Allows the user to change the master password.
        """
        print('-' * 30)
        print("\tChange Master Password".expandtabs(4))
        print('-' * 30)

        old_mpass = getpass("Current Master Password: ")
        while not old_mpass:
            clear_screen()
            print('-' * 30)
            print("\tChange Master Password".expandtabs(4))
            print('-' * 30)
            old_mpass = getpass("Current Master Password: ")
        
        # Hashes the old master password using SHA3-256 algorithm.
        hashed_old_mpass = hashlib.sha3_256(old_mpass.encode()).hexdigest()
        get_old_mpass = self.db_handler.get_master_pass()

        if get_old_mpass is not None and hashed_old_mpass == get_old_mpass:
            new_mpass = getpass("New Master Password: ")
            while not new_mpass:
                clear_screen()
                print('-' * 30)
                print("\tChange Master Password".expandtabs(4))
                print('-' * 30)
                print("Current Master Password: ")
                new_mpass = getpass("New Master Password: ")
        else:
            print("\n> Incorrect old Master Password!")
            return
        
        re_mpass = getpass("Retype New Master Password: ")
        if new_mpass == re_mpass:
            # Hashes the new master password using SHA3-256 algorithm.
            hashed_new_mpass = hashlib.sha3_256(new_mpass.encode()).hexdigest()
            print('')
            self.db_handler.update_master_pass(hashed_new_mpass)
            print("> Master Password updated!")
        else:
            print("\n> Passwords did not match!")

    def erase_data(self):
        """
        Allows the user to erase all data
        stored in the password manager.
        """
        print('-' * 30)
        print("\tErase All Data".expandtabs(8))
        print('-' * 30)

        mpass = getpass("Master Password: ")
        while not mpass:
            clear_screen()
            print('-' * 30)
            print("\tErase All Data".expandtabs(8))
            print('-' * 30)
            mpass = getpass("Master Password: ")
        
        hashed_mpass = hashlib.sha3_256(mpass.encode()).hexdigest()
        get_mpass = self.db_handler.get_master_pass()
        if get_mpass is not None and hashed_mpass == get_mpass:
            print('')
            self.db_handler.drop_tables()
            print("> All data has been erased!")
        else:
            print("\n> Incorrect Master Password!")

def main():
    clear_screen()
    password_manager = PasswordManager()
    password_manager.process_login()

if __name__ == '__main__':
    main()
