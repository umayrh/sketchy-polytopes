#ifndef MINCOST_CONSTANTS_H__
#define MINCOST_CONSTANTS_H__

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "glpk.h"

/* vertex data block */
typedef struct
{
    double rhs;
} v_data;

/* arc data block */
typedef struct
{
    double low, cap, cost, x, rc;
} a_data;

#define node(v) ((v_data *)((v)->data))
#define arc(a)  ((a_data *)((a)->data))
#define timer(s) (s = clock())
#define print_time (printf("  time taken: %0.3f sec\n", ((double) (end - start)) / CLOCKS_PER_SEC))

int read_mincost(glp_graph *G, const char *filename);
void print_mincost_sol(glp_graph *G, double sol);
int make_mincost_net(glp_graph *G, int nodes, int arcs, int supply);

#endif
