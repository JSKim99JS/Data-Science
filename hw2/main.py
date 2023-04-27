from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

""" STEP 0 """

url = "https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory"
req = requests.get(url)

print(req.status_code)

""" STEP 1 """

html_source = req.text

print(html_source)


""" STEP 2 """

soup = BeautifulSoup(req.content, 'html.parser')  # crolling entire page

table = soup.find('table', {
    "class": 'wikitable sortable sortunder tpl-blanktable plainrowheaders plainrowheadersbg sticky-col2'})
rows = table.find_all('tr')

print(rows)


"""2. Extracting data and filling it"""

output_dict = {}

for row in rows[2:]:  # world 제거
    columns = row.find_all('td')  # 각 줄에서 td tag 찾기
    names = row.find_all('th', {'scope': 'row'})  # 국가 이름 포함한 source찾기

    if len(columns) > 1: #th 개수 1 이상인거만 가져오기
        th = row.find('th')
        country_name = th.text.strip()  # th 태그에서 국가 text 만 추출

        d_m = columns[1].text.strip()
        deaths = columns[2].text.strip()
        cases = columns[3].text.strip()

        output_dict[country_name] = {
            'Deaths / million': d_m,
            'Deaths': deaths,
            'Cases': cases
        }

print(output_dict)

print('\n\n\n')

""" 3. Creating a dataframe(Python data structure) from a dictionary"""

df = pd.DataFrame(output_dict)
df = df.transpose() #행을 국가, 열을 수치로
print(df)

"""Step 1. Check each column's data type in the merged dataframe"""

print("\n\n\n")
print(df.dtypes)

"""Step 2. Find and Replace the non-numeric values with NaN.
Then re-check the data types of each column.
All of them should be float-based (float64) or int-based (int64)"""

df = df.replace('—', np.nan) #NaN 값으로 바꾸기

df['Deaths / million'] = df['Deaths / million'].str.replace(',', '').astype(float)
df['Deaths'] = df['Deaths'].str.replace(',', '').astype(float)
df['Cases'] = df['Cases'].str.replace(',', '').astype(int)
#각 항목 float, int형식으로 바꿔주기

print(df.dtypes) # rechecking data types
print('\n\n')

"""Step 3. Drop the rows that contain at least one "nan".
The shape of the updated dataframe should be (230, 3)"""

df = df.dropna() #Nan 값 row 제거
print(df.isna().sum().sum()) # 테이블에 있는 nan 개수 계산
print(df)

"""Step 4. Add a new column 'death_rates' and fill the column with appropriate values"""

df['death_rates'] = df['Deaths']/df['Cases']
print(df)
print('\n\n')

"""5-1. Print top 5 countries with the highest/lowest death rates by COVID-19. (total 10 countries)"""

#death_rates 기준 각 오름차순, 내림차순 정렬 후 5개씩 출력
highest = df.sort_values(by='death_rates', ascending=False).head(5)
lowest = df.sort_values(by='death_rates', ascending=True).head(5)

print(highest)
print(lowest.sort_values(by='death_rates', ascending=False))

"""5-2. Create a sub-dataframe for the five countries extracted in question 5-1(highest case)."""

print('\n\n')
subdf = df.sort_values(by='death_rates', ascending=False).head(5)
print(subdf)

"""5-3. Perform sanity checks on the values of the added column('death_rates').
Do you observe any anomalous value? Delete row(s) containing anomalous value."""

anomalous = subdf['death_rates']>1 # death rates가 1 이상일 수가 없으니까 그런 애들 찾기

print("\n\n")
invalid_rows = subdf[anomalous] #print out the index value of invalid rows
print(invalid_rows.index)
subdf = subdf[~anomalous] #이상한 값 빼고 다시 데이터프레임 저장
print('\n\n')
print(subdf)


"""5-4. Plot death rates from the dataframe 'subdf'"""

subdf.plot(y='death_rates', kind='bar')
plt.show()