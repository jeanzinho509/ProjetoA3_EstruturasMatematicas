from flask import Flask, render_template, request
from consumo_calculos import calcular_consumo_por_regiao

app = Flask(__name__)


@app.route('/')
def index():
    # Variáveis padrão quando a página é carregada pela primeira vez
    return render_template('index.html', consumo=None, regiao=None, ano=None)


@app.route('/calcular', methods=['POST'])
def calcular():
    # Capturar dados do formulário
    ano = int(request.form['ano'])
    regiao = request.form['regiao']

    # Chamar a função de cálculo
    consumo = calcular_consumo_por_regiao(ano, regiao)

    # Enviar os resultados para o template
    return render_template('index.html', ano=ano, regiao=regiao, consumo=consumo)


if __name__ == '__main__':
    app.run(debug=True)
