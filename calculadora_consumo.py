import csv
import math

nome = input("Digite seu nome: ")
cidade = input("Digite sua cidade: ")
area = input("Quantos m² tem sua casa? ")
moradores = int(input("Quantas pessoas moram na casa? "))
valor_kwh = float(input("Digite o valor do kWh: R$ "))

equipamentos = {
    1: ("Geladeira", "Cozinha", 150),
    2: ("Chuveiro Elétrico", "Banheiro", 5500),
    3: ("TV", "Sala", 100),
    4: ("Ar-condicionado", "Quarto", 900),
    5: ("Computador", "Escritório", 200),
    6: ("Lâmpada LED", "Iluminação", 9),
    7: ("Máquina de Lavar", "Lavanderia", 500),
    8: ("Micro-ondas", "Cozinha", 1200)
}

print("\nEquipamentos disponíveis:")

for codigo in equipamentos:
    print(codigo, equipamentos[codigo][0], equipamentos[codigo][2])

consumo_total = 0
continuar = "s"
resumo = []

while continuar == "s":

    codigo = int(input("\nDigite o código do equipamento: "))

    while codigo not in equipamentos:
        print("Código inválido. Escolha um dos códigos da lista acima.")
        codigo = int(input("Digite o código do equipamento: "))

    nome_equipamento = equipamentos[codigo][0]
    potencia = equipamentos[codigo][2]

    quantidade = int(input("Quantidade: "))

    while quantidade <= 0:
        print("Quantidade inválida. Digite um número maior que zero.")
        quantidade = int(input("Quantidade: "))

    horas = float(input("Horas de uso por dia: "))

    while horas <= 0 or horas > 24:
        print("Horas inválidas. Digite um valor entre 0 e 24.")
        horas = float(input("Horas de uso por dia: "))

    consumo = potencia * quantidade * horas * 30 / 1000

    consumo_total = consumo_total + consumo

    resumo.append((nome_equipamento, quantidade, horas, round(consumo, 2)))

    print("Consumo de", nome_equipamento, ":", round(consumo, 2), "kWh/mês")

    continuar = input("Adicionar outro equipamento? (s/n): ")

custo_total = consumo_total * valor_kwh

consumo_referencia = consumo_total

print("\n===== DIMENSIONAMENTO FOTOVOLTAICO =====")

percentual_atendimento = float(
    input("Qual percentual do consumo deseja atender com energia solar? (%): ")
)

while percentual_atendimento <= 0 or percentual_atendimento > 100:
    print("Percentual inválido. Digite um valor entre 1 e 100.")
    percentual_atendimento = float(
        input("Qual percentual do consumo deseja atender com energia solar? (%): ")
    )

fracao_atendimento = percentual_atendimento / 100

energia_fv = consumo_referencia * fracao_atendimento

hsp = float(
    input("Digite as Horas de Sol Pleno (HSP) médias da localização: ")
)

while hsp <= 0:
    print("HSP inválida. Digite um valor maior que zero.")
    hsp = float(
        input("Digite as Horas de Sol Pleno (HSP) médias da localização: ")
    )

dias = 30
eficiencia_global = 0.80

potencia_fv = energia_fv / (hsp * dias * eficiencia_global)

# Seleção automática do módulo fotovoltaico

modulos = []

with open("dados/modulos.csv", encoding="utf-8-sig") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=";")

    for linha in leitor:
        modulo = {
            "id": linha["id"],
            "fabricante": linha["fabricante"],
            "modelo": linha["modelo"],
            "potencia_wp": float(linha["potencia_wp"]),
            "preco_brl": float(linha["preco_brl"])
        }

        modulos.append(modulo)

melhor_modulo = None
menor_custo = None

for modulo in modulos:

    quantidade_modulos = math.ceil(
        (potencia_fv * 1000) / modulo["potencia_wp"]
    )

    potencia_instalada = (
        quantidade_modulos * modulo["potencia_wp"]
    ) / 1000

    custo_modulos = (
        quantidade_modulos * modulo["preco_brl"]
    )

    if menor_custo is None or custo_modulos < menor_custo:

        menor_custo = custo_modulos

        melhor_modulo = {
            "id": modulo["id"],
            "fabricante": modulo["fabricante"],
            "modelo": modulo["modelo"],
            "potencia_wp": modulo["potencia_wp"],
            "quantidade": quantidade_modulos,
            "potencia_instalada": potencia_instalada,
            "custo_total": custo_modulos
        }

print("\n===== RELATÓRIO FINAL =====")
print("Nome:", nome)
print("Cidade:", cidade)
print("Área da casa:", area, "m²")
print("Moradores:", moradores)

print("\nEquipamentos cadastrados:")
for item in resumo:
    print(
        "-", item[0],
        "| Quantidade:", item[1],
        "| Horas/dia:", item[2],
        "| Consumo:", item[3], "kWh/mês"
    )

print("Consumo de referência:", round(consumo_referencia, 2), "kWh/mês")
print("Valor do kWh: R$", valor_kwh)
print("Custo total estimado: R$", round(custo_total, 2))

print("\n===== RESULTADO FOTOVOLTAICO =====")
print("Consumo de referência:", round(consumo_referencia, 2), "kWh/mês")
print("Percentual de atendimento:", percentual_atendimento, "%")
print("Energia mensal desejada:", round(energia_fv, 2), "kWh/mês")
print("HSP utilizada:", hsp, "h/dia")
print("Eficiência global:", eficiencia_global * 100, "%")
print("Potência FV necessária:", round(potencia_fv, 2), "kWp")

print("\n===== MÓDULO SELECIONADO =====")
print("Fabricante:", melhor_modulo["fabricante"])
print("Modelo:", melhor_modulo["modelo"])
print("Potência por módulo:", melhor_modulo["potencia_wp"], "Wp")
print("Quantidade:", melhor_modulo["quantidade"])
print(
    "Potência instalada:",
    round(melhor_modulo["potencia_instalada"], 2),
    "kWp"
)
print(
    "Custo total dos módulos: R$",
    round(melhor_modulo["custo_total"], 2)
)