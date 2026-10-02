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

    resumo.append(
        (
            nome_equipamento,
            quantidade,
            horas,
            round(consumo, 2)
        )
    )

    print(
        "Consumo de",
        nome_equipamento,
        ":",
        round(consumo, 2),
        "kWh/mês"
    )

    continuar = input("Adicionar outro equipamento? (s/n): ")

custo_total = consumo_total * valor_kwh

consumo_referencia = consumo_total

print("\n===== DIMENSIONAMENTO FOTOVOLTAICO =====")

percentual_atendimento = float(
    input(
        "Qual percentual do consumo deseja atender "
        "com energia solar? (%): "
    )
)

while percentual_atendimento <= 0 or percentual_atendimento > 100:
    print(
        "Percentual inválido. "
        "Digite um valor entre 1 e 100."
    )

    percentual_atendimento = float(
        input(
            "Qual percentual do consumo deseja atender "
            "com energia solar? (%): "
        )
    )

fracao_atendimento = percentual_atendimento / 100

energia_fv = consumo_referencia * fracao_atendimento

hsp = float(
    input(
        "Digite as Horas de Sol Pleno (HSP) "
        "médias da localização: "
    )
)

while hsp <= 0:
    print("HSP inválida. Digite um valor maior que zero.")

    hsp = float(
        input(
            "Digite as Horas de Sol Pleno (HSP) "
            "médias da localização: "
        )
    )

dias = 30
eficiencia_global = 0.80

potencia_fv = energia_fv / (
    hsp * dias * eficiencia_global
)

# T33 / T34 / T35
# SELEÇÃO AUTOMÁTICA DO MÓDULO FOTOVOLTAICO

modulos = []

with open(
    "dados/modulos.csv",
    encoding="utf-8-sig"
) as arquivo:

    leitor = csv.DictReader(
        arquivo,
        delimiter=";"
    )

    for linha in leitor:

        modulo = {
            "id": linha["id"],
            "fabricante": linha["fabricante"],
            "modelo": linha["modelo"],
            "potencia_wp": float(
                linha["potencia_wp"]
            ),
            "voc_v": float(
                linha["voc_v"]
            ),
            "isc_a": float(
                linha["isc_a"]
            ),
            "vmp_v": float(
                linha["vmp_v"]
            ),
            "imp_a": float(
                linha["imp_a"]
            ),
            "preco_brl": float(
                linha["preco_brl"]
            )
        }

        modulos.append(modulo)

melhor_modulo = None
menor_custo = None

for modulo in modulos:

    quantidade_modulos = math.ceil(
        (potencia_fv * 1000)
        / modulo["potencia_wp"]
    )

    potencia_instalada = (
        quantidade_modulos
        * modulo["potencia_wp"]
    ) / 1000

    custo_modulos = (
        quantidade_modulos
        * modulo["preco_brl"]
    )

    if (
        menor_custo is None
        or custo_modulos < menor_custo
    ):

        menor_custo = custo_modulos

        melhor_modulo = {
            "id": modulo["id"],
            "fabricante": modulo["fabricante"],
            "modelo": modulo["modelo"],
            "potencia_wp": modulo["potencia_wp"],
            "voc_v": modulo["voc_v"],
            "isc_a": modulo["isc_a"],
            "vmp_v": modulo["vmp_v"],
            "imp_a": modulo["imp_a"],
            "quantidade": quantidade_modulos,
            "potencia_instalada": potencia_instalada,
            "custo_total": custo_modulos
        }

# T36 / T37
# SELEÇÃO E VALIDAÇÃO DO INVERSOR

inversores = []

with open(
    "dados/inversores.csv",
    encoding="utf-8-sig"
) as arquivo:

    leitor = csv.DictReader(
        arquivo,
        delimiter=";"
    )

    for linha in leitor:

        inversor = {
            "id": linha["id"],
            "fabricante": linha["fabricante"],
            "modelo": linha["modelo"],
            "tipo": linha["tipo"],
            "potencia_nominal_w": float(
                linha["potencia_nominal_w"]
            ),
            "potencia_max_fv_w": float(
                linha["potencia_max_fv_w"]
            ),
            "tensao_max_entrada_v": float(
                linha["tensao_max_entrada_v"]
            ),
            "faixa_mppt_min_v": float(
                linha["faixa_mppt_min_v"]
            ),
            "faixa_mppt_max_v": float(
                linha["faixa_mppt_max_v"]
            ),
            "corrente_max_entrada_a": float(
                linha["corrente_max_entrada_a"]
            ),
            "numero_mppt": int(
                linha["numero_mppt"]
            ),
            "compativel_bateria":
                linha["compativel_bateria"],
            "preco_brl": float(
                linha["preco_brl"]
            )
        }

        inversores.append(inversor)

