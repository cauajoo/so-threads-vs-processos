import queue
import threading

from comum import blocos, fundir, novo_acc, processar_bloco


# Processa blocos da fila em uma thread
def worker_thread(fila, idx, global_acc, lock):
    local = novo_acc()
    while (b := fila.get()) is not None:
        processar_bloco(b, idx, local)
    with lock:
        fundir(global_acc, local)


# Roda a versão com threading
def rodar_threads(caminho, n):
    idx, gen = blocos(caminho)
    fila = queue.Queue(maxsize=n * 2)
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
