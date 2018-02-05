#include "constants.h"

int main(int argc, char** argv) {
    printf("GLPK Version: %s\n", glp_version());

    glp_graph *G;
    int ret = 0;
    clock_t start, end;

    // create a graph
    G = glp_create_graph(sizeof(v_data), sizeof(a_data));

    // initialize the graph using a network generator
    printf("make_mincost_net\n");
    timer(start);
    ret = make_mincost_net(G, 50000, 90000, 25000);
    timer(end);
    print_time;

    // solve min-cost using RelaxIV algorithm
    double sol;
    if (ret == 0) {
        printf("glp_mincost_relax4\n");
        timer(start);
        ret = glp_mincost_relax4(G, offsetof(v_data, rhs),
                offsetof(a_data, low), offsetof(a_data, cap),
                offsetof(a_data, cost), 1, &sol, offsetof(a_data, x),
                offsetof(a_data, rc));
        timer(end);
        print_time;
    } else {
        printf("Error in glp_read_mincost: %d\n", ret);
        glp_delete_graph(G);
        return ret;
    }

    if (ret != 0) {
        printf("Error in glp_mincost_relax4: %d\n", ret);
        glp_delete_graph(G);
        return ret;
    }

   //print_mincost_sol(G, sol);

   return 0;
}
