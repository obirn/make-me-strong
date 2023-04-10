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
    return (Gr, SCC, rep_scc)

# ------------------------------------------------------------------------------

# Disclaimer:
# No, the comments don't come from Chat-GPT: It just comes from me because I like my code being commented.
# - Robin


def __find_pairs(Gr, src, x, M, out_deg, pairs, sink, unused_sinks):
    M[x] = True
    if out_deg[x] == 0:
        if sink is None:
            return x
        else:
            unused_sinks.append(x)
            return sink

    for adj in Gr.adjlists[x]:
        if not M[adj]:
            sink = __find_pairs(Gr, src, adj, M,out_deg, pairs, sink,unused_sinks)

    return sink


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
    (Gr, vscc, rep_scc) = __condensation(G)

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
    unused_sources = []
    unused_sinks = []

    for src in sources:
        sink = __find_pairs(Gr, src, src, M, out_deg, pairs, None, unused_sinks)
        if sink is not None:
            pairs.append((src, sink))
        else:
            unused_sources.append(src)

    # sinks_presence = [0] * Gr.order
    # for (source, sink) in pairs:
    #     sinks_presence[sink] += 1

    # unused_sinks = [sink for sink in sinks if sinks_presence[sink] == 0]

    num_edges = __add_first_set_of_edges(G, pairs, isolateds, rep_scc)

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
