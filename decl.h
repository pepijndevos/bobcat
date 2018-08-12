int add(const int a, const int b, int* c) {
  *c = a+b;
  return 0;
}

int push3(int* a) {
  *a = 3;
  return 0;
}

int dup(const int a, int* b, int* c) {
    *b = a;
    *c = a;
    return 0;
}

int seq(const int status) {
  return 0;
}
