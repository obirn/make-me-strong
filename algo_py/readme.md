# `algo_py` directory

**Warning** now `algopy` is `algo_py` (a module named `algopy` already exists in Python...)

[2023-01-23] all files here are the same (for now) as those used in S3

## Utilisation

To import the module `xxx.py`

    from algo_py import xxx


- either the file containing the import is in the same directory as `algopy`
- either `algo_py` has been added to the "Python path" (recommended)

## Graphviz to display graphs
To use the `display` functions in `graph.py`:

- under IPython, if you managed to install [Graphviz](https://pypi.org/project/graphviz/)
    
    - try `graph.display(G)` 
- console mode:
    - you just need graphviz (not the Python module)
    - save the result of your `dot` function in a file (`agraph.dot`in the example below)
    - run `dot`:
        - for instance under Ubuntu
            ```bash
            dot agraph.dot -Tpng > agraph.png
            ```
            creates `agraph.png`: ![`agraph.png`](agraph.png) 
            
- Online: copy the result of `print(graph.dot(G))` here: [https://dreampuf.github.io/GraphvizOnline](https://dreampuf.github.io/GraphvizOnline)
