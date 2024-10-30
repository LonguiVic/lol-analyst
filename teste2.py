import requests
from bs4 import BeautifulSoup


url = 'https://lista.mercadolivre.com.br/pcs#D[A:pcs]'
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

precos = soup.find_all('span', class_='andes-money-amount__fraction')

for preco in precos:
    print(preco.text.strip())