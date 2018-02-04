#include <stdio.h>
#include "constants.h"

int main(int argc, char** argv) {
    printf("GLPK Version: %s\n", glp_version());

    glp_graph *G;
    int ret = 0;

    // create a graph
    G = glp_create_graph(sizeof(v_data), sizeof(a_data));

    // initialize the graph with data from a file in DIMACS format
    ret = glp_read_mincost(G, offsetof(v_data, rhs),
        offsetof(a_data, low), offsetof(a_data, cap),
        offsetof(a_data, cost), "dat/sample.min");

    // write the solution to a file, or log error code
    if (ret == 0) {
        glp_write_mincost(G, offsetof(v_data, rhs),
            offsetof(a_data, low), offsetof(a_data, cap),
            offsetof(a_data, cost), "dat/sample.solution");
    } else {
        printf("Error: %d", ret);
    }

    // clean up data structures
    glp_delete_graph(G);

    return ret;
}
