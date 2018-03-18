import pandas as pd

def get_mortgages(file):
    mortgages = pd.read_csv(file, sep = '\t')
    return mortgages

if __name__ == '__main__':
    mortgages = get_mortgages('mortgages.csv')
    print(mortgages)
