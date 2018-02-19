#include <lemon/list_graph.h>
#include <lemon/dimacs.h>
#include <lemon/concepts/maps.h>
#include <lemon/network_simplex.h>

#include "lemon.h"

using namespace lemon;
using namespace std;

/**
 * Compiles with:
 *  g++ -o hello_lemon src/main/cpp/lemon.cc src/main/cpp/utils.cc -lemon
 */
int main(int argc, char* argv[])
{
  char filename[1024];

  if (0 != parseArgs(argc, argv, filename)) {
    return 1;
  }

  cout << "Reading file " << filename << endl;
  std::ifstream dimacsFile (filename);

  typedef int VType;
  typedef ListDigraph Digraph;
  typedef Digraph::Node Node;
  typedef Digraph::Arc Arc;
  typedef Digraph::ArcIt ArcIt;
  typedef concepts::ReadWriteMap<Arc, VType> LowerMap;
  typedef concepts::ReadWriteMap<Arc, VType> CapacityMap;
  typedef concepts::ReadWriteMap<Arc, VType> CostMap;
  typedef concepts::ReadWriteMap<Node, VType> SupplyMap;

  Digraph graph;
  LowerMap lower;
  CapacityMap capacity;
  CostMap cost;
  SupplyMap supply;

  readDimacsMin(dimacsFile, graph, lower, capacity, cost, supply);

  cout << "Read: " << countNodes(graph) << " nodes, " << countArcs(graph) << " arcs" << endl;

  // Network Simplex
  for (ArcIt a(graph); a != INVALID; ++a) {
    cout << "Working on " << endl;
    cout << lower[a] << endl;
  }

  NetworkSimplex<Digraph> solver(graph);
  solver.reset().resetParams();
//    .lowerMap(lower);
//    .upperMap(capacity)
//    .costMap(cost)
//    .supplyMap(supply);

  //bool ret = solver.run();
  //cout << "Ret: " << ret << endl;

  return 0;
}

