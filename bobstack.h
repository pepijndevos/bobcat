void NAME(dup) (const TYPE a, TYPE* b, TYPE* c) {
    *b = a;
    *c = a;
}

void NAME(swap) (const TYPE a, const TYPE b, TYPE* newb, TYPE* newa) {
    *newb = a;
    *newa = b;
}

void NAME(id) (const TYPE a, TYPE* b) {
    *b = a;
}

void NAME(drop) (const TYPE a) {
}
