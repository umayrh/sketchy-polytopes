#ifndef MINCOST_CONSTANTS_H__
#define MINCOST_CONSTANTS_H__

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
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

#endif
