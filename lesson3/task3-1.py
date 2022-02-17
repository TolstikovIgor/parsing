from pymongo import MongoClient
import json
from pprint import pprint

data = json.load(open("vacancies.json"))

for vac in (data['hh'] + data['superjob']):
    try:
        vac['salary_min'] = float(vac['salary_min'])
    except:
        vac['salary_min'] = None
    try:
        vac['salary_max'] = float(vac['salary_max'])
    except:
        vac['salary_max'] = None

client = MongoClient('localhost', 27017)
db = client['vacancies_db']

vacancies = db.vacancies

vacancies.drop()


def add_vacancy(curvacancy, col):
    if not col.count_documents({'link': curvacancy['link']}):
        col.insert_one(curvacancy)


def add_vacancy1(curvacancy, col):
    try:
        col.replace_one({'link': curvacancy['link']}, curvacancy, upsert=True)
    except ValueError:
        print(ValueError)


for vacancy in (data['hh'] + data['superjob']):
    add_vacancy1(vacancy, vacancies)

print(vacancies.count())


def print_vacancy(vacancies):
    mysalary = input('Вывести вакансии с зарплатой выше : ')
    try:
        mysalary = float(mysalary)
    except:
        mysalary = 0
    for vacancy in vacancies.find({'$or': [{'salary_min': {'$gt': mysalary}}, {'salary_max': {'$lt': mysalary}}]}):
        pprint(vacancy)


print_vacancy(vacancies)
