import requests
import csv
from bs4 import BeautifulSoup

def req_pag(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        return response.text
    except requests.exceptions.RequestException as e:
        print(f'Erro ao fazer requisição: {e}')
        return None



def quinto_andar(tipo_comp_alg, cidade, uf, max_paginas=100):
    dados_imoveis = []
    
    for page in range(1, max_paginas + 1):  # Loop limitado a 10 páginas
        url = f'https://www.quintoandar.com.br/{tipo_comp_alg}/imovel/{cidade}-{uf}-brasil?page={page}'
        html = req_pag(url)
        
        if html is None:
            break
        
        # Criando um objeto BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Buscando todos os elementos h3 e h2 com a classe CozyTypography
        h3_elements = soup.find_all('h3', class_='CozyTypography')
        h2_elements = soup.find_all('h2', class_='CozyTypography')
        
        if not h2_elements:
            break

        # Frases indesejadas para ignorar
        frases_indesejadas = [
            "Quanto custa comprar um imóvel", 
            "Qual bairro tem mais imóveis",
            "Qual a faixa de valor"
        ]

        # Agrupando as informações em trios
        for i in range(len(h2_elements)):
            if i * 3 + 2 >= len(h3_elements):
                continue  # Evita IndexError

            endereco = h2_elements[i].get_text(strip=True).replace('·', '-')
            preco = h3_elements[i * 3].get_text(strip=True).replace('R$ ', 'R$').replace('R$ ', 'R$')
            cond_iptu = h3_elements[i * 3 + 1].get_text(strip=True).replace('R$ ', 'R$').replace('R$ ', 'R$')
            detalhes = h3_elements[i * 3 + 2].get_text(strip=True).replace('·', '-')

            if not any(frase in preco for frase in frases_indesejadas):
                dados_imoveis.append([endereco, preco, cond_iptu, detalhes])
    
    return dados_imoveis

def salvar_csv(dados, nome_arquivo='imoveis.csv'):
    colunas = ['Endereco', 'Preco', 'Condominio_IPTU', 'Detalhes']
    
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow(colunas)
        escritor_csv.writerows(dados)

    print(f'Dados salvos com sucesso no arquivo {nome_arquivo}')


def main():
    ## Quinto Andar vars
    tipo_comp_alg = 'comprar'  # também pode ser 'alugar'
    cidade = 'guarulhos'       # sempre substituir espaço por traço
    uf = 'sp'
    
    dados_imoveis_qa = quinto_andar(tipo_comp_alg, cidade, uf)
    
    salvar_csv(dados_imoveis_qa, f'imoveis-{cidade}.csv')

if __name__ == '__main__':
    main()