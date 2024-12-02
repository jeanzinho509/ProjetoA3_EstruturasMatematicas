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

# Carregar o arquivo Excel
df = pd.read_excel("consumo_geral_v2.xlsx")

# Garantir que a coluna 'Valor' é numérica
df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
df = df.dropna(subset=['Valor'])  # Remove linhas com valores inválidos

# Somar valores por Ano e Mês
total_mensal = df.groupby(['Ano', 'Mês'])['Valor'].sum().reset_index()
print(total_mensal)

# Agrupar por Ano e somar os valores para a regressão anual
consumo_anual = total_mensal.groupby('Ano')['Valor'].sum().reset_index()

# Preparar dados para regressão
x = consumo_anual['Ano'].values.reshape(-1, 1)  # Variável independente
y = consumo_anual['Valor'].values  # Variável dependente

# Garantir que os dados não estão vazios
if len(x) == 0 or len(y) == 0:
    print("Erro: Dados insuficientes para a regressão linear.")
else:
    # Criar e treinar o modelo
    modelo = LinearRegression()
    modelo.fit(x, y)

    # O que esse modelo faz? Ele ajusta uma linha reta aos dados, definindo uma equação da forma: (y = m * x + b)
    # m : inclinacao (taxa de variacao do consumo com o tempo)
    # b : intercepto (valor de y quando x = 0)

    # Prever o consumo para o próximo ano
    proximo_ano = np.array([[consumo_anual['Ano'].max() + 1]])
    previsao_proximo_ano = modelo.predict(proximo_ano)[0]

    print(f"Previsão de consumo para o próximo ano ({proximo_ano[0][0]}): {previsao_proximo_ano:,.2f}")
