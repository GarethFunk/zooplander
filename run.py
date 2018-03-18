from app import app
import Financial_Data_Proc as fin
import json
the_global_variable = {}
with open('globals.txt', 'w') as outfile:
    annual_deposit, annual_income, rent = fin.Analyse_Account()
    #annual_deposit, annual_income, rent = (5000, 30000, 1000)
    json.dump({'annual_deposit': annual_deposit,
               'annual_income': annual_income, 'rent': rent}, outfile)

app.run(host='127.0.0.1', port=8080, debug=True)
