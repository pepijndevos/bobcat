int add(const int a, const int b, int* c) {
  *c = a+b;
  return 0;
}

int sub(const int a, const int b, int* c) {
  *c = a-b;
  return 0;
}

int mul(const int a, const int b, int* c) {
  *c = a*b;
  return 0;
}

int abs(const int a, int* b) {
  if (a > 0) {
      *b = a;
  } else {
      *b = -a;
  }
  return 0;
}

int dup(const int a, int* b, int* c) {
    *b = a;
    *c = a;
    return 0;
}

int swap(const int a, const int b, int* newb, int* newa) {
    *newb = a;
    *newa = b;
    return 0;
}

int id(const int a, int* b) {
    *b = a;
    return 0;
}

int drop(const int a) {
    return 0;
}

int seq(const int status) {
  return 0;
}
