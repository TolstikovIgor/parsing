import requests
from pprint import pprint
from fake_useragent import UserAgent

u = UserAgent()
# print(u.random)

url = "http://yandex.ru"
headers = {
    "User-Agent": u.random
}
r = requests.get(url, headers=headers)

pprint(dict(r.headers))

print("Done")
if r.status_code == 200:
    print("Success!")
else:
    print("Nothing...")

if r.ok:
    print("success!!!")
