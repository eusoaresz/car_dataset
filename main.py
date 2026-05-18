import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Carrega os dados do CSV
def carrega_dados(caminho):
    df = pd.read_csv(caminho)
    df.columns = df.columns.str.strip()
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

    plt.figure(figsize=(8, 8))
    plt.pie(dados, labels=dados.index, autopct="%1.1f%%", startangle=140)
    plt.title("Distribuição de Modelos por Marca (Top 10 + Outros)")
    plt.tight_layout()
    plt.show()


def grafico_barras_decada(df):
    copia = df.copy()
    copia["Década"] = (copia["Year"] // 10 * 10).astype(str) + "s"
    resultado = copia.groupby("Década")["Price (in USD)"].mean().sort_index()

    plt.figure(figsize=(10, 5))
    resultado.plot(kind="bar", color="steelblue")
    plt.title("Preço Médio por Década")
    plt.xlabel("Década")
    plt.ylabel("Preço Médio (USD)")
    plt.tight_layout()
    plt.show()


def grafico_linha_ano(df):
    resultado = df.groupby("Year")["Price (in USD)"].mean().sort_index()

    plt.figure(figsize=(12, 5))
    plt.plot(resultado.index, resultado.values, marker="o", color="crimson", linewidth=2)
    plt.title("Evolução do Preço Médio por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Preço Médio (USD)")
    plt.tight_layout()
    plt.show()


def grafico_potencia_vs_preco(df):
    limpo = df.dropna(subset=["Horsepower", "Price (in USD)"])

    plt.figure(figsize=(10, 6))
    plt.scatter(limpo["Horsepower"], limpo["Price (in USD)"], alpha=0.4, color="darkorange")
    plt.title("Potência vs Preço")
    plt.xlabel("Potência (hp)")
    plt.ylabel("Preço (USD)")
    plt.tight_layout()
    plt.show()


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
    print("6. Gráfico de barras por década")
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
        grafico_barras_decada(dados)
    elif opcao == "7":
        grafico_linha_ano(dados)
    elif opcao == "8":
        grafico_potencia_vs_preco(dados)
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida.")