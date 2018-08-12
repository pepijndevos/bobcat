#include "decl.h"
#include "test.h"
#include <stdio.h>

int main() {
  int out;
  test(5, &out);
  printf("%d\n", out);
}
