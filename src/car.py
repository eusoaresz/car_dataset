import csv
from pathlib import Path
import matplotlib.pyplot as plt

raiz = Path(__file__).parent.parent
arquivo_csv = None

# Procura o arquivo CSV
nomes_csv = [
    raiz / "Sport car price.csv",
    raiz / "Sport_car_price.csv",
    raiz / "sport_car_price.csv",
    raiz / "sport car price.csv",
]
for arquivo in nomes_csv:
    if arquivo.exists():
        arquivo_csv = arquivo
        break

if arquivo_csv is None:
    for arquivo in raiz.iterdir():
        if arquivo.suffix.lower() == ".csv":
            arquivo_csv = arquivo
            break


# Carrega os dados
def carrega_carros(caminho_arquivo=arquivo_csv):
    carros = []
    
    with open(caminho_arquivo, encoding="utf-8-sig", newline="") as arq:
        dados = csv.DictReader(arq)
        for linha in dados:
            try:
                preco = float(str(linha.get("Price (in USD)", "0")).replace(",", "").replace("\"", ""))
                ano = int(linha.get("Year", "")) if linha.get("Year", "").isdigit() else None
                
                carro = {
                    "marca": linha.get("Car Make", "").strip(),
                    "modelo": linha.get("Car Model", "").strip(),
                    "ano": ano,
                    "motor": linha.get("Engine Size (L)", "").strip(),
                    "potencia": linha.get("Horsepower", "").strip(),
                    "torque": linha.get("Torque (lb-ft)", "").strip(),
                    "aceleracao": linha.get("0-60 MPH Time (seconds)", "").strip(),
                    "preco": preco,
                }
                carros.append(carro)
            except:
                continue
    
    return carros


def formata_preco(valor):
    return f"${valor:,.2f}"


# Análises
def top_10_mais_caros(carros):
    ordenados = sorted(carros, key=lambda c: c["preco"], reverse=True)[:10]
    
    print("\nTop 10 carros mais caros")
    for i, carro in enumerate(ordenados, start=1):
        nome = f"{carro['marca']} {carro['modelo']}"
        print(f"{i:2}. {nome:<40} {formata_preco(carro['preco'])}")


def top_10_antigos_e_novos(carros):
    com_ano = [c for c in carros if c["ano"] is not None]
    
    antigos = sorted(com_ano, key=lambda c: (c["ano"], c["marca"], c["modelo"]))[:10]
    novos = sorted(com_ano, key=lambda c: (-c["ano"], c["marca"], c["modelo"]))[:10]
    
    print("\nTop 10 modelos mais antigos")
    for i, carro in enumerate(antigos, start=1):
        print(f"{i:2}. {carro['marca']} {carro['modelo']:<30} {carro['ano']}")
    
    print("\nTop 10 modelos mais recentes")
    for i, carro in enumerate(novos, start=1):
        print(f"{i:2}. {carro['marca']} {carro['modelo']:<30} {carro['ano']}")


def compara_duas_marcas(carros):
    marcas = sorted({c["marca"] for c in carros})
    
    print("\nMarcas disponíveis:")
    for marca in marcas:
        print(f"- {marca}")
    
    marca1 = input("\nDigite a primeira marca: ").strip()
    marca2 = input("Digite a segunda marca: ").strip()
    
    def calcula_media(marca):
        precos = [c["preco"] for c in carros if c["marca"].lower() == marca.lower()]
        if not precos:
            return None
        return sum(precos) / len(precos)
    
    media1 = calcula_media(marca1)
    media2 = calcula_media(marca2)
    
    print("\nComparacao de preco medio")
    if media1 is None:
        print(f"{marca1}: marca nao encontrada.")
    else:
        print(f"{marca1}: {formata_preco(media1)} (media)")
    
    if media2 is None:
        print(f"{marca2}: marca nao encontrada.")
    else:
        print(f"{marca2}: {formata_preco(media2)} (media)")


def analisa_por_ano(carros):
    try:
        ano = int(input("\nDigite o ano para analise: ").strip())
    except ValueError:
        print("Ano invalido.")
        return
    
    todas_marcas = sorted({c["marca"] for c in carros})
    marcas_com_ano = sorted({c["marca"] for c in carros if c["ano"] == ano})
    marcas_sem_ano = [m for m in todas_marcas if m not in marcas_com_ano]
    
    print(f"\nMarcas com modelos de {ano}")
    if marcas_com_ano:
        for marca in marcas_com_ano:
            print(f"- {marca}")
    else:
        print("Nenhuma marca possui modelos desse ano.")
    
    print(f"\nMarcas sem modelos de {ano}")
    if marcas_sem_ano:
        for marca in marcas_sem_ano:
            print(f"- {marca}")
    else:
        print("Todas as marcas possuem modelos desse ano.")


# Gráficos
def grafico_pizza_marcas(carros):
    contagem = {}
    for carro in carros:
        marca = carro["marca"]
        contagem[marca] = contagem.get(marca, 0) + 1
    
    marcas = list(contagem.keys())
    valores = list(contagem.values())
    
    plt.figure(figsize=(11, 11))
    plt.pie(valores, labels=marcas, autopct="%1.1f%%", startangle=90)
    plt.title("Numero de modelos por marca")
    plt.tight_layout()
    plt.savefig("modelos_por_marca_pizza.png", dpi=150)
    plt.show()


def grafico_barras_preco(carros):
    faixas = {
        "Ate 100k": 0,
        "100k-300k": 0,
        "300k-1M": 0,
        "Acima de 1M": 0,
    }
    
    for carro in carros:
        preco = carro["preco"]
        if preco <= 100_000:
            faixas["Ate 100k"] += 1
        elif preco <= 300_000:
            faixas["100k-300k"] += 1
        elif preco <= 1_000_000:
            faixas["300k-1M"] += 1
        else:
            faixas["Acima de 1M"] += 1
    
    labels = list(faixas.keys())
    valores = list(faixas.values())
    
    plt.figure(figsize=(10, 6))
    barras = plt.bar(labels, valores, color=["#264653", "#2a9d8f", "#e9c46a", "#e76f51"])
    plt.title("Numero de modelos por faixa de preco")
    plt.ylabel("Quantidade de modelos")
    plt.xticks(rotation=15)
    plt.bar_label(barras)
    plt.tight_layout()
    plt.savefig("modelos_por_faixa_preco_colunas.png", dpi=150)
    plt.show()


def grafico_linha_ano(carros):
    contagem = {}
    for carro in carros:
        if carro["ano"] is not None:
            ano = carro["ano"]
            contagem[ano] = contagem.get(ano, 0) + 1
    
    anos = sorted(contagem.keys())
    valores = [contagem[a] for a in anos]
    
    plt.figure(figsize=(10, 6))
    plt.plot(anos, valores, marker="o", linewidth=2)
    plt.title("Numero de modelos por ano")
    plt.xlabel("Ano")
    plt.ylabel("Quantidade de modelos")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("modelos_por_ano_linhas.png", dpi=150)
    plt.show()
