#! /usr/bin/env python3
__descr__ = """
This script is a parser from DIMACS to DOT that helps you transform
the max-flow or min-cost DIMACS files into DOT files.
"""
#
# Terminology:
# - 'problem.max' = the max-flow problem written in DIMACS
# - 'problem.min' = the min-cost problem written in DIMACS
# - 'results' = the results of ./pseudo, the max-flow solver
#
#     ./dimacs_to_dot.py problem.max | dot -Tpng > problem.png
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
    for line in dimacs_file:
        vals = [i for i in re.findall("(\d+|\w+)",line)]
        if vals:
            if vals[0] in ["cn","n"]:
                vertices += [vals[1:]]
            if vals[0] == "a":
                edges += [vals[1:]]
    return [vertices, edges]

# Parses a result file that has the form
# Form: `starting_char vertex1 vertex2 flow_value`
# Ex:   `a 4 1 90`
# Call: parse_result("file.result",'a',[[1,2],...]
# In: starting_char is the character that introduces each
#       new result line
# In/out: edges with the form [[1,2],...]
# In: result_file_name is the input file already open
# and add a column into edge
def parse_result(result_file, starting_char, edges):
    for line in result_file:
        vals = [i for i in re.findall("(\d+|\w+)",line)]
        if vals and vals[0] == starting_char:
            vals = vals[1:]
            i = next(i for i in range(len(edges)) if \
                    [vals[0],vals[1]]==[edges[i][0],edges[i][1]])
            edges[i] += [vals[2]]
    return edges

# Creates the dot file and write it into the output_file
def print_dot_file(edges, vertices, output_file):
    print('digraph a \n')
    print('{ \n')
    print('\tgraph [rankdir=LR];')
    for v in vertices:
        print('\t%s [label=%s];' % (v[0], v[1]))
    for e in edges:
        if len(e) == 3:
            print('\t%s -> %s [label="(%s)" fontsize=11];' % (e[0], e[1], e[2]))
        if len(e) == 4:
            print('\t%s -> %s [label=<(%s)> fontsize=11 xlabel=<<font color=\'red\'>%s</font>>];' % (e[0],e[1],e[2],e[3]))
    print('}')

parser = argparse.ArgumentParser(description=__descr__,add_help=True)
parser.add_argument("dimacs_file", nargs='?',\
        type=argparse.FileType('r'), default=sys.stdin,\
        help='the input DIMACS file')
parser.add_argument("-o", nargs='?',\
        type=argparse.FileType('w'), default=sys.stdout, \
        help='the output file in DOT format', metavar='output')
parser.add_argument("-r", required=False, nargs=1, \
        type=argparse.FileType('r'),\
        help='the optional result file given by your solver (see -c)',\
        metavar='result_file')
parser.add_argument("-rstdin", required=False, action="store_true", default=False,\
        help='use stdin as the input for the result file')
parser.add_argument("-c",nargs=1,\
        help='use a different starting char for the result file',\
        metavar='starting_char', default='a')
args = parser.parse_args()

# 0. Checking args
# Exclusive or: either stdin OR a file name
result_has_been_given = False
if (args.rstdin == True or args.r != None):
    result_has_been_given = True
    if not (args.rstdin == True) ^ (args.r != None):
        print("error: can't have both -rstdin and -r",file=sys.stderr)
        sys.exit(1)
    elif args.rstdin == True:
        # We must check that sys.stdin is not already used
        # by dimacs_file
        if args.dimacs_file != sys.stdin:
            res_file = sys.stdin
        else:
            print("error: you must give an explicit dimacs file name \
                  when using -rstdin",file=sys.stderr)
            sys.exit(1)
    else:
        res_file = open(args.r,'r')

# 1. Parse the dimacs file
[vertices,edges] = parse_dimacs(args.dimacs_file)

# 2. Parse the result file if given
if result_has_been_given:
    edges = parse_result(res_file, args.c, edges)

# 3. Produce the dot file
print_dot_file(edges,vertices,args.o)
