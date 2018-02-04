#ifndef MINCOST_CONSTANTS_H__
#define MINCOST_CONSTANTS_H__

#include "glpk.h"

/* vertex data block */
typedef struct
{
    double rhs;
} v_data;

/* arc data block */
typedef struct
{
    double low, cap, cost;
} a_data;

#endif
