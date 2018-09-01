#include "decl.h"
#include "test.h"
#include <stdio.h>

int main(int argc, char *argv[]) {
  Status out;
  char* str;
  test(&out, &str);
  printf("%d %s\n", out, str);
  return 0;
}
