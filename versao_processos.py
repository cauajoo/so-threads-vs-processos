"""Versão Processos: memória isolada; filhos devolvem o resultado por Queue."""
import multiprocessing as mp

from comum import blocos, fundir, novo_acc, processar_bloco


def worker_proc(fila, resultados, idx):
    local = novo_acc()
    while (b := fila.get()) is not None:
        processar_bloco(b, idx, local)
    resultados.put(local)


def rodar_processos(caminho, n):
    idx, gen = blocos(caminho)
    fila, resultados = mp.Queue(maxsize=n * 2), mp.Queue()
    ps = [mp.Process(target=worker_proc, args=(fila, resultados, idx)) for _ in range(n)]
    for p in ps:
        p.start()
    for b in gen:
        fila.put(b)
    for _ in ps:
        fila.put(None)
    acc = novo_acc()
    for _ in ps:  # get() ANTES do join(), senão há deadlock com resultados grandes
        fundir(acc, resultados.get())
    for p in ps:
        p.join()
    return acc
