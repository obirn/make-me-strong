# -*- coding: utf-8 -*-
"""
Undergraduates - S4
Digraphs - strong connectivity
2023-03
"""

from algo_py import graph, stack


#------------------------------------------------------------------------------
# tools

def reverse_graph(G):
    G_1 = graph.Graph(G.order, True)
    for s in range(G.order):
        for adj in G.adjlists[s]:
            G_1.addedge(adj, s)
    return G_1

def __dfs(G, s, M, mark=True):
    M[s] = mark
    for adj in G.adjlists[s]:
        if not M[adj]:
            __dfs(G, adj, M, mark)

def simpleDFS(G, s):
    M = [False]*G.order
    __dfs(G, s, M)
    return M

#------------------------------------------------------------------------------
# 2.1 naive 

    
def naiveAlgo(G):
    G_1 = reverse_graph(G)
    comp = [0] * G.order
    no = 0
    for x in range(G.order):
        if comp[x] == 0:
            plus = simpleDFS(G, x)
            minus = simpleDFS(G_1, x)
            no += 1
            for y in range(G.order):
                if plus[y] and minus[y]:
                    comp[y] = no
    return (no, comp)

#------------------------------------------------------------------------------
# 2.2 Kosaraju

            
def __dfsPost(G, x, M, post):
    M[x] = True
    for y in G.adjlists[x]:
        if not M[y]:
            __dfsPost(G, y, M, post)
    post.push(x)

# SCC: strongly connected component
def Kosaraju(G):
    """
    returns the SCC vector
    """
    post = stack.Stack()
    M = [False] * G.order
    for s in range(G.order):
        if not M[s]:
            __dfsPost(G, s, M, post)
    
    G_1 = reverse_graph(G)
    comp = [0] * G.order
    no = 0
    while not post.isempty():
        s = post.pop()
        if comp[s] == 0:
            no += 1
            __dfs(G_1, s, comp, no)
    
    return (no, comp)
    
#------------------------------------------------------------------------------
# 2.2 Tarjan

def __Tarjan(G, x, pref, cpt, scc, noscc, vertexStack):
    """
    DFS of G from x
    pref the prefix vector and cpt its counter
    scc the component vector and noscc the number of actual component
    vertexStack: the vertex stack!
    return (return_x, cpt, noscc) where return_x is the return value of x
    """
    cpt += 1
    pref[x] = cpt
    return_x = pref[x]
    vertexStack.push(x)
    for y in G.adjlists[x]:
        if pref[y] == 0:
            (return_y, cpt, noscc) = __Tarjan(G, y, pref, cpt, scc, noscc, vertexStack)
            return_x = min(return_x, return_y)
        else:
            return_x = min(return_x, pref[y])
            
    if return_x == pref[x]: # x root of a new scc
        noscc += 1
        y = -1
        while y != x:
            y = vertexStack.pop()
            scc[y] = noscc
            pref[y] = 666 * G.order

    return (return_x, cpt, noscc)

def Tarjan(G):
    """
    return (k, scc)
    k: number of strongly connected components
    scc: vector of components 
    """    
    pref = [0] * G.order
    cpt = 0
    vertexStack = stack.Stack()
    k = 0
    scc = [0] * G.order
    for s in range(G.order):
        if pref[s] == 0:
            (_, cpt, k) = __Tarjan(G, s, pref, cpt, scc, k, vertexStack)
    return (k, scc)



#------------------------------------------------------------------------------
# Condensation built from Tarjan

def condensation(G):
    """
    build the condensation Gr of the digraph G
    return Gr and the vector of strongly connected components: 
      a vector that gives for each vertex the number of the component 
      it belongs to (the vertex in Gr).
    """        
    (k, scc) = Tarjan(G)        # Tarjan numbers components from 1 to k
    SCC = [i-1 for i in scc]    # in Gr, components are numbered from 0 to k-1

    Gr = graph.Graph(k, True)
    for x in range(G.order):
        for y in G.adjlists[x]:
            if SCC[x] != SCC[y] and SCC[y] not in Gr.adjlists[SCC[x]]:
                Gr.addedge(SCC[x], SCC[y])
    return (Gr, SCC)
            
