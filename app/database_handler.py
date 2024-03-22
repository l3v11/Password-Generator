import psycopg
from app import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS

class DatabaseHandler:
    """
    Initializes the DatabaseHandler class by setting up the connection string
    and creating necessary tables if they don't exist.
    """
    def __init__(self):
        self.conn_string = f"dbname={DB_NAME} host={DB_HOST} port={DB_PORT} \
                            user={DB_USER} password={DB_PASS}"
        self.__create_tables()
    
    def execute_query(self, query, params=None):
        """
        Executes a given SQL query with optional parameters
        and returns the result.
        """
        try:
            with psycopg.connect(self.conn_string) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    if cur.description:
                        return cur.fetchall()
                    else:
                        return None
        except (Exception, psycopg.Error) as e:
            print(f"Database error: {e}")
            exit(1)

    def __create_tables(self):
        """
        Creates necessary tables if they don't exist.
        """
        queries = [
            """
            CREATE TABLE IF NOT EXISTS secrets (
                master_password varchar(255) NOT NULL,
                fernet_key      varchar(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS creds (
                website_name varchar(255) PRIMARY KEY,
                username     varchar(255),
                password     varchar(255),
                website_uri  varchar(1024)
            )
            """
        ]
        for query in queries:
            self.execute_query(query)

    def drop_tables(self):
        """
        Drops existing tables if they exist and recreates them.
        """
        self.execute_query("DROP TABLE IF EXISTS secrets, creds")
        self.__create_tables()
    
    def store_secrets(self, master_password, fernet_key):
        """
        Stores a hashed master password and a fernet key
        in the 'secrets' table.
        """
        self.execute_query(
            """INSERT INTO secrets (master_password, fernet_key)
               VALUES (%s, %s)
               """,
               (master_password, fernet_key)
        )

    def get_master_pass(self):
        """
        Retrieves the hashed master password from the 'secrets' table.
        """
        res = self.execute_query("SELECT master_password FROM secrets")
        return res[0][0] if res else None
    
    def get_fernet_key(self):
        """
        Retrieves the fernet key from the 'secrets' table.
        """
        res = self.execute_query("SELECT fernet_key FROM secrets")
        return res[0][0] if res else None

    def update_master_pass(self, master_password):
        """
        Updates the hashed master password in the 'secrets' table.
        """
        self.execute_query("UPDATE secrets SET master_password = %s",
                           (master_password,)
        )

    def store_creds(self, website_name, username, password, website_uri):
        """
        Stores credentials in the 'creds' table.
        """
        self.execute_query(
            """
            INSERT INTO creds (website_name, username, password, website_uri)
            VALUES (%s, %s, %s, %s)
            """,
            (website_name, username, password, website_uri)
        )

    def find_creds(self, website_name):
        """
        Retrieves credentials for a given website name from the 'creds' table.
        """
        res = self.execute_query("SELECT * FROM creds WHERE website_name = %s",
                                 (website_name,)
        )
        return res[0] if res else None

    def list_sites(self):
        """
        Retrieves a list of website names stored in the 'creds' table.
        """
        res = self.execute_query("SELECT website_name FROM creds")
        return [row[0] for row in res] if res else None

    def drop_creds(self, website_name):
        """
        Deletes credentials for a given website name from the 'creds' table.
        """
        self.execute_query("DELETE FROM creds WHERE website_name = %s",
                           (website_name,)
        )