quantidade_string = melhor_modulo["quantidade"]

voc_string = (
    melhor_modulo["voc_v"]
    * quantidade_string
)

vmp_string = (
    melhor_modulo["vmp_v"]
    * quantidade_string
)

isc_string = melhor_modulo["isc_a"]

imp_string = melhor_modulo["imp_a"]

potencia_instalada_w = (
    melhor_modulo["potencia_instalada"]
    * 1000
)

inversores_compativeis = []

for inversor in inversores:

    potencia_ok = (
        potencia_instalada_w
        <= inversor["potencia_max_fv_w"]
    )

    tensao_max_ok = (
        voc_string
        <= inversor["tensao_max_entrada_v"]
    )

    mppt_ok = (
        inversor["faixa_mppt_min_v"]
        <= vmp_string
        <= inversor["faixa_mppt_max_v"]
    )

    corrente_ok = (
        isc_string
        <= inversor["corrente_max_entrada_a"]
    )

    if (
        potencia_ok
        and tensao_max_ok
        and mppt_ok
        and corrente_ok
    ):

        inversores_compativeis.append(
            inversor
        )

melhor_inversor = None

if len(inversores_compativeis) > 0:

    melhor_inversor = min(
        inversores_compativeis,
        key=lambda inversor:
            inversor["preco_brl"]
    )

# T38 / T39
# OPÇÃO DE ARMAZENAMENTO E CÁLCULO DE AUTONOMIA

usar_bateria = input(
    "\nDeseja incluir sistema de armazenamento por bateria? (s/n): "
).strip().lower()

while usar_bateria not in ["s", "n"]:
    print("Opção inválida. Digite s para sim ou n para não.")

    usar_bateria = input(
        "Deseja incluir sistema de armazenamento por bateria? (s/n): "
    ).strip().lower()

tem_bateria = usar_bateria == "s"

horas_autonomia = 0
consumo_diario = 0
energia_autonomia = 0

if tem_bateria:

    horas_autonomia = float(
        input(
            "Quantas horas de autonomia deseja para as baterias? "
        )
    )

    while horas_autonomia <= 0 or horas_autonomia > 24:
        print(
            "Autonomia inválida. "
            "Digite um valor maior que 0 e de no máximo 24 horas."
        )

        horas_autonomia = float(
            input(
                "Quantas horas de autonomia deseja para as baterias? "
            )
        )

    consumo_diario = consumo_referencia / 30

    energia_autonomia = (
        consumo_diario
        * (horas_autonomia / 24)
    )

# T40
# SELEÇÃO AUTOMÁTICA DAS BATERIAS

melhor_bateria = None
eficiencia_bateria = 0.90

if tem_bateria:

    baterias = []

    with open(
        "dados/baterias.csv",
        encoding="utf-8-sig"
    ) as arquivo:

        leitor = csv.DictReader(
            arquivo,
            delimiter=";"
        )

        for linha in leitor:

            bateria = {
                "id": linha["id"],
                "fabricante": linha["fabricante"],
                "modelo": linha["modelo"],
                "tecnologia": linha["tecnologia"],
                "tensao_nominal_v": float(
                    linha["tensao_nominal_v"]
                ),
                "capacidade_ah": float(
                    linha["capacidade_ah"]
                ),
                "capacidade_kwh": float(
                    linha["capacidade_kwh"]
                ),
                "dod_pct": float(
                    linha["dod_pct"]
                ),
                "ciclos": int(
                    linha["ciclos"]
                ),
                "preco_brl": float(
                    linha["preco_brl"]
                )
            }

            baterias.append(bateria)

    menor_custo_baterias = None

    for bateria in baterias:

        dod = bateria["dod_pct"] / 100

        capacidade_util_unidade = (
            bateria["capacidade_kwh"]
            * dod
        )

        energia_corrigida = (
            energia_autonomia
            / eficiencia_bateria
        )

        quantidade_baterias = math.ceil(
            energia_corrigida
            / capacidade_util_unidade
        )

        capacidade_instalada = (
            quantidade_baterias
            * bateria["capacidade_kwh"]
        )

        capacidade_util_instalada = (
            quantidade_baterias
            * capacidade_util_unidade
        )

        custo_baterias = (
            quantidade_baterias
            * bateria["preco_brl"]
        )

        if (
            menor_custo_baterias is None
            or custo_baterias < menor_custo_baterias
        ):

            menor_custo_baterias = custo_baterias

            melhor_bateria = {
                "id": bateria["id"],
                "fabricante": bateria["fabricante"],
                "modelo": bateria["modelo"],
                "tecnologia": bateria["tecnologia"],
                "tensao_nominal_v":
                    bateria["tensao_nominal_v"],
                "capacidade_kwh":
                    bateria["capacidade_kwh"],
                "dod_pct":
                    bateria["dod_pct"],
                "ciclos":
                    bateria["ciclos"],
                "quantidade":
                    quantidade_baterias,
                "capacidade_instalada":
                    capacidade_instalada,
                "capacidade_util_instalada":
                    capacidade_util_instalada,
                "custo_total":
                    custo_baterias
            }

