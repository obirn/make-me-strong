import strong_connectivity as scc
from algo_py import graph
import os
import glob
import inspect
import importlib.util
import importlib

# -------------------------------- Few words -----------------------------------
'''
Hi, this is the Jules Lestienne test file for the 2026 S4 Make Me Strong 
project. 

It is not meant to be used in interpreter mode but rather by modifying
variables in the code. This file tests every functions and prints OK if 
correct. As a reminder the goal is to make a graph strongly connected, 
functions should add needed edges and return them in a list. 

Be sure to have strong_connectivity.py and algo_py in the same folder as this 
file. No print in the file. Function's name starting with '__' are not tested. 

To use it follow modify those variable in the next section:
    - file_to_test: the file you need to test with NO "." in filename
    - graph_folder_path: folder containing all graphs to use for test

If you want some details about your code insert your modifications in the 
specified place. Display graph using https://dreampuf.github.io/GraphvizOnline/ 
Uncomment the concerned code. 
'''


# ------------------------------- Tests functions ------------------------------

def edges_needed(G):
    """
        This function returns the number of scc, and the maximum number of edges needed
        to make the graph G strongly connex (according to Eswaran and Tarjan)
        c.f. https://en.wikipedia.org/wiki/Strong_connectivity_augmentation#Unweighted_version
    """
    # Get the condensation graph and vector of strongly connex components
    (Gr, vscc) = scc.condensation(G)

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

    # Compute maximum number of edges that must be added
    s = len(sinks)
    t = len(sources)
    q = len(isolateds)

    max_number_needed = max(s+q, t+q)
    return Gr.order, max_number_needed

# ---------------------------- Test initialization -----------------------------


file_to_test = "login_makeMeStrong"
graph_folder_path = "./files"

# --------------------------------- Test Zone ----------------------------------

module = importlib.import_module(file_to_test)
graph_test_list = glob.glob(os.path.join(graph_folder_path, '*.gra'))
all_functions = inspect.getmembers(module, inspect.isfunction)

for name, func in all_functions:
    if not name.startswith("__"):
        for graph_path in graph_test_list:
            G = graph.load(graph_path)

            n_scc, tarjan_max = edges_needed(G)


#           Print before modification
            # print("Before calling ", 
            #         func, " on ", 
            #         graph_path, "\n", 
            #         graph.todot(G), "\n")
            
            # input()

#           Function call, to modify for more information about inside code
            edges = func(G)

            Gr, _ = scc.condensation(G)
            if (Gr.order == 1):
                print(name, "is OK on", graph_path)
            else:
                print(name, "is not OK on", graph_path)

            if edges > n_scc:
                print(
                    f"Warning: You added more edges ({edges}) than number of scc ({n_scc})")
            if edges > tarjan_max:
                print(
                    f"Warning: You added more edges ({edges}) than maximum number of tarjan ({tarjan_max})")

#           Edges print
            print("Edges added: ", edges)

            # print()
            
            # input()

#           Print after modifications
            '''print("After calling ", 
                    func, " on ", 
                    graph_path, "\n", 
                    graph.todot(G), "\n")
            '''
