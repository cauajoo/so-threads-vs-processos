"""Funções compartilhadas: leitura em blocos, limpeza (Map) e fusão (Reduce)."""
import csv
from itertools import islice

CHUNK = 50_000  # linhas por bloco
INVALIDOS = {"#NULO", "-1", "#NE", "-3"}
COLUNAS = ("QT_VOTOS_NOMINAIS_VALIDOS", "SG_PARTIDO", "DS_CARGO", "NM_MUNICIPIO")
MUNICIPIO = "SÃO PAULO"  # apenas a capital


def novo_acc():
    """Acumulador: [soma, contagem] geral, e dicts partido/cargo -> [soma, contagem]."""
    return {"geral": [0, 0], "partido": {}, "cargo": {}}


def processar_bloco(linhas, idx, acc):
    """Map: limpa as linhas do bloco e atualiza o acumulador `acc`."""
    iv, ip, ic, im = idx
    for l in linhas:
        try:
            v, p, c = l[iv].strip(), l[ip].strip(), l[ic].strip()
            if l[im].strip().upper() != MUNICIPIO:
                continue
        except IndexError:
            continue
        if v in INVALIDOS or p in INVALIDOS or c in INVALIDOS:
            continue
        try:
            v = int(v)
        except ValueError:
            continue
        acc["geral"][0] += v
        acc["geral"][1] += 1
        for chave, k in (("partido", p), ("cargo", c)):
            s = acc[chave].setdefault(k, [0, 0])
            s[0] += v
            s[1] += 1


def fundir(destino, origem):
    """Reduce: soma o acumulador `origem` em `destino`."""
    destino["geral"][0] += origem["geral"][0]
    destino["geral"][1] += origem["geral"][1]
    for chave in ("partido", "cargo"):
        for k, (s, n) in origem[chave].items():
            d = destino[chave].setdefault(k, [0, 0])
            d[0] += s
            d[1] += n


def blocos(caminhos):
    """Retorna (índices das colunas, gerador de blocos) lendo os CSVs aos pedaços.

    shortcut: usa os índices do 1º arquivo para todos; vale p/ os CSVs munzona do TSE (mesmo layout).
    """
    with open(caminhos[0], encoding="latin-1", newline="") as f:
        cab = next(csv.reader(f, delimiter=";"))
    faltam = [c for c in COLUNAS if c not in cab]
    if faltam:
        raise SystemExit(f"CSV sem as colunas {faltam}. Use o arquivo 'votacao_candidato_munzona'.")
    idx = tuple(cab.index(c) for c in COLUNAS)

    def gen():
        for caminho in caminhos:
            with open(caminho, encoding="latin-1", newline="") as f:
                leitor = csv.reader(f, delimiter=";")
                next(leitor)
                while b := list(islice(leitor, CHUNK)):
                    yield b

    return idx, gen()
