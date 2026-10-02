# Sistema de Dimensionamento Energético Residencial

## Integrantes

- Leonardo Duarte – RM 569029
- João Pedro Conturbia – RM 569788
- Eduardo Oliveira – RM 570374
- Enzo de Nadai – RM 569985

---

## Descrição

Projeto desenvolvido para estimar o consumo de uma residência e realizar o dimensionamento de um sistema fotovoltaico.

O sistema calcula:

- consumo mensal da residência;
- potência fotovoltaica necessária;
- quantidade e seleção de módulos;
- seleção e validação do inversor;
- opção com ou sem bateria;
- autonomia e quantidade de baterias;
- orçamento dos equipamentos;
- resumo final do dimensionamento.

---

## Estrutura do Projeto

```text
/
├── calculadora_consumo.py
├── dados/
│   ├── modulos.csv
│   ├── inversores.csv
│   └── baterias.csv
├── evidencias/
│   ├── cenario_sem_bateria.txt
│   └── cenario_com_bateria.txt
└── README.md
```

---

## Premissas Utilizadas

Para o dimensionamento foram consideradas:

```text
Dias do mês = 30
Eficiência global do sistema FV = 80%
Eficiência da bateria = 90%
```

A potência fotovoltaica é calculada por:

```text
P_FV = Energia FV / (HSP × Dias × Eficiência)
```

A quantidade de módulos é calculada por:

```text
Quantidade = ceil((P_FV × 1000) / Potência do módulo)
```

Para baterias:

```text
Consumo diário = Consumo mensal / 30

Energia para autonomia =
Consumo diário × (Horas de autonomia / 24)
```

---

## Seleção dos Equipamentos

Os equipamentos são selecionados a partir dos arquivos CSV presentes na pasta `dados`.

### Módulos

O sistema calcula a quantidade necessária para cada modelo e seleciona a configuração de menor custo.

### Inversores

São verificadas:

- potência máxima FV;
- tensão máxima de entrada;
- faixa MPPT;
- corrente máxima de entrada.

Entre os inversores compatíveis, é selecionado o de menor custo.

### Baterias

Quando o usuário solicita armazenamento, o sistema calcula a energia necessária para a autonomia e seleciona a configuração de baterias de menor custo.

Também é considerado se o inversor é compatível com sistema de armazenamento.

---

## Orçamento

O orçamento considera:

- módulos fotovoltaicos;
- inversor;
- baterias, quando utilizadas.

Não são considerados custos de instalação, estrutura, cabeamento ou mão de obra.

---

## Cenários de Teste

Foram realizados dois cenários de validação.

### Sem bateria

```text
Consumo: 450 kWh/mês
Percentual atendido: 100%
HSP: 4,5 h/dia

Módulos:
8 x Canadian Solar CS6W-550MS

Potência instalada:
4,40 kWp

Inversor:
SAJ R5-6K-S2-15

Custo total:
R$ 5.719,20
```

### Com bateria

```text
Consumo: 450 kWh/mês
Percentual atendido: 100%
HSP: 4,5 h/dia
Autonomia: 8 horas

Módulos:
9 x Trina Solar TSM-510DE18M(II)

Potência instalada:
4,59 kWp

Inversor:
Deye SUN-5K-SG01LP1-US

Baterias:
2 x Pylontech US5000

Capacidade instalada:
9,60 kWh

Custo total:
R$ 32.860,00
```

As evidências completas estão disponíveis na pasta:

```text
evidencias/
```

---

## Como Executar

No terminal:

```bash
python calculadora_consumo.py
```

Ao final, o sistema apresenta o resumo do dimensionamento e salva automaticamente a evidência em TXT:

```text
evidencias/cenario_sem_bateria.txt
```

ou

```text
evidencias/cenario_com_bateria.txt
```
<<<<<<< HEAD
=======
