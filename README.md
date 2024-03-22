# Password Manager
A Python based Password Manager with PostgreSQL integration

## Features
- **Master Password:** Users can set up a master password when using the password manager for the first time. This master password grants access to the stored credentials.
- **Login Credentials Management:** Users can add, find and remove login credentials for various websites.
- **Data Reset:** Users can erase all data stored in the password manager, including login credentials and the master password, if needed.
- **Data Protection:** The master password undergoes secure hashing using the SHA3-256 algorithm, while login passwords are encrypted using Python's Fernet (symmetric encryption) module, ensuring the protection of sensitive information.
- **Database Integration:** Utilizes PostgreSQL database to provide reliable storage and retrieval of data.
- **User Interface:** Offers a user-friendly command-line interface (CLI) for seamless interaction with the password manager.

## Instructions
- Install [PostgreSQL](https://www.postgresql.org/download/) and configure it.
- Install the required Python packages.
  
  ```
  pip install --no-cache-dir -r requirements.txt
  ```
- Rename the file `config_sample.env` to `config.env` and open it in a text editor.
- Fill up the variables with the database configuration.
- Open a terminal and run the following command.
  
  ```
  python -m app
  ```
- Upon initial login, create a Master Password and don't try to forget it.
