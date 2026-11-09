import glob
import os
import sys
import time

import dashboard
from versao_processos import rodar_processos
from versao_threads import rodar_threads

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVOS = sorted(glob.glob(os.path.join(PASTA, "votacao_candidato_munzona*.csv")))


# Retorna o grupo com maior % dos votos
def melhor(d, total):
    k = max(d, key=lambda k: d[k][0])
    return k, d[k][0] / total * 100


# Executa uma versão e mede o tempo
def medir(nome, fn, caminho, n):
    t0 = time.perf_counter()
    acc = fn(caminho, n)
    dt = time.perf_counter() - t0
    soma, cont = acc["geral"]
    print(f"\n=== {nome} ===")
    print(f"Média geral de votos: {soma / cont:.4f}  ({cont} registros válidos)")
    p, pp = melhor(acc["partido"], soma)
    c, pc = melhor(acc["cargo"], soma)
    print(f"Partido com maior participação: {p} ({pp:.2f}% dos votos)")
    print(f"Cargo com maior participação:   {c} ({pc:.2f}% dos votos)")
    print(f"Tempo: {dt:.4f} s")
    return acc, dt


if __name__ == "__main__":
    caminho = [sys.argv[1]] if len(sys.argv) > 1 else ARQUIVOS
    n = int(sys.argv[2]) if len(sys.argv) > 2 else os.cpu_count() or 4
    if not caminho or not all(os.path.isfile(c) for c in caminho):
        sys.exit(f"Arquivo(s) não encontrado(s): {caminho}")
    print(f"Arquivo: {caminho} | workers: {n}")
    acc, t_thr = medir("THREADS", rodar_threads, caminho, n)
    _, t_proc = medir("PROCESSOS", rodar_processos, caminho, n)
    print("\n=== COMPARAÇÃO ===")
    print(f"Tempo com processos: {t_proc:.4f} s")
    print(f"Tempo com threads:   {t_thr:.4f} s")
    print(f"Melhor desempenho (menor tempo): {'PROCESSOS' if t_proc < t_thr else 'THREADS'}")
    dashboard.mostrar(acc, {"Threads": t_thr, "Processos": t_proc})
