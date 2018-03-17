import requests
import lib.obp
from settings import *
import pandas as pd

obp = lib.obp

obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION)

# Login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

our_bank = OUR_BANK

accounts = obp.getPrivateAccounts(our_bank)
account = accounts[0]['id']

transactions = obp.get_transactions()
transactions = transactions['json']['hits']['hits']

transactions_dataframe = pd.DataFrame(columns=['Date', 'Amount', 'Debit/Credit', 'Currency', 'Description'])

for transaction in transactions:
    transaction = transaction['_source']
    transactions_temp = pd.DataFrame({
        'Date': transaction['posted_date'],
        'Amount': transaction['amount'],
        'Debit/Credit': transaction['debit_credit'],
        'Currency': transaction['currency'],
        'Description': transaction['description']}, index=[0])
    transactions_dataframe = pd.concat([transactions_dataframe, transactions_temp], axis=0)

transactions_dataframe.reset_index()

print(transactions_dataframe)


