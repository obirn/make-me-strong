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


def wikipedia(G: graph.Graph):
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

    # 2) Link pairs of unused sources and unused_sinks together

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
