void NAME(dup) (TYPE const a, TYPE* b, TYPE* c) {
    *b = a;
    *c = a;
}

void NAME(swap) (TYPE const a, TYPE const b, TYPE* newb, TYPE* newa) {
    *newb = a;
    *newa = b;
}

void NAME(id) (TYPE const a, TYPE* b) {
    *b = a;
}

void NAME(drop) (TYPE const a) {
}
