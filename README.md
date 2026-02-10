# Flight Link Generator (LATAM & Azul)

Ferramenta em Python para gerar links de busca de voos para LATAM e Azul usando os códigos IATA informados.

## Como usar

```bash
python flight_links.py
```

Ou importe no seu projeto:

```python
from flight_links import generateFlightLinks

resultados = generateFlightLinks(
    origins=["JPA", "REC", "NAT", "MCZ"],
    destination="FOR",
    outbound_date="2024-10-15",
    inbound_date="2024-10-21",
    adults=1,
)
```

## Interface gráfica (Tkinter)

No Zorin 18 (ou outras distros com Tkinter instalado), execute:

```bash
python gui_app.py
```

A interface permite inserir origens/destino, datas e adultos, inverter origem/destino ou datas, visualizar a resposta organizada em tabela com índice e abrir os links por botões, além de exportar em JSON/CSV/Excel.

### Instalação no Zorin 18

1. Instale Python e Tkinter:

```bash
sudo apt update
sudo apt install -y python3 python3-tk
```

2. (Opcional) Se quiser exportar para Excel, instale o pandas:

```bash
python3 -m pip install pandas
```

3. Execute a interface:

```bash
python3 gui_app.py
```

## Exportações

```python
from pathlib import Path
from flight_links import generate_flight_links, export_json, export_csv

links = generate_flight_links(
    origins=["JPA", "REC"],
    destination="FOR",
    outbound_date="2024-10-15",
    inbound_date="2024-10-21",
)

export_json(links, Path("links.json"))
export_csv(links, Path("links.csv"))
```

## Validação de IATA (opcional)

Por padrão, o gerador usa exatamente os códigos informados (sem validação). Caso queira validar com uma lista local ou API, habilite `validate_iata=True`:

```python
links = generate_flight_links(
    origins=["JPA"],
    destination="FOR",
    outbound_date="2024-10-15",
    inbound_date="2024-10-21",
    validate_iata=True,
)
```
