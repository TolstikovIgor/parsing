# curl -v -X POST "https://api.artsy.net/api/tokens/xapp_token?" \
#                 "client_id=8ef31a9bba0348667324" \
#                 "&" \
#                 "client_secret=87ead3962807b43366ff0b01503cca3d"
import requests
client_id = "8ef31a9bba0348667324"
client_secret = "87ead3962807b43366ff0b01503cca3d"
concrete_params = {
    "client_id": client_id,
    "client_secret": client_secret
}
base_url = "https://api.artsy.net/api/tokens/xapp_token"
# url = f"https://api.artsy.net/api/tokens/xapp_token?" \
#       f"client_id={client_id}&client_secret={client_secret}"
# url = "https://api.artsy.net/api/tokens/xapp_token?" \
#                 "client_id=8ef31a9bba0348667324" \
#                 "&" \
#                 "client_secret=87ead3962807b43366ff0b01503cca3d"
r = requests.post(base_url, params=concrete_params)
from pprint import pprint
pprint(r.text)

headers = {
    "X-XAPP-Token": r.json()['token']
}
url = "https://api.artsy.net/api/artists"
r = requests.get(url, headers=headers)
pprint(r.json())
if r.ok:
    import json
    path = "some_artists.json"
    with open(path, "w") as f:
        json.dump(r.json(), f)