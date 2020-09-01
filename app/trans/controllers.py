from datetime import date
import pandas as pd
import numpy as np
from sqlalchemy.orm import *
from sqlalchemy import *
import os
from dotenv import load_dotenv
from app import create_app
from app.profile.controllers import decrypt, encrypt
from app.trans.models import trans




def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(["xls","csv", "xlsx"])
    # filename = lower(str(filename));
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# app = create_app()
dir = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=dir+'/.env')
PASS = str(os.getenv("PASS"))
engine = create_engine(f'sqlite:///{dir}/{os.getenv("dbname")}.sqlite3')
###############################################################################
#                                                                             #
# This function take a Dataframe as an argument and converts it to Database   #
#                                                                             #
###############################################################################
def convertDF2DB(df):
    df.rename(columns={'Transaction Date':'date',
                           'Category':'category_id',
                           'Account': 'account_id',
                           'Description':'description',
                           'Credit':'credit',
                           'Debit':'debit'},inplace=True)
    df['credit'] = df['credit'].apply(lambda x: encrypt(PASS,str(x)))
    df['debit'] = df['debit'].apply(lambda x: encrypt(PASS,str(x)))
    df['description'] = df['description'].apply(lambda x: encrypt(PASS,x))
    dic = df.to_dict(orient="record")
    Session = sessionmaker(bind=engine)
    s = Session()
    s.bulk_insert_mappings(trans,dic)
    s.commit()




###############################################################################
# This function is used after the user uploads the bank statement. It adds    #
# the selected category and account to the dataframe and returns the the      #
# updated df.                                                                 #
###############################################################################
def addSel2DF(form,df):
    # loop through the selected items and insert them to the dataframe
    new_dic={'Category': []}
    for item in form:
        if (int(item.ex_category.data) == 0) and (int(item.in_category.data) != 0):
            new_dic['Category'].append(int(item.in_category.data))
        elif (int(item.ex_category.data) != 0) and (int (item.in_category.data) == 0):
            new_dic['Category'].append(int(item.ex_category.data))
        else:
            new_dic['Category'].append(np.NaN)

    #update the dataframe columns
    df['Category'] = new_dic['Category']
    df.dropna(subset = ['Category'], inplace=True)
    return df




###############################################################################
#                       read_statement(filename,bank)
# This function munges the bankstatments of several banks in Oman. It accepts
# two parameters, the first is the file name and the second is the bank name
# 21/3/2020: - Bankmuscat Execel Bankstatment of an Account is acceptable
#            - National Bank of Oman Excel Bankstatement of an account is
#              acceptable
#            - Bankmuscat Credit Card Excel Bankstatement is acceptable
#           For Bank Muscat Account --> bank = 'muscat'
#           For Bank NBO Account --> bank = 'nbo'
#           For Bank Muscat Credit Card --> bank = 'mct_crdt'
###############################################################################
def read_statement(filename,bank,account=''):
    def credit (value):
        return max(value, 0)

    def debit (value):
        return min(value, 0)

    if account == '':
        account=bank

    if bank == 'mct_crdt':
        statement = pd.read_excel(filename, skiprows=6, header=1,thousands=',')
        statement = statement[['Transaction Date','Description of Transaction',
                    'Amount in Card Currency']]
        #separate credit from debit into two different columns
        statement['credit']= (
                    statement['Amount in Card Currency'].map(credit))
        statement['Debit']= (
                    statement['Amount in Card Currency'].map(debit)).abs()
        #choose only required columns
        statement = statement[['Transaction Date','Description of Transaction',
                    'Debit','credit']]
    else:
        if bank == 'nbo':
            nrows = 15;
            r_columns = ['Date Posted','Description','Debit','Credit']
        elif bank == 'muscat':
            nrows = 5
            r_columns = ['Transaction Date','Narration','Debit','Credit']
        else:
            nrows= None
# read excel file
        statement = pd.read_excel(filename, skiprows=nrows,
                                    header=1,thousands=',')
        statement = statement[r_columns]

# change header titles
    statement.columns = ['date', 'description', 'debit', 'credit']
# delete the columns that are not required
    statement.dropna(axis='columns', how='all',inplace=True)
#convert the first column Transaction Date to a datetime format
    statement['date'] = pd.to_datetime(statement['date']
              ,dayfirst=True)
    statement['date'] = (
                        statement['date'].dt.strftime('%Y/%m/%d'))
    statement['credit']=round(statement['credit'],3)
    statement['debit']=round(statement['debit'],3)
# replace remaining NaN with 0
    statement.fillna(0,inplace=True)

    return statement
