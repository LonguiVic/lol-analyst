import requests
from bs4 import BeautifulSoup

url = 'https://globo.com'
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

titulos = soup.find_all('h2', class_='post__title')

for titulo in titulos:
    print(titulo.text.strip())