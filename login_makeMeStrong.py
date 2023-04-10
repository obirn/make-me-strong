# -*- coding: utf-8 -*-
"""
S4 - March 2023
Strong Connectivity Homework
@author: robin.varliette
"""

from algo_py import graph, stack
import strong_connectivity as scc

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
                G, y, pref, cpt, scc, noscc, vertexStack, rep_scc)
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

def __condensation(G):
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
    return (Gr, rep_scc)

# ------------------------------------------------------------------------------

# Disclaimer:
# No, the comments don't come from Chat-GPT: It just comes from me because I like my code being commented.
# - Robin


def __find_pairs(Gr, src, x, M, out_deg, sink, unused_sinks):
    M[x] = True
    if out_deg[x] == 0:
        if sink is None:
            return x
        else:
            unused_sinks.append(x)
            return sink

    for adj in Gr.adjlists[x]:
        if not M[adj]:
            sink = __find_pairs(Gr, src, adj, M, out_deg, sink, unused_sinks)
    return sink


def __Eswaran_tarjan(G: graph.Graph):
    """Makes G strongly connected (add edges in G to make it strongly connected)
        Return the number of added edges
    """

    # Get the condensation graph and vector of strongly connex components
    (Gr, rep_scc) = __condensation(G)

    if Gr.order == 1:
        return 0

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

    # Compute the pairs of sources and sinks, as well as the unused sources and pairs
    pairs = []
    M = [False]*Gr.order
    unused_sources = []
    unused_sinks = []
    for src in sources:
        sink = __find_pairs(Gr, src, src, M, out_deg, None, unused_sinks)
        if sink is not None:
            pairs.append((src, sink))
        else:
            unused_sources.append(src)

    edges = []

    # 1) First set of edges: Link pairs and isolated of isolated vertices
    #   1.a) Link all pairs
    if len(pairs) == 0:
        lastSink = None
    else:
        _, lastSink = pairs[0]
        for i in range(1, len(pairs)):
            src, sink = pairs[i]
            edges.append((rep_scc[lastSink], rep_scc[src]))
            lastSink = sink

    #   1.b) Link all isolated vertices
    if len(isolateds) == 0:
        lastIsolated = None
    else:
        lastIsolated = isolateds[0]
        for i in range(1, len(isolateds)):
            isolated = isolateds[i]
            edges.append((rep_scc[lastIsolated], rep_scc[isolated]))
            lastIsolated = isolated

    #   1.c) Create a cycle with isolated vertices and pairs
    if lastSink is not None:
        firstSrc, _ = pairs[0]
        if lastIsolated is not None:
            firstIsolated = isolateds[0]
            edges.append((rep_scc[lastSink], rep_scc[firstIsolated]))
            edges.append((rep_scc[lastIsolated], rep_scc[firstSrc]))
        else:
            edges.append((rep_scc[lastSink], rep_scc[firstSrc]))
    else:
        if lastIsolated is not None:
            firstIsolated = isolateds[0]
            edges.append((rep_scc[lastIsolated], rep_scc[firstIsolated]))

    # 2) Link unused sources and unused_sinks together

    i = 0
    len_usrc = len(unused_sources)
    len_usinks = len(unused_sinks)

    while i < len_usinks and i < len_usrc:
        edges.append((rep_scc[unused_sinks[i]], rep_scc[unused_sources[i]]))
        i += 1

    # 3) Link remaining sources or sinks to the cycle

    # Get a vertex that is already in the cycle
    vertex_in_cycle = lastIsolated if lastSink is None else lastSink

    while i < len_usinks:
        edges.append((rep_scc[unused_sinks[i]], rep_scc[vertex_in_cycle]))
        i += 1

    while i < len_usrc:
        edges.append((rep_scc[vertex_in_cycle], rep_scc[unused_sources[i]]))
        i += 1

    # Add edges to the graph
    for x, y in edges:
        G.addedge(x, y)
    return len(edges)



def __paires_dfs(Gr, x, visited, in_degrees, out_degrees, pairs):
    visited[x] = True
    if out_degrees[x] == 0:
        return x
    for adj in Gr.adjlists[x]:
        sink = __paires_dfs(Gr, adj, visited, in_degrees, out_degrees, pairs)
        if sink is not None:
            return sink
    return None


