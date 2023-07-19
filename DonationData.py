import requests
import pandas as pd
from bs4 import BeautifulSoup

#Use BeautifulSoup to scrape web data
URL = "https://www.opensecrets.org/donor-lookup/results?cand=&cycle=2022&employ=&jurisdiction=&name=&occupation=&page=1&state=&type=&zip=90623"
site = requests.get(URL)
data = site.text
soup = BeautifulSoup(data, 'html.parser')
page = 1


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

#print(df_short)

#Check for more pages
nextFound = (soup.find('div', class_='paginate_button next') != None)

#print(nextFound)

while(nextFound):
    page += 1
    URL = "https://www.opensecrets.org/donor-lookup/results?cand=&cycle=2022&employ=&jurisdiction=&name=&occupation=&page=" + str(page) + "&state=&type=&zip=90623"
    site = requests.get(URL)
    data = site.text
    soup = BeautifulSoup(data, 'html.parser')
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

    for row in rows:
        if(len(row) > 1):
            df.loc[len(df)] = row

    nextFound = (soup.find('div', class_='paginate_button next') != None)


#Fix contributor names
df['Contributor'] = df['Contributor'].str.split('\\n').str[0]

#Need to add zip, phone number, address
df_short = df[['Contributor', 'Occupation', 'Date', 'Amount', 'Recipient']]

#Filter to democrats
df_short = df_short[df_short['Recipient'].str.contains("\(D\)|Democrat", na=False)]

print(df_short)
df_short.to_csv("E:\\My Documents\..CS Projects\DonationData\\testCSV.csv",index=False)