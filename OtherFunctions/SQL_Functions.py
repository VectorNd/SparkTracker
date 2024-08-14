# used to check if a given file exists or not
import os.path

# used to create, modify and store database files using sql
import sqlite3 as sql

# miscellaneous functions that are repeated but simple
from OtherFunctions.MiscFunctions import *


class Database:
    def __init__(self):
        # If the file does not exist then create one and ask user for email and check frequency
        if not self.file_exists():
            self.connect()
            self.create_tables()
            # self.get_user_data()
            # self.get_product_params()

        else:
            self.connect()

    '''
        These functions will get data from user and store it in the database
    '''

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.con.close()

    # Checks if a given file exists
    @staticmethod
    def file_exists():
        if os.path.isfile('OtherFunctions/Database.db'):
            return True
        else:
            return False

    # Attempts connection to the database file
    def connect(self):
        try:
            self.con = sql.connect('OtherFunctions/Database.db')
        except sql.Error:
            print(sql.Error)
            exit()

        # Create a cursor using the connection to the database
        self.c = self.con.cursor()

    # Create tables url and user for first time initialization
    def create_tables(self):
        # Create USER table with user_id as the primary key
        self.c.execute('''
            CREATE TABLE USER(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                number TEXT,
                checkFrequency TEXT
            )
        ''')

        # Create URL table with product_id as the primary key and user_id as a foreign key
        self.c.execute('''
            CREATE TABLE URL(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                url TEXT,
                maxPrice REAL,
                FOREIGN KEY(user_id) REFERENCES USER(user_id)
            )
        ''')

    # Gets the user data and stores it in the USER table, returning the user_id
    def get_user_data(self, username, email, number, check_freq):
        self.c.execute('INSERT INTO USER (username, email, number, checkFrequency) VALUES (?, ?, ?, ?)', 
                       (username, email, number, check_freq))
        self.con.commit()

        # Get the last inserted user_id
        return self.c.execute('SELECT last_insert_rowid()').fetchone()[0]
    

    def all_users(self):
    # Fetch all users from the USER table
        users = self.c.execute("SELECT * FROM USER").fetchall()

        # Print each user record
        for user in users:
            print(user)


    def get_product_params(self,user_id,url,max_price):
        # while True:
        # url = input('Copy the url from the product page and paste it below\n')
        # max_price = input('Enter the max price of the product\n')

        product_id = len(self.c.execute("SELECT product_id FROM URL").fetchall()) + 1
        if self.c.execute("SELECT product_id FROM URL").fetchone() == "1":
            product_id -= 1

        # Insert the received values into the sql database
        self.c.execute('INSERT INTO URL (user_id, url, maxPrice) VALUES (?, ?, ?)', 
                       (user_id, url, max_price))

        # commits the changes made to the database
        self.con.commit()

        # print('\n\nDo you want to enter another product link? y/n\n')

        # If the user doesn't enter y then the url access function is terminated.
        # if input() != 'y':
        #     break

    '''
        From here the functions will access the database to return values
    '''
    def get_user_products(self, user_id):
        return self.c.execute('SELECT * FROM URL WHERE user_id = ?', (user_id,)).fetchall()
    
    def single_user_data(self,username):
        return self.c.execute('SELECT * FROM URL WHERE username = ?', (username,)).fetchall()
    
    def access_user_data(self):
        return self.c.execute("SELECT * FROM USER").fetchall()

    def access_product_params(self):
        return self.c.execute("SELECT * FROM URL").fetchall()

    def remove_product(self, product_id):
        self.c.execute("DELETE FROM URL WHERE product_id = " + str(product_id))
        print("The product has been removed")
        self.rearrange_accounts(int(product_id))

    def rearrange_accounts(self, deleted_product_id):
        for i in range(deleted_product_id, len(self.c.execute("SELECT product_id FROM URL").fetchall()) + 2):
            self.c.execute("UPDATE URL SET product_id = ? WHERE product_id = ?", (i - 1, i))
        self.con.commit()
