typedef enum {FAILURE, SUCCESS, RUNNING} Status;

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

int success(Status *st) {
    *st = SUCCESS;
    return 0;
}

int running(Status *st) {
    *st = RUNNING;
    return 0;
}

int failure(Status *st) {
    *st = FAILURE;
    return 0;
}

int seq_pre(Status* dummy) {
    *dummy = SUCCESS;
    return 0;
}

int seq(const Status st, const Status accum, Status* next) {
    switch (st) {
        case RUNNING:
            *next = RUNNING;
            return 1;
        case FAILURE:
            *next = FAILURE;
            return 1;
        case SUCCESS:
            *next = SUCCESS;
            return 0;
    }
    return 0;
}

int seq_post(const Status st, Status* result) {
    *result = st;
    return 0;
}

