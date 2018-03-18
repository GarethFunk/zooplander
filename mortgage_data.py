import pandas as pd
import math
global annual_deposit
global annual_income
global rent

def roundup(x):
    return int(math.ceil(x / 5.0)) * 5

def get_mortgages(file):
    mortgages = pd.read_csv(file, sep = '\t')
    return mortgages

#house value from Abs
def return_ranked_loans(house_value, deposit, rent, mortgages):
    #borrowed = house_value - deposit
    #print((house_value-deposit)*100/house_value)
    percentage = str(roundup((house_value-deposit)*100/house_value)) + '%'
    print(percentage)
    returned_mortgages = mortgages.loc[mortgages['Maximum loan to value'] >= percentage]
    # Monthly payments musn't be more than the rent
    returned_mortgages = returned_mortgages.loc[returned_mortgages['Monthly cost'] >= ('£' + str(rent))]
    # In order of suitability
    returned_mortgages.sort_values(by='The overall cost for comparison is (APR)', ascending=True, inplace=True)

    return returned_mortgages

def time_to_afford(time_projectedDeposit_house_price):



if __name__ == '__main__':
    mortgages = get_mortgages('mortgages_20%_200000.csv')
    ranked = return_ranked_loans(250000, 25000, 1000, mortgages)
    print(ranked)

