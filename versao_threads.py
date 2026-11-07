"""Versão Threads: workers compartilham memória; a fusão final usa Lock."""
import queue
import threading

from comum import blocos, fundir, novo_acc, processar_bloco


def worker_thread(fila, idx, global_acc, lock):
    local = novo_acc()  # acumula sem lock; só a fusão final é protegida
    while (b := fila.get()) is not None:
        processar_bloco(b, idx, local)
    with lock:
        fundir(global_acc, local)


def rodar_threads(caminho, n):
    idx, gen = blocos(caminho)
    fila = queue.Queue(maxsize=n * 2)  # limita blocos em memória
    acc, lock = novo_acc(), threading.Lock()
    ts = [threading.Thread(target=worker_thread, args=(fila, idx, acc, lock)) for _ in range(n)]
    for t in ts:
        t.start()
    for b in gen:
        fila.put(b)
    for _ in ts:
        fila.put(None)
    for t in ts:
        t.join()
    return acc
