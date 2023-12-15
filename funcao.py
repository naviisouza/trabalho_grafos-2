import time

import networkx as nx

import menu as m


def voltar(G, direcao):

    input("\nPressione ENTER para retornar ao menu.")

    m.menu(G, direcao)


def criarGrafo(numVertices, direcao):
    if direcao == 1:
        G = nx.Graph()
        for x in range(1, numVertices + 1):
            G.add_node(input("\nDigite o rótulo do vétice " + str(x) + ": "),
                       weight=float(input("Digite o peso do vértice " + str(x) + ": ")))

    elif direcao == 2:
        G = nx.DiGraph()
        for x in range(1, numVertices + 1):
            G.add_node(input("\nDigite o rótulo do vétice " + str(x) + ": "),
                       weight=float(input("Digite o peso do vértice " + str(x) + ": ")))
    return G


def lerArquivo(caminho):
    G = nx.read_gml(caminho)
    return G


def criarArestas(G, direcao):
    v1 = input("\nDigite o rótulo do primeiro vértice da aresta: ")
    v2 = input("Digite o rótulo do segundo vértice da aresta: ")
    peso = float(input("Digite o peso da aresta: "))

    G.add_edge(v1, v2, weight=peso)

    valor = int(
        input("\nDigite 1 para criar uma nova aresta ou 2 para retornar ao menu: "))

    if valor == 1:
        criarArestas(G, direcao)

    voltar(G, direcao)


def removerArestas(G, direcao):
    v1 = input("\nDigite o rótulo do primeiro vértice da aresta: ")
    v2 = input("Digite o rótulo do segundo vértice da aresta: ")

    G.remove_edge(v1, v2)

    valor = int(
        input("\nDigite 1 para remover outra aresta ou 2 para retornar ao menu: "))

    if valor == 1:
        removerArestas(G, direcao)

    voltar(G, direcao)


def rotularArestas(G, direcao):
    v1 = input("\nDigite o rótulo do primeiro vértice da aresta: ")
    v2 = input("Digite o rótulo do segundo vértice da aresta: ")
    rotulo = input("Digite um rótulo para a aresta: ")
    aresta = [v1, v2]

    nx.set_edge_attributes(G, aresta, rotulo)

    print("\nO rótulo " + rotulo + " foi adicionado à aresta " + v1 + v2 + ".")

    voltar(G, direcao)


def adjacenciaVertices(G, direcao):
    v = input("\nDigite o rótulo de um dos vértices existentes: ")

    print("\nVértices adjacentes: ")
    print([n for n in G.neighbors(v)])

    voltar(G, direcao)


def adjacenciaArestas(G, direcao):
    v1 = input("\nDigite o rótulo do primeiro vértice da aresta: ")
    v2 = input("Digite o rótulo do segundo vértice da aresta: ")

    arestas = list(G.edges)

    print("\nArestas adjacentes: ")

    for i in range(len(arestas)):
        if arestas[i] == (v1, v2):
            pass

        elif v1 in arestas[i]:
            print(arestas[i])

        elif v2 in arestas[i]:
            print(arestas[i])

        else:
            pass

    voltar(G, direcao)


def existenciaArestas(G, direcao):
    v1 = input("\nDigite o rótulo do primeiro vértice da aresta: ")
    v2 = input("Digite o rótulo do segundo vértice da aresta: ")

    if G.has_edge(v1, v2) is True:
        print("\nExiste.")

    else:
        print("\nNão existe.")

    voltar(G, direcao)


def vazioOuCompleto(G, direcao):
    arestas = G.number_of_edges()
    vertices = G.number_of_nodes()

    if arestas == 0:
        print("\nO grafo é vazio.")

    elif arestas == (vertices * (vertices - 1))/2:
        print("\nO grafo é completo.")

    else:
        print("\nO grafo não é vazio e também não é completo.")

    voltar(G, direcao)


def matrizAdjacencia(G, direcao):
    print("\nMatriz de adjacência: ")

    A = nx.to_scipy_sparse_array(G)

    print(A.todense())

    voltar(G, direcao)


def listaAdjacencia(G, direcao):
    print("\nLista de adjacência: ")

    for line in nx.generate_adjlist(G):
        print(line)

    voltar(G, direcao)


def gerarArquivo(G, direcao):
    nx.write_gml(G, "grafo.gml")
    print("\nO arquivo foi salvo na mesma pasta do código fonte.")
  
    voltar(G, direcao)


def quantidades(G, direcao):
    print("\nNúmero de arestas: ")
    print(G.number_of_edges())

    print("Número de vértices: ")
    print(G.number_of_nodes())

    voltar(G, direcao)


def naive(G, direcao, op, v1, v2):
    if op is True:
        dfs_original = len(list(nx.dfs_edges(G)))
        G.remove_edge(v1, v2)
        dfs_result = len(list(nx.dfs_edges(G)))
        G.add_edge(v1, v2, weight=1)
        if dfs_result != dfs_original:
            return True
        else:
            return False
    else:
        pontes = []
        arestas = list(G.edges())
        dfs_original = len(list(nx.dfs_edges(G)))
        for v1, v2 in arestas:
            G.remove_edge(v1, v2)
            dfs_result = len(list(nx.dfs_edges(G)))
            if dfs_result != dfs_original:
                pontes.append((v1, v2))
            G.add_edge(v1, v2)
        print("\n%d Pontes achadas" % len(pontes))
        for v1, v2 in pontes:
            print(v1, "--", v2)
        voltar(G, direcao)


