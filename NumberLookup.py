import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

zipCode = "91321"
input = os.getcwd() +"\CSV_Output\\" + zipCode + ".csv" 

df = pd.read_csv(input)

df['Phone Number'] = ""
print(df)


examplePerson = df.loc[0].at["Contributor"]
print(examplePerson)

lastName = examplePerson.split(", ")[1]
firstName = examplePerson.split(", ")[0]

#firstName = "John"
#lastName = "Smith"

URL = "https://www.fastpeoplesearch.com/name/" + firstName + "-" + lastName + "_" + str(zipCode)

print(URL)

site = requests.Session()
site = requests.get(URL)
data = site.text
soup = BeautifulSoup(data, 'html.parser')
soupText = soup.get_text()

address = soupText.split("who live at")[0]
address = soupText.split(zipCode)[0]

print(address)