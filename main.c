#include "decl.h"
#include "test.h"
#include <stdio.h>

int main(int argc, char *argv[]) {
  int out;
  test(10000, -5, 6, &out);
  printf("%d\n", out);
}
