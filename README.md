# Análise de Grafos — M2
Implementação em Python para análise e coloração de grafos, incluindo também a geração de árvores geradoras mínimas (MST) com os algoritmos Prim e Kruskal.


## Execução dos Algoritmos
### Formato Geral
python coloracao.py --input <arquivo.txt> --algo <algoritmo> [opções]


## Algoritmos de Coloração

#### DSATUR
python coloracao.py --input grafos/grafo1.txt --algo dsatur --verify --show


#### Welsh–Powell
python coloracao.py --input grafos/grafo1.txt --algo welsh --verify

#### Greedy
python coloracao.py --input grafos/grafo1.txt --algo greedy --show


#### Força Bruta (Exata)
python coloracao.py -i grafos/grafo_pequeno.txt --algo brute --limit 12 --verify --show


## Comparação de Algoritmos
### Comparar Todos os de Coloração
python coloracao.py --input grafos/grafo1.txt --compare


### Comparar MST (Prim x Kruskal)
python coloracao.py --input grafos/grafo1.txt --mst --show


exibe uma tabela de comparação com:
- Soma das arestas
- Tempo de execução
- Arestas da MST


## Exportar Resultado
Salva o mapeamento vértice -> cor em CSV:
python coloracao.py -i grafos/grafo1.txt --algo dsatur --output resultado.csv