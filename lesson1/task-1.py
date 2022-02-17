import requests
import json

main_link = 'https://api.github.com/users/'
name='TolstikovIgor'
response=requests.get(main_link+name+'/repos')
j_data=response.json()

new_j={}
print(f"Список репозиториев {name}:")
for i in range(len(j_data)):
    repository=j_data[i]['full_name'].replace(name+'/','')
    print(str(i+1)+') '+repository)
    new_j[i+1]=repository

with open('lesson-1.json', "w", encoding="utf-8") as file:
    json.dump(new_j, file)
