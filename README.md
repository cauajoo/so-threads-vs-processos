# Threads vs Processos (Python)

> **P3 · 2026.2** · Sistemas Operacionais (AV2)

Lê os CSVs de votação do TSE em blocos (Map-Reduce) e compara o tempo de execução entre
**multithreading** e **multiprocessing**. Considera apenas os votos de **São Paulo capital**.

Calcula a média geral de votos e o partido e o cargo com maior participação (%) no total, e mostra um
mini dashboard no terminal.

## Como executar
1. Baixe `votacao_candidato_munzona_2026.zip` no [portal de dados abertos do TSE](https://dadosabertos.tse.jus.br/)
   e extraia os arquivos `_BR.csv` (presidente) e `_SP.csv` para esta pasta. Eles não estão no repositório por causa do tamanho.
2. Rode:
```bash
python main.py
```
Opcional: `python main.py caminho.csv 8` (um arquivo e o número de workers).

## Estrutura
| Arquivo | Conteúdo |
|---|---|
| `main.py` | Ponto de entrada: roda as duas versões, mede com `perf_counter` e compara |
| `versao_threads.py` | Versão com `threading.Thread` e `Lock` |
| `versao_processos.py` | Versão com `multiprocessing.Process` e `Queue` |
| `comum.py` | Leitura em blocos, limpeza dos dados e fusão dos resultados |
| `dashboard.py` | Mini dashboard em texto (tempos e rankings) |

## Conceitos praticados
Concorrência, threads vs processos, GIL, filas, sincronização com `Lock` e Map-Reduce.
