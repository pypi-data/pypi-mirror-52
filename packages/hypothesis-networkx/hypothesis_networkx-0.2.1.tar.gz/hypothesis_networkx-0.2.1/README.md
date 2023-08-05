# Hypothesis-networkx

This module provides a Hypothesis strategy for generating networkx graphs.
This can be used to efficiently and thoroughly test your code.

## Installation

This module can be installed via `pip`:
```
pip install hypothesis-networkx
```

## User guide

The module exposes a single function: `graph_builder`. This function is a
hypothesis composite strategy for building graphs. You can use it as follows:

```python3
from hypothesis_networkx import graph_builder
from hypothesis import strategies as st
import networkx as nx

node_data = st.fixed_dictionaries({'name': st.text(),
                                   'number': st.integers()})
edge_data = st.fixed_dictionaries({'weight': st.floats(allow_nan=False,
                                                       allow_infinity=False)})


builder = graph_builder(graph_type=nx.Graph,
                        node_keys=st.integers(),
                        node_data=node_data,
                        edge_data=edge_data,
                        min_nodes=2, max_nodes=10,
                        min_edges=1, max_edges=None,
                        self_loops=False,
                        connected=True)

graph = builder.example()
print(graph.nodes(data=True))
print(graph.edges(data=True))
```

Of course this builder is a valid hypothesis strategy, and using it to just
make examples is not super useful. Instead, you can (and should) use it in
your testing framework:

```python3
from hypothesis import given

@given(graph=builder)
def test_my_function(graph):
    assert my_function(graph) == known_function(graph)

```

The meaning of the arguments given to `graph_builder` are pretty
self-explanatory, but they *must* be given as keyword arguments. 
  - `node_data`: The strategy from which node attributes will be drawn.
  - `edge_data`: The strategy from which edge attributes will be drawn.
  - `node_keys`: Either the strategy from which node keys will be draw, or
                 None. If None, node keys will be integers from the range (0, number of nodes).
  - `min_nodes` and `max_nodes`: The minimum and maximum number of nodes the 
                                 produced graphs will contain.
  - `min_edges` and `max_edges`: The minimum and maximum number of edges the
                                 produced graphs will contain. Note that less 
                                 edges than `min_edges` may be added if there 
                                 are not enough nodes, and more than
                                 `max_edges` if `connected` is True.
  - `graph_type`: This function (or class) will be called without arguments to
                  create an empty initial graph.
  - `connected`: If True, the generated graph is guaranteed to be a single
                 connected component.
  - `self_loops`: If False, there will be no self-loops in the generated graph.
                  Self-loops are edges between a node and itself.

## Known limitations

There are a few (minor) outstanding issues with this module:

  - Graph generation may be slow for large graphs.
  - The `min_edges` argument is not always respected when the produced graph
    is too small.
  - The `max_edges` argument is not always respected if `connected` is True.
  - It currently works for Python 2.7, but this is considered deprecated and
    may stop working without notice.

## See also

[Networkx](https://networkx.github.io/documentation/stable/index.html)
[Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html)
