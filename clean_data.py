# Load and clean the data
import pandas as pd
import duckdb
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
def sql(query):
    return duckdb.sql(query).df()
energy=pd.read_csv('/Users/mumaizah/Downloads/owid-energy-data.csv')
countries=energy[energy['iso_code'].notna()]
data_2023=countries[countries['year']==2023]