# T41
# VALIDAÇÃO DA ARQUITETURA COM BATERIA

if tem_bateria:

    melhor_combinacao = None
    menor_custo_combinacao = None

    for modulo in modulos:

        quantidade_modulos = math.ceil(
            (potencia_fv * 1000)
            / modulo["potencia_wp"]
        )

        potencia_instalada_teste = (
            quantidade_modulos
            * modulo["potencia_wp"]
        ) / 1000

        potencia_instalada_teste_w = (
            potencia_instalada_teste * 1000
        )

        voc_teste = (
            modulo["voc_v"]
            * quantidade_modulos
        )

        vmp_teste = (
            modulo["vmp_v"]
            * quantidade_modulos
        )

        isc_teste = modulo["isc_a"]

        custo_modulos_teste = (
            quantidade_modulos
            * modulo["preco_brl"]
        )

        for inversor in inversores:

            bateria_ok = (
                inversor["compativel_bateria"]
                .strip()
                .lower()
                == "sim"
            )

            potencia_ok = (
                potencia_instalada_teste_w
                <= inversor["potencia_max_fv_w"]
            )

            tensao_max_ok = (
                voc_teste
                <= inversor["tensao_max_entrada_v"]
            )

            mppt_ok = (
                inversor["faixa_mppt_min_v"]
                <= vmp_teste
                <= inversor["faixa_mppt_max_v"]
            )

            corrente_ok = (
                isc_teste
                <= inversor["corrente_max_entrada_a"]
            )

            if (
                bateria_ok
                and potencia_ok
                and tensao_max_ok
                and mppt_ok
                and corrente_ok
            ):

                custo_combinacao = (
                    custo_modulos_teste
                    + inversor["preco_brl"]
                )

                if (
                    menor_custo_combinacao is None
                    or custo_combinacao
                    < menor_custo_combinacao
                ):

                    menor_custo_combinacao = (
                        custo_combinacao
                    )

                    melhor_combinacao = {
                        "modulo": modulo,
                        "quantidade":
                            quantidade_modulos,
                        "potencia_instalada":
                            potencia_instalada_teste,
                        "custo_modulos":
                            custo_modulos_teste,
                        "inversor":
                            inversor,
                        "voc_string":
                            voc_teste,
                        "vmp_string":
                            vmp_teste,
                        "isc_string":
                            isc_teste
                    }

    if melhor_combinacao is not None:

        modulo_escolhido = (
            melhor_combinacao["modulo"]
        )

        melhor_modulo = {
            "id":
                modulo_escolhido["id"],
            "fabricante":
                modulo_escolhido["fabricante"],
            "modelo":
                modulo_escolhido["modelo"],
            "potencia_wp":
                modulo_escolhido["potencia_wp"],
            "voc_v":
                modulo_escolhido["voc_v"],
            "isc_a":
                modulo_escolhido["isc_a"],
            "vmp_v":
                modulo_escolhido["vmp_v"],
            "imp_a":
                modulo_escolhido["imp_a"],
            "quantidade":
                melhor_combinacao["quantidade"],
            "potencia_instalada":
                melhor_combinacao[
                    "potencia_instalada"
                ],
            "custo_total":
                melhor_combinacao[
                    "custo_modulos"
                ]
        }

        melhor_inversor = (
            melhor_combinacao["inversor"]
        )

        voc_string = (
            melhor_combinacao["voc_string"]
        )

        vmp_string = (
            melhor_combinacao["vmp_string"]
        )

        isc_string = (
            melhor_combinacao["isc_string"]
        )

        imp_string = melhor_modulo["imp_a"]

        potencia_instalada_w = (
            melhor_modulo[
                "potencia_instalada"
            ]
            * 1000
        )

    else:

        melhor_inversor = None

# T42
# CÁLCULO DO ORÇAMENTO DOS EQUIPAMENTOS

