from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
mongo_base = client.instagram

col = mongo_base['instagram']


username = input('Введите логин пользователя , чьи подписки и подписчики вас интересуют (для выхода ничего не вводите):  ')

if username:
    if col.count_documents({"username": username}):
        user_data = col.find_one({"username": username})

        for user_id in user_data['subscriptions']:
            try:
                if col.count_documents({"user_id": user_id}):
                    pass
                else:
                    print(f"Не найден {user_id}")
            except:
                print(f"Ошибка {user_id}")

        print(f"Всего подписок {len(user_data['subscriptions'])}")

        user_id = user_data['user_id']

        users_doc = col.find({"subscriptions": user_id})
        for subs in users_doc:

           pass

        print(f'Всего подписчиков {col.count_documents({"subscriptions": user_id})}')

    else:
        print(f'Пользоватли с логином {username} не найдены')