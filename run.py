import Financial_Data_Proc as fin
the_global_variable = {}
annual_deposit, annual_income, rent = fin.Analyse_Account()

from app import app

app.run(host='127.0.0.1', port=8080, debug=True)

