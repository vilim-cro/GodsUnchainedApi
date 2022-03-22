import requests
import coinmarketcap_api

def obrisi(file_name):
    file = open(file_name,"r+")
    file.truncate(0)
    file.close()

def get_card_names():
    url = 'https://api.godsunchained.com/v0/proto?page=1&perPage=1193'
    data = requests.get(url).json()["records"]
    for card in data:
        if card["set"] != "core" and card["set"] != "welcome":
            names.append(card["name"])

def get_gods_card_price(name):
    url = f"https://api.x.immutable.com/v1/orders?order_by=buy_quantity&direction=asc&status=active&buy_token_address=0xccc8cb5229b0ac8069c51fd58367fd1e622afd97&sell_token_name={name.replace(' ', '%20')}&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c"
    headers = {"Accept": "application/json"}
    try:
        result = requests.request("GET", url, headers=headers).json()["result"]
        return result[0]["buy"]["data"]["quantity"]
    except:
        return -1

def get_eth_card_price(name):
    url = f"https://api.x.immutable.com/v1/orders?order_by=buy_quantity&direction=asc&status=active&buy_token_type=eth&sell_token_name={name.replace(' ', '%20')}&sell_token_address=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c"
    headers = {"Accept": "application/json"}
    try:
        result = requests.request("GET", url, headers=headers).json()["result"]
        return result[0]["buy"]["data"]["quantity"]
    except:
        return -1

#Nađi zadnju cijenu ETH i GODSa
gods_USD = round(coinmarketcap_api.get_price('GODS'), 2)
eth_USD = int(coinmarketcap_api.get_price('ETH'))
print(f"GODS: {gods_USD}$, ETH. {eth_USD}$")

names = []
get_card_names()

obrisi("velika_razlika.txt")
obrisi("mala_razlika.txt")
velika = open("velika_razlika.txt", "a")
mala = open("mala_razlika.txt", "a")

for name in names:
    gods_cijena = int(get_gods_card_price(name)) / 1.0E18 * gods_USD
    price = get_eth_card_price(name)
    eth_cijena = int(get_eth_card_price(name)) / 1.0E18 * eth_USD
    razlika = gods_cijena - eth_cijena
    rel_raz = razlika / eth_cijena * 100
    if gods_cijena >= 0 and eth_cijena >= 0:
        print(f"{name} | {round(gods_cijena, 2)}$ (GODS) | {round(eth_cijena, 2)}$ (ETH) | {round(razlika, 1)}$ | {round(rel_raz, 1)}%")
        if (eth_cijena <= 150 and rel_raz <= 0):
            mala.write(f"Karta: {name} | Razlika u cijeni: {razlika} ({rel_raz}%)\n")
        if (eth_cijena <= 150 and razlika >= 1 and rel_raz >= 15):
            velika.write(f"Karta: {name} | Razlika u cijeni: {razlika} ({rel_raz}%)\n")

mala.close()
velika.close()

