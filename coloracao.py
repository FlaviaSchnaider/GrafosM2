# Coloração de Grafos - M2 (Parte 1)
# Entrada: arquivo texto com grafo não direcionado, não ponderado.
# Saída: número cromático, tempo e (opcionalmente) a coloração.

import argparse
import sys
import time

# Leitura do grafo
def carregar_grafo(arquivo):
    """
    Lê um grafo de um arquivo em vários formatos:
      1) Arestas: "u v"
      2) Cabeçalho "n m" + m arestas
      3) DIMACS: "p edge n m" e linhas "e u v"
    Retorna (n, adj, mapa_original)
    """
    arestas = []
    n_cabecalho = None

    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith('c'):
                continue

            if linha.startswith('p '):
                partes = linha.split()
                if len(partes) >= 4 and partes[2].isdigit():
                    n_cabecalho = int(partes[2])
                continue

            if linha.startswith('e '):
                partes = linha.split()
                if len(partes) >= 3:
                    u, v = partes[1], partes[2]
                else:
                    continue
            else:
                partes = linha.split()
                if len(partes) == 2:
                    a, b = partes
                    if not arestas and n_cabecalho is None:
                        try:
                            n_cabecalho = int(a)
                            continue
                        except ValueError:
                            pass
                    u, v = a, b
                else:
                    continue

            try:
                u, v = int(u), int(v)
            except ValueError:
                continue

            if u != v:
                arestas.append((u, v))

    if not arestas and not n_cabecalho:
        raise ValueError("Nenhuma aresta válida encontrada.")

    vertices = {v for e in arestas for v in e}

    if n_cabecalho:
        menor = min(vertices) if vertices else 1
        base = 0 if menor == 0 else 1
        if base == 0:
            vertices |= set(range(0, n_cabecalho))
        else:
            vertices |= set(range(1, n_cabecalho + 1))

    lista_vertices = sorted(vertices)
    mapa = {v: i for i, v in enumerate(lista_vertices)}
    n = len(lista_vertices)
    adj = [set() for _ in range(n)]

    for u, v in arestas:
        i, j = mapa[u], mapa[v]
        if i != j:
            adj[i].add(j)
            adj[j].add(i)

    return n, adj, mapa


# Algoritmos de coloração
def valido(adj, cores):
    for u in range(len(adj)):
        for v in adj[u]:
            if cores[u] == cores[v]:
                return False
    return True


def cores_usadas(cores):
    return max(cores) + 1 if cores else 0

# Exibir coloração colorida
def mostrar_colorido(cores, mapa, limite=10):
    """Mostra os vértices coloridos no terminal com cores reais"""
    if len(cores) > limite:
        print("(Ocultando coloração colorida, grafo grande)")
        return

    # Paleta de cores ANSI
    paleta = [
        "\033[31m",  # vermelho
        "\033[32m",  # verde
        "\033[33m",  # amarelo
        "\033[34m",  # azul
        "\033[35m",  # magenta
        "\033[36m",  # ciano
        "\033[91m",  # vermelho claro
        "\033[92m",  # verde claro
        "\033[93m",  # amarelo claro
        "\033[94m",  # azul claro
        "\033[95m",  # magenta claro
        "\033[96m",  # ciano claro
    ]
    reset = "\033[0m"

    inv = {v: u for u, v in mapa.items()}
    print("\nVértices coloridos:")
    for i, c in enumerate(cores):
        cor_ansi = paleta[c % len(paleta)]
        print(f"{cor_ansi}{inv[i]} -> cor {c}{reset}")


def guloso(adj):
    n = len(adj)
    cores = [-1] * n
    for v in range(n):
        viz = {cores[w] for w in adj[v] if cores[w] != -1}
        cor = 0
        while cor in viz:
            cor += 1
        cores[v] = cor
    return cores


def welsh_powell(adj):
    n = len(adj)
    ordem = sorted(range(n), key=lambda v: len(adj[v]), reverse=True)
    cores = [-1] * n
    for v in ordem:
        viz = {cores[w] for w in adj[v] if cores[w] != -1}
        cor = 0
        while cor in viz:
            cor += 1
        cores[v] = cor
    return cores


def dsatur(adj):
    n = len(adj)
    cores = [-1] * n
    sat = [0] * n
    grau = [len(adj[v]) for v in range(n)]
    viz_cores = [set() for _ in range(n)]

    v = max(range(n), key=lambda x: grau[x])
    cores[v] = 0
    for w in adj[v]:
        viz_cores[w].add(0)
        sat[w] = len(viz_cores[w])

    for _ in range(n - 1):
        v = max((i for i in range(n) if cores[i] == -1),
                key=lambda x: (sat[x], grau[x]))
        cor = 0
        while cor in viz_cores[v]:
            cor += 1
        cores[v] = cor
        for w in adj[v]:
            if cores[w] == -1:
                viz_cores[w].add(cor)
                sat[w] = len(viz_cores[w])
    return cores


def forca_bruta(adj, limite=12):
    n = len(adj)
    if n > limite:
        raise ValueError(f"Força bruta bloqueada para n>{limite}")

    cores = [-1] * n

    def tenta(v, k):
        if v == n:
            return True
        proibidas = {cores[w] for w in adj[v] if cores[w] != -1}
        for c in range(k):
            if c in proibidas:
                continue
            cores[v] = c
            if tenta(v + 1, k):
                return True
            cores[v] = -1
        return False

    k = 2
    while True:
        cores[:] = [-1] * n
        if tenta(0, k):
            return cores
        k += 1
        if k > n:
            return list(range(n))


# Utilitários
def medir(funcao, *args, **kwargs):
    inicio = time.perf_counter()
    res = funcao(*args, **kwargs)
    fim = time.perf_counter()
    return res, fim - inicio


# Execução principal
def main():
    parser = argparse.ArgumentParser(description="Coloração de Grafos (Parte 1)")
    parser.add_argument("-i", "--input", required=True, help="Arquivo do grafo")
    parser.add_argument("-a", "--algo", choices=["brute", "greedy", "welsh", "dsatur"], required=True)
    parser.add_argument("--verify", action="store_true", help="Verificar se coloração é válida")
    parser.add_argument("--show", action="store_true", help="Mostrar vértice->cor (para n<10)")
    parser.add_argument("--limit", type=int, default=12, help="Limite de vértices para força bruta")
    args = parser.parse_args()

    try:
        n, adj, mapa = carregar_grafo(args.input)
    except Exception as e:
        print("Erro ao ler o grafo:", e, file=sys.stderr)
        sys.exit(1)

    if args.algo == "brute" and n > args.limit:
        print(f"Grafo tem {n} vértices (> {args.limit}). Use heurísticas.", file=sys.stderr)
        sys.exit(2)

    funcoes = {
        "greedy": guloso,
        "welsh": welsh_powell,
        "dsatur": dsatur,
        "brute": lambda a: forca_bruta(a, args.limit),
    }

    cores, tempo = medir(funcoes[args.algo], adj)
    k = cores_usadas(cores)

    print(f"Algoritmo: {args.algo}")
    print(f"Vértices: {n}")
    print(f"Cores usadas: {k}")
    print(f"Tempo: {tempo:.6f}s")

    if args.verify:
        print("Coloração válida:", "sim" if valido(adj, cores) else "não")

    if args.show and n < 10:
        inv = {v: u for u, v in mapa.items()}
        print("Vértice -> Cor")
        for i in range(n):
            print(f"{inv[i]} -> {cores[i]}")
            print()
            mostrar_colorido(cores, mapa)



if __name__ == "__main__":
    main()
