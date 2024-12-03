# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt
#
# # Carregar o arquivo Excel
# df = pd.read_excel("consumo_geral_v2.xlsx")
#
# # Garantir que a coluna 'Valor' é numérica
# df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
# df = df.dropna(subset=['Valor'])  # Remove linhas com valores inválidos
#
# # Somar valores por Ano e Mês
# total_mensal = df.groupby(['Ano', 'Mês'])['Valor'].sum().reset_index()
#
# # Debug: Verificar os dados agrupados
# print("Total Mensal Agrupado:")
# print(total_mensal)
#
# # Agrupar por Ano e somar os valores para a regressão anual
# consumo_anual = total_mensal.groupby('Ano')['Valor'].sum().reset_index()
#
# # Debug: Verificar os dados anuais
# print("Consumo Anual Agrupado:")
# print(consumo_anual)
#
# # Preparar dados para regressão
# X = consumo_anual['Ano'].values.reshape(-1, 1)  # Variável independente
# y = consumo_anual['Valor'].values  # Variável dependente
#
# # Garantir que os dados não estão vazios
# if len(X) == 0 or len(y) == 0:
#     print("Erro: Dados insuficientes para a regressão linear.")
# else:
#     # Criar e treinar o modelo
#     modelo = LinearRegression()
#     modelo.fit(X, y)
#
#     # Fazer previsões para os próximos 5 anos
#     anos_futuros = 2
#     anos = np.arange(consumo_anual['Ano'].min(), consumo_anual['Ano'].max() + anos_futuros + 1).reshape(-1, 1)
#     previsoes = modelo.predict(anos)
#
#     # Criar DataFrame com previsões
#     previsao_df = pd.DataFrame({'Ano': anos.flatten(), 'Consumo Previsto': previsoes})
#     print("Previsão de Consumo:")
#     print(previsao_df)
#
#     # Plotar o gráfico
#     plt.figure(figsize=(10, 6))
#     plt.scatter(X, y, color='blue', label='Consumo Real')
#     plt.plot(anos, previsoes, color='red', label='Previsão')
#     plt.xlabel('Ano')
#     plt.ylabel('Consumo Total (MWh)')
#     plt.title('Previsão de Consumo de Energia Elétrica')
#     plt.legend()
#     plt.show()

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from dash import Dash, dcc, html
import plotly.express as px

# Carregar o arquivo Excel diretamente
def carregar_dados():
    df = pd.read_excel("consumo_geral_v2.xlsx")

    # Garantir que a coluna 'Valor' é numérica
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
    df = df.dropna(subset=['Valor'])  # Remove linhas com valores inválidos

    # Somar valores por Ano e Mês
    total_mensal = df.groupby(['Ano', 'Mês'])['Valor'].sum().reset_index()

    # Agrupar por Ano e somar os valores para a regressão anual
    consumo_anual = total_mensal.groupby('Ano')['Valor'].sum().reset_index()

    return total_mensal, consumo_anual

# Criar modelo de regressão
def criar_modelo(consumo_anual):
    x = consumo_anual['Ano'].values.reshape(-1, 1)  # Variável independente
    y = consumo_anual['Valor'].values  # Variável dependente

    modelo = LinearRegression()
    modelo.fit(x, y)
    return modelo

# Previsão do próximo ano
def prever_proximo_ano(modelo, consumo_anual):
    proximo_ano = np.array([[consumo_anual['Ano'].max() + 1]])
    previsao = modelo.predict(proximo_ano)[0]
    return proximo_ano[0][0], previsao

# Preparar gráfico
app = Dash(__name__)

def criar_graficos(total_mensal, consumo_anual):
    fig_mensal = px.line(total_mensal, x='Mês', y='Valor', color='Ano', title='Consumo Mensal por Ano')
    fig_anual = px.bar(consumo_anual, x='Ano', y='Valor', title='Consumo Anual Total')
    return fig_mensal, fig_anual

# Dados iniciais
total_mensal, consumo_anual = carregar_dados()
modelo = criar_modelo(consumo_anual)
proximo_ano, previsao = prever_proximo_ano(modelo, consumo_anual)

fig_mensal, fig_anual = criar_graficos(total_mensal, consumo_anual)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Previsão de Consumo de Energia no Brasil"),

    html.Div([
        html.H3(f"Previsão para {proximo_ano}: {previsao:,.2f} kWh"),
    ], style={"margin-bottom": "30px"}),

    dcc.Graph(figure=fig_mensal),
    dcc.Graph(figure=fig_anual),
])

if __name__ == "__main__":
    app.run_server(debug=True)
