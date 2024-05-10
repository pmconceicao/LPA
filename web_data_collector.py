import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import os


        ###### Recolher e filtrar os dados das página Sala 1, Sala 2 e Sala 3 e guardá-los em ficheiros .csv com o
        ######  nome “sala1.csv”, “sala2.csv” e “sala3.csv” (respetivamente) no diretório “db”. Cada linha da
        ######  tabela da página web será uma linha no respetivo ficheiro com os valores separados por vírgula.

# Função para salvar os dados em um arquivo CSV
def salvar_csv(nome_arquivo, dados):
    df = pd.DataFrame(dados, columns=['Porta', 'Count RX (Bytes)', 'Count TX (Bytes)', 'Bitrate RX (Mbps)', 'Bitrate TX (Mbps)'])
    df.to_csv(nome_arquivo, index=False)

# Função para recolher os dados da página e filtrá-los
def recolher_dados(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    
    data = []
    for row in rows:
        cols = row.find_all(['th', 'td'])
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    
    # Remover a primeira linha (cabeçalho da tabela)
    data = data[1:]
    return data


# Diretório para salvar os arquivos CSV
diretorio = 'db'

# Cria o diretório se não existir
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

# URLs dos arquivos HTML
urls = ['sala1.html', 'sala2.html', 'sala3.html']

for i, url in enumerate(urls):
    # Construir o URL completo
    url_completa = f'https://anaconceicao26.github.io/P/{url}'  
    
    # Recolher dados da página
    dados = recolher_dados(url_completa)
    
    # Salvar os dados em um arquivo CSV
    nome_arquivo = os.path.join(diretorio, f'sala{i+1}.csv')
    salvar_csv(nome_arquivo, dados)



        ###### Crie os gráficos que achar adequados para representar os dados recolhidos (ex., gráfico linhas,
        ######  gráfico de barras, …).

# Função para criar gráfico de linhas para Count RX (Bytes) e Count TX (Bytes)
def criar_grafico_linhas_count(dados, titulos):
    plt.figure(figsize=(10, 6))
    for i in range(1, len(dados[0])):
        if i == 1 or i == 2:  # Verifica se é a segunda ou terceira coluna (Count RX ou Count TX)
            plt.plot([d[0] for d in dados[0:]], [float(d[i]) for d in dados[0:]], label=titulos[i+1])
    plt.xlabel('Porta')
    plt.ylabel('Valor')
    plt.title(titulos[0] + ' -> Count RX (Bytes) e Count TX (Bytes)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Ajustar escala do eixo y
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    plt.show()

# Função para criar gráfico de linhas para Bitrate RX (Mbps) e Bitrate TX (Mbps)
def criar_grafico_linhas_bitrate(dados, titulos):
    plt.figure(figsize=(10, 6))
    for i in range(1, len(dados[0])):
        if i == 3 or i == 4:  # Verifica se é a quarta ou quinta coluna (Bitrate RX ou Bitrate TX)
            plt.plot([d[0] for d in dados[0:]], [float(d[i]) for d in dados[0:]], label=titulos[i+1])
    plt.xlabel('Porta')
    plt.ylabel('Valor')
    plt.title(titulos[0] + ' -> Bitrate RX (Mbps) e Bitrate TX (Mbps)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    
    # Ajustar escala do eixo y
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    plt.show()


# Função para criar gráfico de barras para Count RX (Bytes) e Count TX (Bytes)
def criar_grafico_barras_count(dados, titulos):
    plt.figure(figsize=(10, 6))
    portas = [d[0] for d in dados[0:]]
    for i in range(1, len(dados[0])):
        if i == 1 or i == 2:  # Verifica se é a segunda ou terceira coluna (Count RX ou Count TX)
            valores = [float(d[i]) for d in dados[0:]]  # Considerando o primeiro valor da lista como o valor a ser representado
            plt.bar(portas, valores, label=titulos[i+1])
    plt.xlabel('Porta')
    plt.ylabel('Valor')
    plt.title(titulos[0] + ' - Count RX (Bytes) e Count TX (Bytes)')
    plt.legend()
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    
    # Ajustar escala do eixo y
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    plt.show()

# Função para criar gráfico de barras para Bitrate RX (Mbps) e Bitrate TX (Mbps)
def criar_grafico_barras_bitrate(dados, titulos):
    plt.figure(figsize=(10, 6))
    portas = [d[0] for d in dados[0:]]
    for i in range(1, len(dados[0])):
        if i == 3 or i == 4:  # Verifica se é a quarta ou quinta coluna (Bitrate RX ou Bitrate TX)
            valores = [float(d[i]) for d in dados[0:]]  # Considerando o primeiro valor da lista como o valor a ser representado
            plt.bar(portas, valores, label=titulos[i+1])
    plt.xlabel('Porta')
    plt.ylabel('Valor')
    plt.title(titulos[0] + ' - Bitrate RX (Mbps) e Bitrate TX (Mbps)')
    plt.legend()
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    
    # Ajustar escala do eixo y
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    plt.show()


# Criar gráficos para cada arquivo CSV
for i in range(1, 4):
    nome_arquivo_csv = f'db/sala{i}.csv'
    df = pd.read_csv(nome_arquivo_csv)
    
    # Extrair rótulos das colunas
    titulo1 = ['Gráfico de Linhas - ' + str(i)] + list(df.columns)
    titulo2 = ['Gráfico de Barras - ' + str(i)] + list(df.columns)
    
    # Gráfico de linhas
    criar_grafico_linhas_count(df.values.tolist(), titulo1)
    criar_grafico_linhas_bitrate(df.values.tolist(), titulo1)
    
    # Gráfico de barras
    criar_grafico_barras_count(df.values.tolist(), titulo2)
    criar_grafico_barras_bitrate(df.values.tolist(), titulo2)