def Tarjan(G, direcao, op, v1):
    if op is True:
        result = False
        time = 0
        node_list = []
        vertices = []

        for node in list(G.nodes()):
            new_tuple = (
                node, {"tree_root": False, "visited": False,
                       "cut": False, "time": 0, "low": 0})
            node_list.append(new_tuple)
        G.add_nodes_from(node_list)

        T = nx.DiGraph()

        for node in list(G.nodes()):
            if (G._node[node]["visited"] is False):
                G._node[node]["tree_root"] = True
                findCutVertices(G, node, T, time)

        for node in list(G.nodes()):
            if (G._node[node] == v1):
                if (G._node[node]["cut"] is True):
                    result = True
                    break
        return result

    else:
        time = 0
        node_list = []
        vertices = []

        for node in list(G.nodes()):
            new_tuple = (
                node, {"tree_root": False, "visited": False, "cut": False,
                       "time": 0, "low": 0})
            node_list.append(new_tuple)
        G.add_nodes_from(node_list)

        T = nx.DiGraph()

        for node in list(G.nodes()):
            if (G._node[node]["visited"] is False):
                G._node[node]["tree_root"] = True
                findCutVertices(G, node, T, time)

        for node in list(G.nodes()):
            if (G._node[node]["cut"] is True):
                vertices.append(node)
        print("\n%d Vértices achados" % len(vertices))
        for v1 in vertices:
            print(v1)
        voltar(G, direcao)


def findCutVertices(G, root, T, time):
    G._node[root]["visited"] = True
    G._node[root]["time"] = time
    G._node[root]["low"] = time
    time += 1
    T.add_node(root)
    for item in list(G.neighbors(root)):
        if (G._node[item]["visited"] is False):
            findCutVertices(G, item, T, time)
            T.add_edge(root, item)
            G._node[root]["low"] = min(
                G._node[root]["low"], G._node[item]["low"])
            if (G._node[root]["tree_root"] and len(list(T.successors(root))) > 1):
                G._node[root]["cut"] = True
            elif (not (G._node[root]["tree_root"]) and G._node[item]["low"] >= G._node[root]["time"]):
                G._node[root]["cut"] = True
        else:
            G._node[root]["low"] = min(
                G._node[root]["low"], G._node[item]["time"])
    return time


def fleury(G, direcao):
    inicio = 0.0
    if direcao == 1:
        G1 = nx.Graph()
        for node in list(G.nodes()):
            G1.add_node(node)
        for v1, v2, in list(G.edges()):
            G1.add_edge(v1, v2)
    elif direcao == 2:
        G1 = nx.DiGraph()
        for node in list(G.nodes()):
            G1.add_node(node)
        for v1, v2, in list(G.edges()):
            G1.add_edge(v1, v2)

    escolha = int(
        input("Gostaria de usar qual função? (1)Naive / (2)Tarjan: "))

    if escolha == 1:
        if nx.is_eulerian(G) is False:
            print("\nO grafo não possui caminho euleriano.")
        else:

            numVertices = nx.number_of_edges(G)
            fonte = input("Digite o rótulo do vértice inicial: ")
            inicio = time.time()
            print("Caminho de Fleury: ")
            print(fonte)

            for i in range(numVertices):
                if G.degree(fonte) > 1:
                    n = [n for n in G.neighbors(fonte)]
                    for j in range(len(n)):
                        ponte = naive(G, direcao, True, fonte, n[j])
                        if ponte is False:
                            print(n[j])
                            G.remove_edge(fonte, n[j])
                            fonte = n[j]
                            break
                elif G.degree(fonte) == 1:
                    n = [n for n in G.neighbors(fonte)]
                    print(n[0])
                    G.remove_edge(fonte, n[0])
                    fonte = n[0]
    elif escolha == 2:
        if nx.is_eulerian(G) is False:
            print("\nO grafo não possui caminho euleriano.")
        else:

            numVertices = nx.number_of_nodes(G)
            fonte = input("Digite o rótulo do vértice inicial: ")
            inicio = time.time()
            print("Caminho de Fleury: ")
            print(fonte)

            for i in range(numVertices):
                if G.degree(fonte) > 1:
                    n = [n for n in G.neighbors(fonte)]
                    for j in range(len(n)):
                        ponte = Tarjan(G, direcao, True, fonte)
                        if ponte is False:
                            print(n[j])
                            G.remove_edge(fonte, n[j])
                            fonte = n[j]
                            break
                elif G.degree(fonte) == 1:
                    n = [n for n in G.neighbors(fonte)]
                    print(n[0])
                    G.remove_edge(fonte, n[0])
                    fonte = n[0]
    fim = time.time()
    tempoTotal = str(fim-inicio)
    print("\n========== Tempo de execução: ==========")
    print(tempoTotal + " segundos")
    voltar(G1, direcao)