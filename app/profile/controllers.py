from datetime import date
import pandas as pd
import numpy as np
import psycopg2
import os
from dotenv import load_dotenv
from Crypto.Cipher import XOR
import base64

from config import dbtype




dir = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=dir+'/.env')
###############################################################################
#                       encrypt and decrypt(key,plaintext)
# these functions are used to encrypt  data before writing them to the database
# and decrypt the imported datafrom the db
#
###############################################################################
def encrypt(key, plaintext):
    cipher = XOR.new(key)
    return base64.b64encode(cipher.encrypt(plaintext))

def decrypt(key, ciphertext):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.b64decode(ciphertext))




###############################################################################
# This function is used to convert a database transactions to dataframe.      #
# Args (user_id)                                                             #
###############################################################################
def convertDB2DF(userid):
    ''' This function is used to convert a database transactions
        to dataframe. Args (database)'''

    PGDATABASE=str(os.getenv("dbname"))
    PASS = str(os.getenv("PASS"))

    if dbtype == "sqlite":
        import sqlite3
        conn=sqlite3.connect(f'{dir}/{PGDATABASE}.sqlite3')
    elif dbtype == "psql":
        PGHOST='localhost'
        PGUSER=str(os.getenv("dbuser_app"))
        PGPASSWORD=str(os.getenv("dbpass_app"))
        conn_string = "host="+ PGHOST +" port="+ "5432" +" dbname="\
                + PGDATABASE +" user=" + PGUSER +" password="+ PGPASSWORD
        conn=psycopg2.connect(conn_string)

    df = pd.read_sql(f'select date, description, debit, credit, \
                    categories.category, accounts.account \
                    from trans \
                    inner join accounts on accounts.id=trans.account_id\
                    inner join categories on categories.id=trans.category_id\
                    where user_id={userid};',
                    conn)
    df.columns=['Date', 'Description', 'Debit', 'Credit','Category','Account']
    df['Credit'] = df['Credit'].apply(
            lambda x: decrypt(PASS,x).decode('utf-8')).astype(float)
    df['Debit'] = df['Debit'].apply(
            lambda x: decrypt(PASS,x).decode('utf-8')).astype(float)
    df['Description'] = df['Description'].apply(
            lambda x: decrypt(PASS,x).decode('utf-8'))
    df.sort_values(by=['Date'],inplace=True)
    return df
