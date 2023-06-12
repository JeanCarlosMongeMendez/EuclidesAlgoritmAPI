
import pyodbc
import pandas as pd

cnxn_str = ("Driver={SQL Server};"
            "Server=(local)\SQLEXPRESS;"
            "Database=Euclid;"
            "Trusted_Connection=yes;")

cnxn_str2 = ("Driver={SQL Server};"
            "Server=;"
            "Database=;"
            "UID=;"
            "PWD=;")

encryptionKey = "TESTEXP"

class Connection:

    def __init__(self):
        print("init")

    def add_user(self, username, inteligence, password):
        cnxn = pyodbc.connect(cnxn_str)
        cursor = cnxn.cursor()
        query = "INSERT INTO users (username, inteligence, pass) " \
                f"VALUES ('{username}', '{inteligence}', EncryptByPassPhrase('{encryptionKey}', '{password}'))"
        print(query)
        try:
            cursor.execute(query)
            cnxn.commit()
        except TypeError as e:
            print(e)
            return None, 400

        del cnxn

    def get_users(self):
        cnxn = pyodbc.connect(cnxn_str)
        query = ("SELECT id, username, inteligence, "
                 f"pass = Convert(varchar(32), DecryptByPassPhrase('{encryptionKey}', pass)) "
                 "FROM dbo.users")
        data = pd.read_sql(query, cnxn)
        del cnxn
        return data
