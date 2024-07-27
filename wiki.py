from bs4 import BeautifulSoup
import requests

url="https://en.wikipedia.org/wiki/Python_(programming_language)"
response=requests.get(url)
soup = BeautifulSoup(response.content,"html.parser")

datatype_table=soup.find(class_="wikitable")
body=datatype_table.find('tbody')
rows=body.find_all('tr')[1:]

mutable_types=[]
immutable_types=[]

for row in rows:
    data=row.find_all('td')
    if data[1].get_text()=='mutable\n':
        mutable_types.append(data[0].get_text().strip())
    else:
        immutable_types.append(data[0].get_text().strip())
print(f"Mutable tyeps:{mutable_types}")
print(f"IMMutable tyeps:{immutable_types}")