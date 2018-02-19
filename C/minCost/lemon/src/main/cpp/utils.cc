#include "lemon.h"

using namespace std;

/**
 * Parses input arguments, and expects at least one argument.
 * Expects a filename to be the first argument.
 */
int parseArgs(int argc, char* argv[], char* filename)
{
  if (argc > 1) {
    int len = strlen(argv[1]);
    if (len == 0) {
      perror("No input filename given");
      return 1;
    }
    memcpy(filename, argv[1], len+1);
    return 0;
  }
  perror("No input filename given");
  return 1;
}

