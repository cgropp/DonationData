import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

while(True):
    #Use BeautifulSoup to scrape web data
    zipCode = input("Please enter a zipcode:\n")
    URL = "https://www.opensecrets.org/donor-lookup/results?cand=&cycle=2022&employ=&jurisdiction=&name=&occupation=&page=1&state=&type=&zip=" + str(zipCode)
    site = requests.get(URL)
    data = site.text
    soup = BeautifulSoup(data, 'html.parser')
    page = 1

    #Check for more pages
    nextFound = (soup.find('div', class_='paginate_button next') != None)

    #List of tables
    tables = soup.find_all('table')

    #Extract table
    table = soup.find('table', class_='u-mt2')
    if table == None:
        print("No results found for this zip code\n")
        continue
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



    while(nextFound):
        page += 1
        URL = "https://www.opensecrets.org/donor-lookup/results?cand=&cycle=2022&employ=&jurisdiction=&name=&occupation=&page=" + str(page) + "&state=&type=&zip="+ str(zipCode)
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
        if (page >= 10):
            nextFound = False


    #Fix contributor names
    df["Location"] = df['Contributor'].str.split('\t\t\t\t\t\t\t\t\t\t').str[1]
    df['Contributor'] = df['Contributor'].str.split('\\n').str[0]

    #Isolate relevant columns
    df_short = df[['Contributor', 'Location', 'Occupation', 'Date', 'Amount', 'Recipient']]

    #Filter to democrats
    df_short = df_short[df_short['Recipient'].str.contains("\(D\)|Democrat", na=False)]
    df_short["ZipCode"] = zipCode


    print(df_short)
    currDir = os.getcwd()
    outputFile = currDir+"\\CSV_Output\\" + zipCode + ".csv" 
    print("File successfully saved to " + outputFile)
    df_short.to_csv(outputFile,index=False)