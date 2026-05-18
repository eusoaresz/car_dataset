# Sport Car Price Analyzer

Projeto em Python para analisar um arquivo CSV com dados de carros esportivos.
O programa abre um menu no terminal e permite ver estatísticas simples e gerar gráficos.

## O que o projeto faz

- Mostra as marcas com maior preço medio.
- Lista os 10 carros mais caros e os 10 mais baratos.
- Compara duas marcas escolhidas pelo usuario.
- Faz analise por ano.
- Gera graficos de pizza, barras, linha e dispersao.

## Arquivos principais

- `main.py`: ponto de entrada do programa.
- `src/car.py`: funcoes auxiliares de leitura e analise dos dados.
- `Sport car price.csv`: base de dados usada pelo projeto.

## Como executar

1. Abra o terminal na pasta do projeto.
2. Ative a sua virtualenv, se estiver usando uma.
3. Instale as dependencias.

```bash
python -m pip install pandas matplotlib
```

4. Rode o programa.

```bash
python main.py
```

## Observacoes

- O CSV deve ficar na pasta raiz do projeto.
- O programa procura automaticamente por arquivos com nome parecido com `Sport car price.csv`.
- Ao escolher a opcao `0`, o programa encerra.