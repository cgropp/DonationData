import requests
import pandas as pd
from bs4 import BeautifulSoup

#Use BeautifulSoup to scrape web data
URL = "https://www.opensecrets.org/donor-lookup/results?cand=&cycle=2022&employ=&jurisdiction=&name=&occupation=&page=1&state=&type=&zip=90623"
site = requests.get(URL)
data = site.text
soup = BeautifulSoup(data, 'html.parser')



#List of tables
tables = soup.find_all('table')

#Extract table
table = soup.find('table', class_='u-mt2')

# Defining of the dataframe


header = []
rows = []

# Collecting Data
for i, row in enumerate(table.find_all('tr')):
    if i == 0:
        header = [el.text.strip() for el in row.find_all('th')]
    else:
        rows.append([el.text.strip() for el in row.find_all('td')])



df = pd.DataFrame(rows, columns=['Category', 'Contributor', 'Employer', 'Occupation', 'Date', 'Amount', 'Recipient', 'Recipient Jurisdiction'])


#Need to add zip, phone number, address
df_short = df[['Contributor', 'Occupation', 'Date', 'Amount', 'Recipient']]

#Filter to democrats
df_short = df_short[df_short['Recipient'].str.contains("\(D\)|Democrat", na=False)]

print(df_short)


