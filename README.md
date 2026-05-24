# Sport Car Price Analyzer

Projeto em Python para analisar um arquivo CSV com dados de carros esportivos.
O programa abre um menu no terminal e permite ver estatísticas simples e gerar gráficos.

## O que o projeto faz

- Mostra as 10 marcas com maior preço médio.
- Lista os 10 carros mais caros e os 10 mais baratos.
- Compara duas marcas escolhidas pelo usuário.
- Faz análise por ano com quantidade de modelos e preço médio.
- Gera gráficos de pizza e barras usando Plotly.
- Lê e normaliza automaticamente colunas como preço, potência, aceleração e ano.

## Arquivos principais

- `main.py`: versão principal do programa com leitura do CSV, análises e menu interativo.
- `src/car.py`: módulo com a implementação anterior das análises e gráficos em Matplotlib.
- `requirements.txt`: dependências do projeto.
- `Sport_car_price.csv`: base de dados usada pelo projeto.

## Como executar

1. Abra o terminal na pasta do projeto.
2. Ative a sua virtualenv, se estiver usando uma.
3. Instale as dependências.

```bash
python -m pip install -r requirements.txt
```

4. Rode o programa.

```bash
python main.py
```

## Menu atual

- `1` - Top 10 marcas por preço médio
- `2` - Top 10 mais caros e mais baratos
- `3` - Comparar duas marcas
- `4` - Análise por ano
- `5` - Gráfico de pizza por marca
- `6` - Gráfico de barras de média de preço por ano
- `0` - Sair

## Observações

- O CSV deve ficar na pasta raiz do projeto.
- O programa procura automaticamente por arquivos com nomes como `Sport_car_price.csv` e variações parecidas.
- O gráfico de pizza mostra as 10 marcas com mais modelos e agrupa o restante em "Outros".
- O gráfico de barras mostra a média de preço por ano.
- Ao escolher a opção `0`, o programa encerra.
