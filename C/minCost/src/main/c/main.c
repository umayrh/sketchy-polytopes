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

    // solve min-cost using RelaxIV algorithm
    double sol;
    if (ret == 0) {
        ret = glp_mincost_relax4(G, offsetof(v_data, rhs),
             offsetof(a_data, low), offsetof(a_data, cap),
             offsetof(a_data, cost), 0, &sol, offsetof(a_data, x),
            offsetof(a_data, rc));
    } else {
        printf("Error in glp_read_mincost: %d", ret);
        glp_delete_graph(G);
        // clean up data structures
        return ret;
    }

    // write the solution to a file, or log error code
    if (ret == 0) {
        int i;
        glp_vertex *v, *w;
        glp_arc *a;

        printf("ret = %d; sol = %5g\n", ret, sol);

        for (i = 1; i <= G->nv; i++) {
            v = G->v[i];
            for (a = v->out; a != NULL; a = a->t_next) {
                w = a->head;
                printf("arc %d->%d: x = %5g; rc = %5g\n",
                    v->i, w->i, arc(a)->x, arc(a)->rc);
            }
        }
    } else {
        printf("Error in glp_mincost_relax4: %d", ret);
        glp_delete_graph(G);
        return ret;
    }
    return 0;
}
