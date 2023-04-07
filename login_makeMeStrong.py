# -*- coding: utf-8 -*-
"""
S4 - March 2023
Strong Connectivity Homework
@author: robin.varliette
"""

from algo_py import graph, stack

# you can use any function from strong_çonnectivity.py, for instance scc.condensation

# you can import anything from algo_py or built-in... (do not forget to add the import part!)

# ------------------------------------------------------------------------------
# 2.2 Tarjan


def __aux_tarjan(G, x, pref, cpt, scc, noscc, vertexStack, rep_scc):
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
            (return_y, cpt, noscc) = __aux_tarjan(
                G, y, pref, cpt, scc, noscc, vertexStack)
            return_x = min(return_x, return_y)
        else:
            return_x = min(return_x, pref[y])

    if return_x == pref[x]:  # x root of a new scc
        noscc += 1
        rep_scc.append(x)
        y = -1
        while y != x:
            y = vertexStack.pop()
            scc[y] = noscc
            pref[y] = 666 * G.order

    return (return_x, cpt, noscc)


def __tarjan_custom(G):
    """
    return (k, scc, rep_scc)
    k: number of strongly connected components
    scc: vector of components 
    rep_scc: vector of vertex representat for each scc
    """
    pref = [0] * G.order
    cpt = 0
    vertexStack = stack.Stack()
    k = 0
    scc = [0] * G.order
    rep_scc = []
    for s in range(G.order):
        if pref[s] == 0:
            (_, cpt, k) = __aux_tarjan(
                G, s, pref, cpt, scc, k, vertexStack, rep_scc)
    return (k, scc, rep_scc)


# ------------------------------------------------------------------------------
# Condensation built from Tarjan

def condensation(G):
    """
    Returns Gr, SCC, rep_scc
    Gr: the condensation of the digraph G
    SCC: the vector of strongly connected components,
      a vector that gives for each vertex the number of the component 
      it belongs to (the vertex in Gr).
    rep_scc: the vector containing for each index i a vertex contained in the i-th strongly connected component.
    """
    # Tarjan numbers components from 1 to k
    (k, scc, rep_scc) = __tarjan_custom(G)

    # in Gr, components are numbered from 0 to k-1
    SCC = [i-1 for i in scc]

    Gr = graph.Graph(k, True)
    for x in range(G.order):
        for y in G.adjlists[x]:
            if SCC[x] != SCC[y] and SCC[y] not in Gr.adjlists[SCC[x]]:
                Gr.addedge(SCC[x], SCC[y])
    return (Gr, SCC, rep_scc)

# ------------------------------------------------------------------------------

# Disclaimer:
# No, the comments don't come from Chat-GPT: It just comes from me because I like my code being commented.
# - Robin


def __find_pairs(Gr, src, x, M, out_deg, pairs, foundSink):
    # Mark the vertex as visited
    M[x] = True

    # Detect if it is the first sink to be found during the dfs.
    # If it is, append it in the pairs list,
    # and return the information that the first sink has been found.
    if out_deg[x] == 0:
        if not foundSink:
            pairs.append((src, x))
        else:
            # Unmark the vertex so that future sources that will explore them will add them in pairs.
            M[x] = False
        return True

    # Iterate through the neighbours of x
    for adj in Gr.adjlists[x]:

        # If the neighbour has been marked, it means that another source marked this vertex AND that a sink has been found.
        # Thus, we don't need to explore this path.

        # Explore the unmarked vertices
        if not M[adj]:

            # Recursive call:
            # Search if the first sounk has been found.
            # If it is, we still need to mark all the spanning forest so that reachable sinks don't get appended.
            foundSink = __find_pairs(Gr, src, adj, M,
                                     out_deg, pairs,
                                     foundSink)

    return foundSink


def __add_edge(G, scc_x, scc_y, rep_scc):
    """ Add an edge to link scc 'scc_x' to scc 'scc_y' using the rep_scc vector
    """
    # Get the representants in the graph
    repx = rep_scc[scc_x]
    repy = rep_scc[scc_y]

    # Add edge in the graph
    G.adjlists[repx].append(repy)


def __add_first_set_of_edges(G, pairs, isolateds, rep_scc):

    num_edges = 0

    # 1) Link all pairs
    if len(pairs) == 0:
        lastSink = None
    else:
        _, lastSink = pairs[0]
        for i in range(1, len(pairs)):
            src, sink = pairs[i]
            __add_edge(G, lastSink, src, rep_scc)
            num_edges += 1
            lastSink = sink

    # 2) Link all isolated vertices
    if len(isolateds) == 0:
        lastIsolated = None
    else:
        lastIsolated = isolateds[0]
        for i in range(1, len(isolateds)):
            isolated = isolateds[i]
            __add_edge(G, lastIsolated, isolated, rep_scc)
            num_edges += 1
            lastIsolated = isolated

    # 3) Create a cycle with isolated vertices and pairs
    if lastSink is not None:
        firstSrc, _ = pairs[0]
        if lastIsolated is not None:
            firstIsolated = isolateds[0]
            __add_edge(G, lastSink, firstIsolated, rep_scc)
            __add_edge(G, lastIsolated, firstSrc, rep_scc)
            num_edges += 2
        else:
            __add_edge(G, lastSink, firstSrc, rep_scc)
            num_edges += 1
    else:
        if lastIsolated is not None:
            firstIsolated = isolateds[0]
            __add_edge(G, lastIsolated, firstIsolated, rep_scc)
            num_edges += 1

    return num_edges


