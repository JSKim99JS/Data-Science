import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/2019%E2%80%9320_coronavirus_pandemic_by_country_and_territory'
html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser')

table = soup.find_all('table')[0]
rows = table.find_all('tr')

data = {}
for row in rows[2:]:
    cols = row.find_all('td')
    if len(cols) > 4:
        country = cols[1].text.strip()
        cases = cols[2].text.strip()
        deaths = cols[4].text.strip()
        rate = cols[5].text.strip()
        data[country] = {'cases': cases, 'deaths': deaths, 'rate': rate}

print(data)