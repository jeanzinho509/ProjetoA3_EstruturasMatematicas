import pandas as pd


def calcular_consumo_por_regiao(ano, regiao, arquivo_excel="./consumo_geral_v2.xlsx"):
    # Carregar dados do Excel
    df = pd.read_excel(arquivo_excel, header=None, names=["Ano", "Mês", "Região", "Consumo"])

    # Filtrar dados pelo ano e região
    filtro = (df["Ano"] == ano) & (df["Região"] == regiao)
    dados_filtrados = df[filtro]

    # Calcular o consumo total para a região e ano
    consumo_total = dados_filtrados["Consumo"].sum()

    return consumo_total