def wikipedia(G):
    """Makes G strongly connected (add edges in G to make it strongly connected)
        Return the number of added edges
    """

    # Get the condensation graph and vector of strongly connex components
    (Gr, vscc) = scc.condensation(G)

    if Gr.order == 1:
        return 0

    # For each scc, choose a vertex that will represent it.
    rep_scc = [0] * Gr.order
    for x in range(G.order):
        rep_scc[vscc[x]] = x

    # Compute in and out degree
    in_deg = [0] * Gr.order
    out_deg = [0] * Gr.order
    for x in range(Gr.order):
        for y in Gr.adjlists[x]:
            in_deg[y] += 1
            out_deg[x] += 1

    # Retrieve source, sink and isolated vertices
    sources, sinks, isolateds = [], [], []
    for x in range(Gr.order):
        if out_deg[x] == 0:
            if in_deg[x] == 0:
                isolateds.append(x)
            else:
                sinks.append(x)
        elif in_deg[x] == 0:
            sources.append(x)

    # Compute the pairs of sources and sinks
    pairs = []
    M = [False]*Gr.order
    for src in sources:
        __find_pairs(Gr, src, src, M, out_deg, pairs, False)

    # Detect unused source and sinks
    # TODO: Can be improved by detecting unused source/sources sinks during the dfs
    source_presence = [0] * Gr.order
    sinks_presence = [0] * Gr.order
    for (source, sink) in pairs:
        sinks_presence[sink] += 1
        source_presence[source] += 1

    unused_sources = [src for src in sources if source_presence[src] == 0]
    unused_sinks = [sink for sink in sinks if sinks_presence[sink] == 0]

    num_edges = __add_first_set_of_edges(G, pairs, isolateds, rep_scc)

    # TODO: This sure can be improved too
    len_usrc = len(unused_sources)
    len_usinks = len(unused_sinks)

    i = 0
    while i < len_usinks and i < len_usrc:
        __add_edge(G, unused_sinks[i], unused_sources[i], rep_scc)
        num_edges += 1
        i += 1

    while i < len_usinks:
        __add_edge(G, unused_sinks[i], sources[0], rep_scc)
        num_edges += 1
        i += 1

    while i < len_usrc:
        __add_edge(G, sinks[0], unused_sources[i], rep_scc)
        num_edges += 1
        i += 1

    return num_edges


def __paires_dfs(Gr, x, visited, in_degrees, out_degrees, pairs):
    visited[x] = True
    for adj in Gr.adjlists[x]:
        if not visited[adj]:
            __paires_dfs(Gr, adj, visited, in_degrees, out_degrees, pairs)
    if in_degrees[x] == 0 and out_degrees[x] > 0:
        for adj in Gr.adjlists[x]:
            if out_degrees[adj] == 0:
                pairs.append((x, adj))
                in_degrees[x], out_degrees[x] = 0, 0
                in_degrees[adj], out_degrees[adj] = 0, 0
                break


def wikipedia(G):
    # On trouve la condensation du graphe
    Gr, SCC = scc.condensation(G)

    # On trouve les ss [s], les puits [p] et les sommets isolés [q].
    # Rq :    Les ss sont les composantes fortement connectées avec au
    #           moins une arête sortante, mais aucune arête entrante. Les puits
    #           sont les composantes fortement connectées avec des arêtes entrantes
    #           mais aucune arête sortante. Les sommets isolés sont les
    #           composantes fortement connectées sans arêtes entrantes ni
    #           sortantes.

    s_source, t_puit, q_isole = [], [], []
    in_degrees, out_degrees = [0]*G.order, [0]*G.order
    for x in range(Gr.order):
        for adj in G.adjlists[x]:
            in_degrees[adj] += 1
            out_degrees[x] += 1

    for s in range(Gr.order):
        if in_degrees[s] == 0 and out_degrees[s] == 0:
            q_isole.append(s)
        elif in_degrees[s] == 0:
            s_source.append(s)
        elif out_degrees[s] == 0:
            t_puit.append(s)

    # On calcule le nombre de edges à ajouter
    s, t, q = len(s_source), len(t_puit), len(q_isole)
    nb_edges = max(s+q, t+q)

    # On parcours en dfs Gr pour trouver les couples (s,t)
    pairs = []
    visited = [False]*Gr.order

    for src in s_source:
        sink = __paires_dfs(Gr, src, visited, in_degrees, out_degrees, pairs)

    # On se sert des 3 listes pour relier les noeuds entre eux => fortement connexe
    # On suit plusieurs étapes pour ça :
    # I) On connecte les paires avec celles isolées dans
    cycle = pairs + [(q_isole[k], q_isole[k+1]) for k in range(len(q_isole) - 1)
                     ] + [(q_isole[-1], q_isole[0])] if q_isole else []

    # II) On connecte les t_puits qui restent aux s_ss qui restent
    restes_s = [x for x in s_source if in_degrees[x] == 0]
    restes_t = [x for x in t_puit if out_degrees[x] == 0]
    le_reste = list(zip(restes_t, restes_s))

    # III) On connecte les s_ss et les t_puits au cycle en ajoutant un edge par s_s ou t_p
    derniers_edges = []
    if len(restes_s) > len(restes_t):
        for k, s in enumerate(restes_s):
            if k >= len(restes_t) and cycle:
                edge = (s, cycle[0][0])
                derniers_edges.append(edge)
    elif len(restes_t) > len(restes_s) and cycle:
        for k in range(len(restes_s), len(restes_t)):
            edge = (cycle[0][1], restes_t[k])
            derniers_edges.append(edge)

    # IV) On ajoute les arêtes calculées à G
    for (src, tpt) in cycle + le_reste + derniers_edges:
        G.addedge(SCC[src], SCC[tpt])

    # V) On a fini !
    return nb_edges
