import time
import os
from requests.models import Response
import urllib3
from bs4 import BeautifulSoup
from urllib3 import request

def texte():
    url_search = 'https://www.amazon.fr/s?k=tablette&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_1' 
    http = urllib3.PoolManager()

    req = http.request("GET", url_search)

    if req.status == 200 :
        soup = BeautifulSoup(req.data, 'lxml')
        liste = []
        cartes = soup.find_all('div',{'data-component-type':'s-search-result'})
        for carte in cartes:
            href = carte.find('h2').find('a')['href']
            lien = (f'https://www.amazon.fr{href}')
            liste.append(lien)

        for i in liste:
            print(str(i))


        with open('url.txt', 'w') as file:
            for lien in liste:
                file.write(lien +'\n')
    else:
        print(req.status)
    http.clear()

#texte()

def extraction():
    m=0
    c = 0
    http = urllib3.PoolManager()
    with open ('url.txt','r') as file:
        with open('info.txt','w') as file_2:
            file_2.write('name,price\n')
            for row in file:
                url = row.strip()
                reponse = http.request('GET', url)
                erreur = reponse.status
                if reponse.status == 200:
                    soup = BeautifulSoup(reponse.data, 'lxml')
                    find_price = soup.find('span', {'id':'priceblock_ourprice'})
                    if find_price != None:
                        price = find_price.text.strip()
                    else:
                        pass
                    find_nom = soup.find('span', {'id':'productTitle'})
                    if find_nom != None:   
                        nom = find_nom.text.strip()
                    print(nom+','+ price)
                    file_2.write(nom +','+ price +'\n')
                    c = c + 1
                else:
                    print(f'erreur {erreur}')
                    m = m + 1
                    pass
                time.sleep(1)
            print(f'{c} objets ont été référencés.')
            print(f'il y eu {m} erreur(s)' )
            
        file_2.close        
    file.close()
    

extraction()
