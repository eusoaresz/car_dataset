# Sport Car Price Analyzer

Projeto em Python para analisar um arquivo CSV com dados de carros esportivos.
O programa abre um menu no terminal e permite ver estatísticas simples e gerar gráficos.

## O que o projeto faz

- Mostra as 10 marcas com maior preço médio.
- Lista os 10 carros mais caros e os 10 mais baratos.
- Compara duas marcas escolhidas pelo usuário, exibindo preço médio, máximo, mínimo, potência média e 0-60 mph médio.
- Mostra os 10 carros mais potentes.
- Faz análise por ano, mostrando marcas presentes e ausentes em um ano escolhido.
- Gera gráficos de pizza por marca e de barras com a média de preço por ano.
- Lê e normaliza automaticamente colunas como preço, potência, aceleração e ano.
- Remove duplicatas ao carregar os dados.

## Estrutura do projeto

- `src/main.py`: versão principal do programa com leitura do CSV, análises, gráficos e menu interativo.
- `src/car.py`: implementação anterior com leitura via `csv` e gráficos em Matplotlib.
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
python src/main.py
```

## Menu atual

- `1` - Top 10 marcas por preço médio
- `2` - Top 10 mais caros e mais baratos
- `3` - Comparar duas marcas
- `4` - Top 10 mais potentes
- `5` - Gráfico de pizza por marca
- `6` - Gráfico de barras de média de preço por ano
- `7` - Análise por ano
- `0` - Sair

## Observações

- O CSV deve ficar na pasta raiz do projeto ou em `src/`.
- O programa procura automaticamente por arquivos com nomes como `Sport_car_price.csv` e variações parecidas.
- O gráfico de pizza mostra a distribuição de modelos por marca, agrupando o restante em "Outros".
- O gráfico de barras mostra a média de preço por ano.
- Ao escolher a opção `0`, o programa encerra.
