import pydot
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert dot file to png file')
    parser.add_argument('dot_file', help='Input dot file')
    parser.add_argument('png_file', help='Output png file')
    args = parser.parse_args()

    try:
        (graph,) = pydot.graph_from_dot_file(args.dot_file)
        graph.write_png(args.png_file)
    except Exception as e:
        print(e)
        sys.exit(1)
    sys.exit(0)
