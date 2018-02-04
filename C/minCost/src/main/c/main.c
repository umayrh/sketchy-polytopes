#include <stdio.h>
#include "constants.h"

int main(int argc, char** argv) {
    printf("GLPK Version: %s\n", glp_version());
    return 0;
}
