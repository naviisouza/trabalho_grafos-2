import networkx as nx
import funcao as func
import menu as m
import sys


sys.setrecursionlimit(10 ** 9)

definirGrafo = int(input("\nDigite 1 para criar um grafo ou 2 para usar um arquivo GML: "))

if definirGrafo == 1:
    numVertices = int(input("\nDigite o número de vértices: "))
    direcao = int(input("\nSe o grafo for não-direcionado, digite 1; se for direcionado, digite 2: "))
    G = func.criarGrafo(numVertices, direcao)

    m.menu(G, direcao)

elif definirGrafo == 2:
    direcao = int(input("\nSe o grafo for não-direcionado, digite 1; se for direcionado, digite 2: "))
    caminho = input("\nInsira o caminho do arquivo: ")
    # ./cem.gml
    # ./mil.gml
    # ./dez_mil.gml
    # ./cem_mil.gml
    G = func.lerArquivo(caminho)

    m.menu(G, direcao)