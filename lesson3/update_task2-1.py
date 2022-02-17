from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint
import pandas as pd


myvacancy = input('Введите название нужной вакансии: ').strip()
maxpages = input('Сколько страниц читать (0 = все страницы): ')
if len(myvacancy) == 0:
    exit(0)

try:
    maxpages = int(maxpages)
except:
    maxpages = 1

vacancies_hh = []
vacancies_superjob = []

if True:
    page = 1
    hh_link = 'https://hh.ru'
    params = {'area': '1',
              'fromSearchLine': 'true',
              'st': 'searchVacancy',
              'text': myvacancy,
              'from': 'suggest_post'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}


    paramsstr = f"?area=1&fromSearchLine=true&st=searchVacancy&text={myvacancy}"

    next_page_url = hh_link + '/search/vacancy/' + paramsstr

    while True:
        html = requests.get(next_page_url, headers=headers)
        soup = bs(html.text, 'html.parser')

        vacancy_block = soup.find('div', {'class': "vacancy-serp"})
        try:
            next_page_url = hh_link + soup.find('a', {'data-qa': "pager-next"})['href']
        except:
            next_page_url = ''

        if not vacancy_block:
            print("Выходим из hh")
            next_page_url = ''
            break
        vacancy_list = vacancy_block.find_all('div', {'class': 'vacancy-serp-item'})


        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_site = hh_link
            vacancy_info = vacancy.find('span', {'class': 'g-user-content'}).find('a')
            vacancy_name = vacancy_info.getText()
            vacancy_link = vacancy_info['href']
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if(vacancy_salary):
                vacancy_salary = vacancy_salary.getText().strip()

                vacancy_salary = re.sub(r'(\d)\s*(\d)', r'\1\2', vacancy_salary)


                match = re.fullmatch(r'(\d+)\s*.\s*(\d+) (\w+.)', vacancy_salary)
                if (match):
                    salary_min = match.group(1)
                    salary_max = match.group(2)
                    salary_currency = match.group(3)

                else:
                    match = re.fullmatch(r'от\s*(\d+)\s*(\w+.)', vacancy_salary)
                    if (match):
                        salary_min = match.group(1)
                        salary_max = None
                        salary_currency = match.group(2)

                    else:
                        match = re.fullmatch(r'до\s*(\d+)\s*(\w+.)', vacancy_salary)
                        if (match):
                            salary_min = None
                            salary_max = match.group(1)
                            salary_currency = match.group(2)
                        else:
                            salary_min = None
                            salary_max = None
                            salary_currency = None
            else:
                salary_min = None
                salary_max = None
                salary_currency = None

            vacancy_company_info = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info'})
            vacancy_company_link = hh_link+vacancy_company_info.find('a')['href']
            vacancy_company_name = vacancy_company_info.getText().strip()
            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['company_link'] = vacancy_company_link
            vacancy_data['company_name'] = vacancy_company_name
            vacancy_data['site'] = vacancy_site
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency


            vacancies_hh.append(vacancy_data)

        if next_page_url == '' or (page >= maxpages and maxpages != 0):
            break
        page += 1

    print(f'Найдено {len(vacancies_hh)} вакансий на {page} страницах на сайте {hh_link}')


page = 1
error = 0
superjob_link = 'https://www.superjob.ru'
params = {'area': '1',
          'fromSearchLine': 'true',
          'st': 'searchVacancy',
          'text': myvacancy,
          'from': 'suggest_post'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

paramsstr = f"?keywords={myvacancy}&geo[t][0]=4"


next_page_url = superjob_link + '/vacancy/search/' + paramsstr

while True:
    html = requests.get(next_page_url, headers=headers)
    soup = bs(html.text, 'html.parser')

    vacancy_block = soup.find('div', {'class': "_1ID8B"})
    try:
        next_page_url = soup.find('div', {"class": "_3zucV L1p51 undefined _1Fty7 _2tD21 _3SGgo"})
        next_page_url = superjob_link + next_page_url.find('a', {"rel": "next"})["href"]
    except:
        next_page_url = ''

    if not vacancy_block:
        print("Выходим из superjob.ru")
        next_page_url = ''
        break
    vacancy_list = vacancy_block.find_all('div', {'class': 'f-test-vacancy-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_site = superjob_link
        try:
            vacancy_info = vacancy.find('div', {'class': 'jNMYr GPKTZ _1tH7S'})
            vacancy_info_a = vacancy_info.find('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'}).find('a')
            vacancy_name = vacancy_info_a.getText()
            vacancy_link = superjob_link + vacancy_info_a['href']

            vacancy_salary = vacancy_info.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'})
            if vacancy_salary:
                vacancy_salary = vacancy_salary.getText().strip()
                vacancy_salary = re.sub(r'(\d)\s*(\d)', r'\1\2', vacancy_salary)

                match = re.fullmatch(r'(\d+)\s*.\s*(\d+)\s*(\w+.)', vacancy_salary)
                if (match):
                    salary_min = match.group(1)
                    salary_max = match.group(2)
                    salary_currency = match.group(3)
                else:
                    match = re.fullmatch(r'от\s*(\d+)\s*(\w+.)', vacancy_salary)
                    if (match):
                        salary_min = match.group(1)
                        salary_max = None
                        salary_currency = match.group(2)
                    else:
                        match = re.fullmatch(r'до\s*(\d+)\s*(\w+.)', vacancy_salary)
                        if (match):
                            salary_min = None
                            salary_max = match.group(1)
                            salary_currency = match.group(2)
                        else:
                            salary_min = None
                            salary_max = None
                            salary_currency = None
            else:
                salary_min = None
                salary_max = None
                salary_currency = None

            vacancy_company_info = vacancy.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'}).find('a')
            vacancy_company_link = superjob_link+vacancy_company_info['href']
            vacancy_company_name = vacancy_company_info.getText().strip()

            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['company_link'] = vacancy_company_link
            vacancy_data['company_name'] = vacancy_company_name
            vacancy_data['site'] = vacancy_site
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency


            vacancies_superjob.append(vacancy_data)
        except:
            error += 1
    if next_page_url == '' or (page >= maxpages and maxpages != 0):
        break
    page += 1
print(f'Найдено {len(vacancies_superjob)} вакансий на {page} страницах на сайте {superjob_link}')

df = pd.DataFrame(vacancies_hh + vacancies_superjob)
pd.set_option('display.max_columns', None)
pprint(df)

to_json = {'hh': vacancies_hh, 'superjob': vacancies_superjob}
with open('vacancies.json', 'w') as outfile:
    json.dump(to_json, outfile)
