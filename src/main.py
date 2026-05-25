import pandas as pd
import plotly.express as px
from pathlib import Path

def carrega_dados(caminho):
    df = pd.read_csv(caminho)
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()

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

    if "0-60 MPH Time (seconds)" in df.columns:
        df["0-60 MPH Time (seconds)"] = pd.to_numeric(
            df["0-60 MPH Time (seconds)"].astype(str).str.extract(r"(\d+\.?\d*)", expand=False),
            errors="coerce",
        )

    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

    return df


def formata_preco(valor):
    return f"${valor:,.0f}"


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


def top_10_mais_potentes(df):
    cols = ["Car Make", "Car Model", "Year", "Horsepower", "Price (in USD)"]
    resultado = df.dropna(subset=["Horsepower"]).nlargest(10, "Horsepower")[cols]
    print("\n=== Top 10 Carros Mais Potentes ===")
    print(f"  {'Marca/Modelo':<40} {'Ano':>4}  {'Potência':>10}  {'Preço':>14}")
    for _, linha in resultado.iterrows():
        nome = f"{linha['Car Make']} {linha['Car Model']}"
        print(f"  {nome:<40} {linha['Year']:>4}  {int(linha['Horsepower']):>8} hp  {formata_preco(linha['Price (in USD)']):>14}")


def analisa_por_ano(df):
    anos_disponiveis = sorted(df["Year"].dropna().unique().astype(int))
    print(f"\nAnos disponíveis: {anos_disponiveis[0]} – {anos_disponiveis[-1]}")

    try:
        ano = int(input("Digite o ano para análise: ").strip())
    except ValueError:
        print("Ano inválido.")
        return

    todas_marcas  = set(df["Car Make"])
    marcas_com    = set(df[df["Year"] == ano]["Car Make"].dropna().unique())
    marcas_sem    = todas_marcas - marcas_com

    print(f"\n=== Análise por Ano: {ano} ===")
    print(f"  Total de marcas no dataset:      {len(todas_marcas)}")
    print(f"  Marcas COM modelos em {ano}:     {len(marcas_com)}")
    print(f"  Marcas SEM modelos em {ano}:     {len(marcas_sem)}")

    if marcas_com:
        print(f"\n  Marcas presentes em {ano}:")
        for m in sorted(marcas_com):
            qtd = len(df[(df["Year"] == ano) & (df["Car Make"] == m)])
            print(f"    {m:<25} {qtd} modelo(s)")
    else:
        print(f"\n  Nenhuma marca possui modelos em {ano}.")

    if marcas_sem:
        print(f"\n  Marcas ausentes em {ano}:")
        print("   ", ", ".join(sorted(marcas_sem)))


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


if __name__ == "__main__":
    caminho_csv = acha_csv()
    if caminho_csv:
        dados = carrega_dados(caminho_csv)
        print(f"Dados carregados: {len(dados)} registros, {dados['Car Make'].nunique()} marcas.")
    else:
        print("Arquivo CSV não encontrado.")
        exit()

    while True:
        print("\n=== Sport Car Price ===")
        print("1. Top 10 marcas por preço médio")
        print("2. Top 10 mais caros e mais baratos")
        print("3. Comparar duas marcas")
        print("4. Top 10 mais potentes")
        print("5. Gráfico de pizza por marca")
        print("6. Gráfico de barras de média de preço por ano")
        print("7. Análise por ano")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            top_10_marcas_preco(dados)
        elif opcao == "2":
            carros_mais_e_menos_caros(dados)
        elif opcao == "3":
            compara_duas_marcas(dados)
        elif opcao == "4":
            top_10_mais_potentes(dados)
        elif opcao == "5":
            grafico_pizza_marcas(dados)
        elif opcao == "6":
            grafico_media_preco_ano(dados)
        elif opcao == "7":
            analisa_por_ano(dados)
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")