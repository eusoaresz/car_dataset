import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path

pio.renderers.default = "browser"

# Carrega os dados do CSV
def carrega_dados(caminho):
    df = pd.read_csv(caminho)
    df.columns = df.columns.str.strip()

    # Normaliza e converte colunas numéricas que vêm como string
    if "Price (in USD)" in df.columns:
        df["Price (in USD)"] = pd.to_numeric(
            df["Price (in USD)"].astype(str).str.replace(r'[$,]', '', regex=True),
            errors="coerce",
        )

    if "Horsepower" in df.columns:
        df["Horsepower"] = pd.to_numeric(
            df["Horsepower"].astype(str).str.extract(r"(\d+\.?\d*)", expand=False),
            errors="coerce",
        )

    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

    return df


def formata_preco(valor):
    return f"${valor:,.0f}"


# Análises
def top_10_marcas_preco(df):
    resultado = df.groupby("Car Make")["Price (in USD)"].mean().sort_values(ascending=False).head(10)
    print("\n=== Top 10 Marcas por Preço Médio ===")
    for marca, preco in resultado.items():
        print(f"  {marca:<20} {formata_preco(preco)}")


def carros_mais_e_menos_caros(df):
    cols = ["Car Make", "Car Model", "Year", "Price (in USD)"]
    mais_caros = df.nlargest(10, "Price (in USD)")[cols]
    menos_caros = df.nsmallest(10, "Price (in USD)")[cols]

    print("\n=== Top 10 Carros Mais Caros ===")
    for _, linha in mais_caros.iterrows():
        print(f"  {linha['Car Make']} {linha['Car Model']} ({linha['Year']}) — {formata_preco(linha['Price (in USD)'])}")

    print("\n=== Top 10 Carros Mais Baratos ===")
    for _, linha in menos_caros.iterrows():
        print(f"  {linha['Car Make']} {linha['Car Model']} ({linha['Year']}) — {formata_preco(linha['Price (in USD)'])}")


def compara_duas_marcas(df):
    marcas = sorted(df["Car Make"].unique())
    print("\nMarcas disponíveis:", ", ".join(marcas))

    marca1 = input("Digite a 1ª marca: ").strip()
    marca2 = input("Digite a 2ª marca: ").strip()

    for marca in [marca1, marca2]:
        filtro = df[df["Car Make"].str.lower() == marca.lower()]
        if filtro.empty:
            print(f"  Marca '{marca}' não encontrada.")
            continue
        print(f"\n--- {marca} ({len(filtro)} modelos) ---")
        print(f"  Preço médio:     {formata_preco(filtro['Price (in USD)'].mean())}")
        print(f"  Preço máximo:    {formata_preco(filtro['Price (in USD)'].max())}")
        print(f"  Preço mínimo:    {formata_preco(filtro['Price (in USD)'].min())}")
        print(f"  Potência média:  {filtro['Horsepower'].mean():.0f} hp")
        print(f"  0-60 mph médio:  {filtro['0-60 MPH Time (seconds)'].mean():.2f} s")


def analisa_por_ano(df):
    resultado = df.groupby("Year")["Price (in USD)"].agg(["mean", "count"]).sort_index(ascending=False)
    print("\n=== Análise por Ano ===")
    print(f"  {'Ano':<6} {'Qtd':>4}  {'Preço Médio':>14}")
    for ano, linha in resultado.iterrows():
        print(f"  {ano:<6} {int(linha['count']):>4}  {formata_preco(linha['mean']):>14}")


# Gráficos
def grafico_pizza_marcas(df):
    contagem = df["Car Make"].value_counts()
    top = contagem.head(10)
    outros = contagem.iloc[10:].sum()
    dados = pd.concat([top, pd.Series({"Outros": outros})])

    fig = px.pie(
        values=dados.values,
        names=dados.index,
        title="Distribuição de Modelos por Marca (Top 10 + Outros)",
        hole=0.35,
    )
    fig.show()


def grafico_media_preco_ano(df):
    copia = df.dropna(subset=["Year", "Price (in USD)"]).copy()
    resultado = copia.groupby("Year")["Price (in USD)"].mean().sort_index()

    fig = px.bar(
        x=resultado.index.astype(int),
        y=resultado.values,
        title="Preço Médio por Ano",
        labels={"x": "Ano", "y": "Preço Médio (USD)"},
    )
    fig.show()


def grafico_linha_ano(df):
    resultado = df.groupby("Year")["Price (in USD)"].mean().sort_index()

    fig = px.line(
        x=resultado.index.astype(int),
        y=resultado.values,
        markers=True,
        title="Evolução do Preço Médio por Ano",
        labels={"x": "Ano", "y": "Preço Médio (USD)"},
    )
    fig.show()


def grafico_potencia_vs_preco(df):
    limpo = df.dropna(subset=["Horsepower", "Price (in USD)"])

    fig = px.scatter(
        limpo,
        x="Horsepower",
        y="Price (in USD)",
        title="Potência vs Preço",
        opacity=0.4,
        labels={"Horsepower": "Potência (hp)", "Price (in USD)": "Preço (USD)"},
    )
    fig.show()


# Menu principal
def acha_csv():
    raiz = Path(__file__).parent
    nomes = [
        raiz / "Sport car price.csv",
        raiz / "Sport_car_price.csv",
        raiz / "sport car price.csv",
        raiz / "sport_car_price.csv",
    ]
    for arquivo in nomes:
        if arquivo.exists():
            return arquivo
    for arquivo in raiz.iterdir():
        if arquivo.suffix.lower() == ".csv":
            return arquivo
    return None


# Carregamento do CSV
caminho_csv = acha_csv()
if caminho_csv:
    dados = carrega_dados(caminho_csv)
    print(f"Dados carregados: {len(dados)} registros, {dados['Car Make'].nunique()} marcas.")
else:
    print("Arquivo CSV não encontrado.")
    exit()


# Loop do menu
while True:
    print("\n=== Sport Car Price ===")
    print("1. Top 10 marcas por preço médio")
    print("2. Top 10 mais caros e mais baratos")
    print("3. Comparar duas marcas")
    print("4. Análise por ano")
    print("5. Gráfico de pizza por marca")
    print("6. Gráfico de barras de média de preço por ano")
    print("7. Gráfico de linha por ano")
    print("8. Gráfico de potência vs preço")
    print("0. Sair")

    opcao = input("\nEscolha uma opção: ").strip()

    if opcao == "1":
        top_10_marcas_preco(dados)
    elif opcao == "2":
        carros_mais_e_menos_caros(dados)
    elif opcao == "3":
        compara_duas_marcas(dados)
    elif opcao == "4":
        analisa_por_ano(dados)
    elif opcao == "5":
        grafico_pizza_marcas(dados)
    elif opcao == "6":
        grafico_media_preco_ano(dados)
    elif opcao == "7":
        grafico_linha_ano(dados)
    elif opcao == "8":
        grafico_potencia_vs_preco(dados)
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida.")