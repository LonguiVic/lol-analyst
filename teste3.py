import requests
from bs4 import BeautifulSoup

url = 'https://docs.python.org/3/tutorial/index.html'
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

links = soup.find_all('a')

for link in links:
    href = link.get('href')
    if href:
        print(href)