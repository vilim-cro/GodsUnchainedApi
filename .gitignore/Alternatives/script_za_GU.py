#Selenium imports
from idna import check_hyphen_ok
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import coinmarketcap_api

BROJ_PON = 5

class Karta:
    def __init__(self, ime):
        self.ime = ime
        self.eth = 0
        self.gods = 0
        self.razlika = 0
        self.rel_raz = 0

#Nađi zadnju cijenu ETH i GODSa
gods_USD = round(coinmarketcap_api.get_price('GODS'), 2)
eth_USD = int(coinmarketcap_api.get_price('ETH'))
print(f"GODS: {gods_USD}$, ETH. {eth_USD}$")

DRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe'

def obrisi(file_name):
    file = open(file_name,"r+")
    file.truncate(0)
    file.close()

def nadi_kandidate():
    obrisi("imena.txt")
    dat = open("imena.txt", "a")
    SITE_PATH = "https://gudecks.com/meta/card-rankings?userRank=4&decksWithCard=5000"
    driver.get(SITE_PATH)
    imena = []
    cookie_accept = 0
    try:
        cookie_accept = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="I understand"]'))
                )
    finally:
        cookie_accept.click()
    for i in range(BROJ_PON):
        try:
            imena = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-ranking-name'))
                    )
        finally:
            for ime in imena:
                dat.write(ime.get_attribute('innerHTML'))
                dat.write('\n')
        next = driver.find_element(By.XPATH, '//button[text()=">"]')
        next.click()
    
    dat.close()

def nadi_cijenu(card_name, token):
    SITE_PATH = f"https://market.immutable.com/assets?collection=0xacb3c6a43d15b907e8433077b6d38ae40936fe2c&keywordSearch={card_name}&{token}&sort[order_by]=buy_quantity&sort[direction]=asc"
    driver.get(SITE_PATH)
    cijena = 0
    try:
        cijena = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'css-fidqih'))
            )
    finally:
        if cijena != 0:
            return cijena.get_attribute('innerHTML')
        else:
            return 100000

def nadi_razliku(card_name):
    karta = Karta(card_name)
    karta.eth = float(nadi_cijenu(card_name, "currencyFilter[buy_token_type]=ETH"))
    karta.gods = float(nadi_cijenu(card_name, "currencyFilter[buy_token_address]=0xccc8cb5229b0ac8069c51fd58367fd1e622afd97"))
    karta.razlika = round(karta.gods * gods_USD - karta.eth * eth_USD, 1)
    karta.rel_raz = round((karta.razlika / (karta.eth * eth_USD)) * 100, 1)
    return karta

op = Options()
#op.add_argument('--headless')
driver = webdriver.Chrome(DRIVER_PATH, options=op)

#nadi karte kandidate
nadi_kandidate()

#imena
dat1 = open("imena.txt", "r")
lista = dat1.read().splitlines()

obrisi("velika_razlika.txt")
obrisi("mala_razlika.txt")
velika = open("velika_razlika.txt", "a")
mala = open("mala_razlika.txt", "a")

for ime in lista:
    karta = nadi_razliku(ime.replace(' ', '%20'))
    print(f"{karta.ime.replace('%20', ' ')} | {round(karta.gods * gods_USD, 1)}$ (GODS)| {round(karta.eth * eth_USD, 1)}$ (ETH) | {karta.razlika}$ | {karta.rel_raz}%")
    if (karta.eth * eth_USD <= 150 and karta.rel_raz <= 0):
        mala.write(f"Karta: {ime} | Razlika u cijeni: {karta.razlika} ({karta.rel_raz}%)\n")
    if (karta.eth * eth_USD <= 150 and karta.razlika >= 1 and karta.rel_raz >= 15):
        velika.write(f"Karta: {ime} | Razlika u cijeni: {karta.razlika} ({karta.rel_raz}%)\n")
mala.close()
velika.close()
driver.quit()

