import web3
import json
import time
from datetime import datetime
from threading import Timer
import requests
import sys
import os

#https://bsc-dataseed.binance.org mainnet
#https://data-seed-prebsc-1-s1.binance.org:8545 testnet
w3 = web3.Web3(web3.HTTPProvider("https://bsc-dataseed.binance.org"))
site_url = "http://dexseed.top/launchpad/"
#site_url = "http://localhost/launchpad/"

def update_raised_amount():
    try:
        resposta = requests.get(site_url+'/update_raised_amount.php')
        print(str(resposta.content))
    except:
        print(f'Pool offline')
        pass

def checar_transacao():
    try:
        resposta = requests.get(site_url+'/pool.php')
        json_resposta = resposta.json()
        hash_tx = json_resposta['hash_tx']
        amount2 = float(json_resposta['amount_tx'])
        amount = amount2-0.001
        bep20 = json_resposta['bep20']
        tx_hash = hash_tx
        if(amount>0):
            try:
                tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                my_tx = w3.eth.getTransaction(tx_hash)
                valor = my_tx.value/1000000000000000000
                carteira = my_tx.to
            except:
                valor = 0
                carteira = 0
                pass
        else:
            valor = 0
            carteira = 0
        print(carteira)
        print(valor)

        if(bep20==carteira):
            print(f'carteira ok')
            carteiraok = 1
        else:
            print(f'carteira errada')
            carteiraok = 0
        if(valor>=amount):
            print(f'valor ok')
            valorok = 1
        else:
            print('valor errado')
            valorok = 0
        if(carteiraok == 1 & valorok==1):
            print(f'tudo ok')
            resposta2 = requests.get(site_url+'check.php?hash='+hash_tx+'&confirm=2&recebido=xZxZxZDf09ç8jHjHyuh3Dsapzçç')
        else:
            resposta2 = requests.get(site_url+'check.php?hash='+hash_tx+'&confirm=1&recebido=xZxZxZDf09ç8jHjHyuh3Dsapzçç')
            print(hash_tx)
            os.system('cls' if os.name =='nt' else 'clear')
    except:
        print(f'Pool offline')
        pass

run = True
def asyncTask1():
    global run
    checar_transacao()
    if run:
        Timer(3, asyncTask1).start()
        
def asyncTask2():
    global run
    update_raised_amount()
    if run:
        Timer(60 * 1, asyncTask2).start()

asyncTask1()
asyncTask2()
