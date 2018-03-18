import pandas as pd
import math
import numpy as np
from zoopla_getter import pred_10y_prices
global annual_deposit
global annual_income
global rent

def roundup(x):
    return int(math.ceil(x / 5.0)) * 5

def get_mortgages(file):
    mortgages = pd.read_csv(file, sep = '\t')
    return mortgages


def get_right_year_nums(pred_10y_output, correct_year):
    idx = pred_10y_output[0].index(correct_year) #year list
    return pred_10y_output[1][idx], pred_10y_output[2][idx] # deposit and
    # house price in that year


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


def time_to_afford(time_projected):
    #which year will annual_deposit be more than 10%, house_price
    year = []
    for i in range(len(time_projected[1])):
        if time_projected[1][i]/time_projected[2][i] >= 0.1:
            year.append(time_projected[0][i])
    if not year:
        return None
    else:
        return year[0]

def string_summary(ranked_loans):
    return print(ranked_loans['Mortgages available'] + ', ' + ranked_loans['Maximum loan to value'] +
                 " Loan to Value," + " Average APR for a 25 Year Term: " + ranked_loans['The overall cost for comparison is (APR)'] +
                ", Monthly Repayment " + ranked_loans['Monthly cost'] +
                 ". Additional Benefits include " + ranked_loans['Additional benefits'] + ".")


if __name__ == '__main__':
    mortgages = get_mortgages('mortgages_20%_200000.csv')
    ranked = return_ranked_loans(250000, 25000, 1000, mortgages)
    prediction = pred_10y_prices('W12', 10000, 250000) #postcode, annual_saving, house_price now
    #prediction = ([2016,2017], [10000.0, 11000.0], [20000.0, 21000.0])

    rent = 1000

    year_to_afford = time_to_afford(prediction)
    if year_to_afford is not None:
        print(year_to_afford)
        deposit, house_price = get_right_year_nums(prediction, time_to_afford(prediction))
        ranked = return_ranked_loans(house_price, deposit, rent, mortgages)
        print(ranked.iloc[0])
        string_summary(ranked.iloc[0])
        print(string_summary)

    else:
        print("")


