#include "decl.h"
#include "test.h"
#include <stdio.h>

int main(int argc, char *argv[]) {
  Status out;
  test(&out);
  printf("%d\n", out);
  return 0;
}
