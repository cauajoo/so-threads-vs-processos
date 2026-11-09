# Desenha um gráfico de barras no terminal
def _barras(titulo, itens, fmt, largura=40):
    print(f"\n{titulo}")
    mx = max(v for _, v in itens) or 1
    for nome, v in itens:
        print(f"  {nome[:22]:<22} {'█' * max(1, round(v / mx * largura)):<{largura}} {fmt(v)}")


# Mostra o dashboard com tempos e rankings
def mostrar(acc, tempos):
    soma, cont = acc["geral"]
    print("\n" + "=" * 70 + "\n  DASHBOARD - VOTOS TSE\n" + "=" * 70)
    print(f"  Registros válidos: {cont}   Média geral: {soma / cont:.4f}")
    _barras("Tempo de execução (menor = melhor)", list(tempos.items()), lambda v: f"{v:.2f} s")
    for chave, nome in (("partido", "Top 5 partidos"), ("cargo", "Top 5 cargos")):
        top = sorted(((k, s / soma * 100) for k, (s, n) in acc[chave].items()), key=lambda x: -x[1])[:5]
        _barras(f"{nome} por % do total de votos", top, lambda v: f"{v:.2f}%")
    venc = min(tempos, key=tempos.get)
    print(f"\n  >>> Melhor desempenho: {venc.upper()} ({tempos[venc]:.2f} s)\n")
