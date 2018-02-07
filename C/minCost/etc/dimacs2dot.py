#! /usr/bin/env python3
__descr__ = """
This script is a parser from DIMACS to DOT that helps you transform
the max-flow or min-cost DIMACS files into DOT files.
"""
#
# This script is a version of Maël Valais's, posted at
# https://gist.github.com/maelvalais/755c16db4681e3a671c1
# It requires python3 to work.
#
# Terminology:
# - 'problem.max' = the max-flow problem written in DIMACS
# - 'problem.min' = the min-cost problem written in DIMACS
#
#     ./dimacs2dot.py problem.max | dot -Tpng > problem.png
#
# NOTES:
# 1) the `cn 2 NAME` are comment lines, but are used in this script to give
#    names to the vertices.
#
# Content of problem.max:
#
#   p max 10 15
#   n  1   s
#   n  10  t
#   cn 2   A
#   cn 3   B
#   cn 4   C
#   cn 5   D
#   cn 6   E
#   cn 7   Mac
#   cn 8   Linux
#   cn 9   Windows
#   a  1   7   2
#   a  1   8   2
#   a  1   9   3
#   a  7   2   1
#   a  7   4   1
#   a  7   6   1
#   a  7   3   1
#   a  8   3   1
#   a  8   5   1
#   a  9   5   1
#   a  2   10  1
#   a  3   10  1
#   a  4   10  1
#   a  5   10  1
#   a  6   10  1

import re
import sys
import argparse

# Parses the DIMACS file and produces `edges` and `vertices`
# In: the DIMACS input file already open
# Out: [vertices, edges] with
#       edges = [[vertex1, vertex2],...]
#       vertices = [vertex1, vertex2...]
def parse_dimacs(dimacs_file):
    edges = []
    vertices = []
    problem_type = None
    for line in dimacs_file:
        vals = [i for i in re.findall("(\d+|\w+)",line)]
        if vals:
            if vals[0] == "p":
                problem_type = vals[1]
            if vals[0] in ["cn","n"]:
                vertices += [vals[1:]]
            if vals[0] == "a":
                edges += [vals[1:]]
    return [problem_type, vertices, edges]

# Creates the dot file and write it into the output_file
def print_dot_file(problem_type, edges, vertices, output_file):
    if problem_type is None or problem_type not in ['min', 'max']:
        raise ValueError("Invalid problem type given in input file")

    print('digraph a \n')
    print('{ \n')
    print('\tgraph [rankdir=LR];')
    for v in vertices:
        print('\t%s [label=%s];' % (v[0], v[1]))
    if problem_type == 'max':
        for e in edges:
            if len(e) == 3:
                print('\t%s -> %s [label="(%s)" fontsize=11];' % (e[0], e[1], e[2]))
            if len(e) == 4:
                print('\t%s -> %s [label=<(%s)> fontsize=11 xlabel=<<font color=\'red\'>%s</font>>];' % (e[0],e[1],e[2],e[3]))
    if problem_type == 'min':
        for e in edges:
            label = "lb={}, ub={}".format(e[2], e[3])
            xlabel = "cost={}".format(e[4])
            print('\t{} -> {} [label="({})" fontsize=11 xlabel=<<font color=\'red\'>{}</font>>];'.format(e[0], e[1], label, xlabel))
    print('}')

# Parsing arguments
parser = argparse.ArgumentParser(description=__descr__,add_help=True)
parser.add_argument("dimacs_file", nargs='?',\
        type=argparse.FileType('r'), default=sys.stdin,\
        help='the input DIMACS file')
parser.add_argument("-o", nargs='?',\
        type=argparse.FileType('w'), default=sys.stdout, \
        help='the output file in DOT format', metavar='output')
parser.add_argument("-c",nargs=1,\
        help='use a different starting char for the result file',\
        metavar='starting_char', default='a')
args = parser.parse_args()

# 0. Checking args
# We must check that sys.stdin is not already used by dimacs_file
if args.dimacs_file != sys.stdin:
    res_file = sys.stdin
else:
    print("error: you must give an explicit dimacs file name \
        when using -rstdin",file=sys.stderr)
    sys.exit(1)

# 1. Parse the dimacs file
[problem_type, vertices, edges] = parse_dimacs(args.dimacs_file)

# 2. Produce the dot file
print_dot_file(problem_type, edges, vertices,args.o)
