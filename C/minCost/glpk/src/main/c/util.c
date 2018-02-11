#include "constants.h"

//
// initialize the graph with data from a file in DIMACS format
//
int read_mincost(glp_graph *G, const char *filename) {
    printf("glp_read_mincost\n");
    return glp_read_mincost(G, offsetof(v_data, rhs),
            offsetof(a_data, low), offsetof(a_data, cap),
            offsetof(a_data, cost), filename);
}

//
// function for print the solution of min-cost problem
//
void print_mincost_sol(glp_graph *G, double sol) {
    printf("print_mincost_sol\n");
    int i;
    glp_vertex *v, *w;
    glp_arc *a;

    printf("sol = %5g\n", sol);

    for (i = 1; i <= G->nv; i++) {
        v = G->v[i];
        for (a = v->out; a != NULL; a = a->t_next) {
            w = a->head;
            printf("arc %d->%d: x = %5g; rc = %5g\n",
                v->i, w->i, arc(a)->x, arc(a)->rc);
        }
    }
}

//
// function for generation a min-cost network using glp_netgen
//
int make_mincost_net(glp_graph *G, int nodes, int arcs, int supply) {
    int ret;
    int parm[1+15];

    parm[0];            // not used
    parm[1] = 666;      // iseed - 8-digit positive random number seed
    parm[2] = 101;      // nprob - 8-digit problem id number
    parm[3] = nodes;    // nodes - total number of nodes
    parm[4] = 1;        // nsorc - total number of source nodes (including transshipment nodes)
    parm[5] = 1;        // nsink - total number of sink nodes (including transshipment nodes)
    parm[6] = arcs;     // iarcs - number of arc
    parm[7] = 1;        // mincst - minimum cost for arcs
    parm[8] = 1000;     // maxcst - maximum cost for arcs
    parm[9] = supply;   // itsup - total supply
    parm[10] = 0;       // ntsorc - number of transshipment source nodes
    parm[11] = 0;       // ntsink - number of transshipment sink nodes
    parm[12] = 10;      // iphic - percentage of skeleton arcs to be given the maximum cost
    parm[13] = 100;     // ipcap - percentage of arcs to be capacitated
    parm[14] = 0;       // mincap - minimum upper bound for capacitated arcs
    parm[15] = 50;      // maxcap  - maximum upper bound for capacitated arcs

    ret = glp_netgen(G, offsetof(v_data, rhs),
        offsetof(a_data, cap), offsetof(a_data, cost), parm);

    return ret;
}

