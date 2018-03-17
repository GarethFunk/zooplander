import requests
import obp
from settings import *
import pandas as pd
from datetime import datetime


obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION)

# Login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

#our_bank = OUR_BANK

#accounts = obp.getPrivateAccounts(our_bank)
#account = accounts[0]['id']


def get_transactions():

    transactions = obp._get_transactions()
    transactions = transactions['json']['hits']['hits']

    transactions_dataframe = pd.DataFrame(columns=['Date', 'Amount', 'Currency', 'Description'])

    for transaction in transactions:
        transaction = transaction['_source']
        if transaction['debit_credit'] == 'Credit':
            transaction['amount'] = 0 - float(transaction['amount'])
        transaction['posted_date'] = datetime.strptime(transaction['posted_date'], '%Y-%m-%d')
        transactions_temp = pd.DataFrame({
            'Date': transaction['posted_date'],
            'Amount': transaction['amount'],
            'Currency': transaction['currency'],
            'Description': transaction['description']}, index=[0])
        transactions_dataframe = pd.concat([transactions_dataframe, transactions_temp], axis=0)

    return transactions_dataframe

if __name__ == '__main__':
    print_transactions = get_transactions()
    print(print_transactions)


