void NAME(add) (const TYPE a, const TYPE b, TYPE* c) {
  *c = a+b;
}

void NAME(sub) (const TYPE a, const TYPE b, TYPE* c) {
  *c = a-b;
}

void NAME(mul) (const TYPE a, const TYPE b, TYPE* c) {
  *c = a*b;
}

void NAME(abs) (const TYPE a, TYPE* b) {
  if (a > 0) {
      *b = a;
  } else {
      *b = -a;
  }
}