custo_modulos_orcamento = melhor_modulo["custo_total"]

custo_inversor_orcamento = 0

if melhor_inversor is not None:
    custo_inversor_orcamento = melhor_inversor["preco_brl"]

custo_baterias_orcamento = 0

if tem_bateria and melhor_bateria is not None:
    custo_baterias_orcamento = melhor_bateria["custo_total"]

custo_total_sistema = (
    custo_modulos_orcamento
    + custo_inversor_orcamento
    + custo_baterias_orcamento
)

# RELATÓRIO FINAL

print("\n===== RELATÓRIO FINAL =====")

print("Nome:", nome)
print("Cidade:", cidade)
print("Área da casa:", area, "m²")
print("Moradores:", moradores)

print("\nEquipamentos cadastrados:")

for item in resumo:

    print(
        "-",
        item[0],
        "| Quantidade:",
        item[1],
        "| Horas/dia:",
        item[2],
        "| Consumo:",
        item[3],
        "kWh/mês"
    )

print(
    "\nConsumo total:",
    round(consumo_total, 2),
    "kWh/mês"
)

print(
    "Valor do kWh: R$",
    valor_kwh
)

print(
    "Custo total estimado: R$",
    round(custo_total, 2)
)

# RESULTADO FOTOVOLTAICO

print(
    "\n===== RESULTADO FOTOVOLTAICO ====="
)

print(
    "Consumo de referência:",
    round(consumo_referencia, 2),
    "kWh/mês"
)

print(
    "Percentual de atendimento:",
    percentual_atendimento,
    "%"
)

print(
    "Energia mensal desejada:",
    round(energia_fv, 2),
    "kWh/mês"
)

print(
    "HSP utilizada:",
    hsp,
    "h/dia"
)

print(
    "Eficiência global:",
    eficiencia_global * 100,
    "%"
)

print(
    "Potência FV necessária:",
    round(potencia_fv, 2),
    "kWp"
)

# MÓDULO SELECIONADO

print(
    "\n===== MÓDULO SELECIONADO ====="
)

print(
    "Fabricante:",
    melhor_modulo["fabricante"]
)

print(
    "Modelo:",
    melhor_modulo["modelo"]
)

print(
    "Potência por módulo:",
    melhor_modulo["potencia_wp"],
    "Wp"
)

print(
    "Quantidade:",
    melhor_modulo["quantidade"]
)

print(
    "Potência instalada:",
    round(
        melhor_modulo["potencia_instalada"],
        2
    ),
    "kWp"
)

print(
    "Potência excedente:",
    round(
        melhor_modulo["potencia_instalada"]
        - potencia_fv,
        2
    ),
    "kWp"
)

print(
    "Custo total dos módulos: R$",
    round(
        melhor_modulo["custo_total"],
        2
    )
)

# INVERSOR SELECIONADO

print(
    "\n===== INVERSOR SELECIONADO ====="
)

if melhor_inversor is not None:

    print(
        "Fabricante:",
        melhor_inversor["fabricante"]
    )

    print(
        "Modelo:",
        melhor_inversor["modelo"]
    )

    print(
        "Tipo:",
        melhor_inversor["tipo"]
    )

    print(
        "Potência nominal:",
        melhor_inversor[
            "potencia_nominal_w"
        ],
        "W"
    )

    print(
        "Potência máxima FV:",
        melhor_inversor[
            "potencia_max_fv_w"
        ],
        "W"
    )

    print(
        "Número de MPPT:",
        melhor_inversor["numero_mppt"]
    )

    print(
        "Compatível com bateria:",
        melhor_inversor[
            "compativel_bateria"
        ]
    )

    print(
        "Preço: R$",
        round(
            melhor_inversor["preco_brl"],
            2
        )
    )

    print(
        "\n===== VALIDAÇÃO TÉCNICA ====="
    )

    print(
        "Potência FV instalada:",
        round(
            potencia_instalada_w,
            2
        ),
        "W"
    )

    print(
        "Voc da string:",
        round(
            voc_string,
            2
        ),
        "V"
    )

    print(
        "Vmp da string:",
        round(
            vmp_string,
            2
        ),
        "V"
    )

    print(
        "Isc da string:",
        round(
            isc_string,
            2
        ),
        "A"
    )

    print(
        "Imp da string:",
        round(
            imp_string,
            2
        ),
        "A"
    )

    print(
        "Status: configuração compatível"
    )

else:

    print(
        "Nenhum inversor do dataset "
        "é compatível com a configuração "
        "dimensionada."
    )

