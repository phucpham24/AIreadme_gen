from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config

if __name__ == "__main__":
    config = Config(max_depth=10)  # Set the maximum depth for the call graph

    # Output DOT file
    graphviz_dot = GraphvizOutput(output_file='call_graph.dot')
    graphviz_dot.output_format = 'dot'  # Set the output format to DOT

    # Export DOT format call graph separately
    with PyCallGraph(output=graphviz_dot, config=config):
        main()