def __link_edge(G, x, adj, gscc):
    rx = gscc[x]
    radj = gscc[adj]

    # On les lie entre eux
    G.adjlists[rx].append(radj)


def __premieres_liaisons(G, pairs, q_isole, gscc):
    edges_to_add = 0

    # 1 - on relie toutes les paires
    if len(pairs) == 0:
        last_t = None
    else:
        _, last_t = pairs[0]
        for k in range(1, len(pairs)):
            s, t = pairs[k]
            __link_edge(G, last_t, s, gscc)
            edges_to_add += 1
            last_t = t

    # 2 - on relie tous les sommets
    if len(q_isole) == 0:
        last_q = None
    else:
        last_q = q_isole[0]
        for k in range(1, len(q_isole)):
            q = q_isole[k]
            __link_edge(G, last_q, q, gscc)
            edges_to_add += 1
            last_q = q

    # 3 - on crée le cycle avec les paires et les sommets isolés
    if last_t is not None:
        first_s, _ = pairs[0]
        if last_q is not None:
            first_q = q_isole[0]
            __link_edge(G, last_t, first_q, gscc)
            __link_edge(G, last_q, first_s, gscc)
            edges_to_add += 2
        else:
            __link_edge(G, last_t, first_s, gscc)
            edges_to_add += 1
    else:
        if last_q is not None:
            first_q = q_isole[0]
            __link_edge(G, last_q, first_q, gscc)
            edges_to_add += 1

    return edges_to_add


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

    if Gr.order == 1:
        return 0

    # construction d'une concordance SCC - gscc, f(représentant)
    gscc = Gr.order*[0]
    for k in range(G.order):
        gscc[SCC[k]] = k

    s_source, t_puit, q_isole = [], [], []
    in_degrees, out_degrees = [0]*Gr.order, [0]*Gr.order

    # degrés intérieurs et extérieurs
    for x in range(Gr.order):
        for adj in Gr.adjlists[x]:
            in_degrees[adj] += 1
            out_degrees[x] += 1

    # détection puits - isolés - sources
    for s in range(G.order):
        if in_degrees[s] == 0 and out_degrees[s] == 0:
            q_isole.append(s)
        elif in_degrees[s] == 0:
            s_source.append(s)
        elif out_degrees[s] == 0:
            t_puit.append(s)

    '''# On calcule le nombre de edges à ajouter
                s, t, q = len(s_source), len(t_puit), len(q_isole)
                nb_edges = max(s+q, t+q)'''

    # On parcours en dfs Gr pour trouver les couples (s,t)
    pairs = []
    visited = [False]*Gr.order

    for src in s_source:
        sink = __paires_dfs(Gr, src, visited, in_degrees, out_degrees, pairs)
        if sink is not None:
            pairs.append((src,sink))

    # On détecte les sources et les puits inutilisés
    ishere_s = [0]*Gr.order
    ishere_t = [0]*Gr.order
    for (s,t) in pairs:
        ishere_s[s] += 1
        ishere_t[t] += 1

    fresh_s = [s for s in s_source if ishere_s[s] == 0]
    fresh_t = [t for t in t_puit if ishere_t[t] == 0]

    edges_to_add = __premieres_liaisons(G, pairs, q_isole, gscc)

    lgth_fresh_s = len(fresh_s)
    lgth_fresh_t = len(fresh_t)
    k = 0

    # 2e étape --------------------------------------
    while k < lgth_fresh_t and k < lgth_fresh_s:
        __link_edge(G, fresh_t[k], fresh_s[k], gscc)
        edges_to_add += 1
        k += 1

    # 3e étape --------------------------------------
    while k < lgth_fresh_t:
        __link_edge(G, fresh_t[k], s_source[0], gscc)
        edges_to_add += 1
        k += 1

    while k < lgth_fresh_s:
        __link_edge(G, s_source[0], fresh_s[k], gscc)
        edges_to_add += 1
        k += 1
    # -----------------------------------------------
    # On a fini !
    return edges_to_add