print("\n===== ARMAZENAMENTO POR BATERIA =====")

if tem_bateria:

    print("Armazenamento solicitado: Sim")

    print(
        "Autonomia desejada:",
        horas_autonomia,
        "horas"
    )

    print(
        "Consumo médio diário:",
        round(consumo_diario, 2),
        "kWh/dia"
    )

    print(
        "Energia necessária para autonomia:",
        round(energia_autonomia, 2),
        "kWh"
    )

    print(
        "Eficiência considerada da bateria:",
        eficiencia_bateria * 100,
        "%"
    )

    if melhor_bateria is not None:

        print(
            "\n===== BATERIA SELECIONADA ====="
        )

        print(
            "Fabricante:",
            melhor_bateria["fabricante"]
        )

        print(
            "Modelo:",
            melhor_bateria["modelo"]
        )

        print(
            "Tecnologia:",
            melhor_bateria["tecnologia"]
        )

        print(
            "Capacidade por bateria:",
            melhor_bateria["capacidade_kwh"],
            "kWh"
        )

        print(
            "DoD:",
            melhor_bateria["dod_pct"],
            "%"
        )

        print(
            "Quantidade:",
            melhor_bateria["quantidade"]
        )

        print(
            "Capacidade nominal instalada:",
            round(
                melhor_bateria[
                    "capacidade_instalada"
                ],
                2
            ),
            "kWh"
        )

        print(
            "Capacidade útil instalada:",
            round(
                melhor_bateria[
                    "capacidade_util_instalada"
                ],
                2
            ),
            "kWh"
        )

        print(
            "Custo total das baterias: R$",
            round(
                melhor_bateria["custo_total"],
                2
            )
        )

        if melhor_inversor is not None:

            print(
                "Inversor compatível com sistema de armazenamento: Sim"
            )

        else:

            print(
                "Inversor compatível com sistema de armazenamento: Não"
            )

else:

    print("Armazenamento solicitado: Não")

print("\n===== ORÇAMENTO DO SISTEMA =====")

print(
    "Custo dos módulos: R$",
    round(custo_modulos_orcamento, 2)
)

print(
    "Custo do inversor: R$",
    round(custo_inversor_orcamento, 2)
)

if tem_bateria:

    print(
        "Custo das baterias: R$",
        round(custo_baterias_orcamento, 2)
    )

else:

    print(
        "Custo das baterias: R$ 0.00"
    )

print(
    "Custo total dos equipamentos: R$",
    round(custo_total_sistema, 2)
)

print("\n===== RESUMO FINAL DO DIMENSIONAMENTO =====")

print(
    "Consumo de referência:",
    round(consumo_referencia, 2),
    "kWh/mês"
)

print(
    "Percentual atendido por energia solar:",
    percentual_atendimento,
    "%"
)

print(
    "Geração mensal desejada:",
    round(energia_fv, 2),
    "kWh/mês"
)

print(
    "HSP considerada:",
    hsp,
    "h/dia"
)

print(
    "Potência FV calculada:",
    round(potencia_fv, 2),
    "kWp"
)

print(
    "Potência FV instalada:",
    round(
        melhor_modulo["potencia_instalada"],
        2
    ),
    "kWp"
)

print(
    "Módulos:",
    melhor_modulo["quantidade"],
    "x",
    melhor_modulo["fabricante"],
    melhor_modulo["modelo"],
    "-",
    melhor_modulo["potencia_wp"],
    "Wp"
)

if melhor_inversor is not None:

    print(
        "Inversor:",
        melhor_inversor["fabricante"],
        melhor_inversor["modelo"],
        "-",
        melhor_inversor["potencia_nominal_w"],
        "W"
    )

else:

    print(
        "Inversor: nenhuma opção compatível encontrada"
    )

if tem_bateria and melhor_bateria is not None:

    print("Sistema com bateria: Sim")

    print(
        "Autonomia desejada:",
        horas_autonomia,
        "horas"
    )

    print(
        "Baterias:",
        melhor_bateria["quantidade"],
        "x",
        melhor_bateria["fabricante"],
        melhor_bateria["modelo"]
    )

    print(
        "Capacidade nominal instalada:",
        round(
            melhor_bateria[
                "capacidade_instalada"
            ],
            2
        ),
        "kWh"
    )

    print(
        "Capacidade útil instalada:",
        round(
            melhor_bateria[
                "capacidade_util_instalada"
            ],
            2
        ),
        "kWh"
    )

else:

    print("Sistema com bateria: Não")

print(
    "Custo total dos equipamentos: R$",
    round(custo_total_sistema, 2)
)

