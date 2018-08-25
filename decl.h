#define TYPE int
#define NAME(name) name ## i
#include "bobmath.h"
#include "bobstack.h"
#undef TYPE
#undef NAME

#define TYPE float
#define NAME(name) name ## f
#include "bobmath.h"
#include "bobstack.h"
#undef TYPE
#undef NAME

#define TYPE char*
#define NAME(name) name ## s
#include "bobstack.h"
#undef TYPE
#undef NAME

typedef enum {FAILURE, SUCCESS, RUNNING} Status;

void success(Status *st) {
    *st = SUCCESS;
}

void running(Status *st) {
    *st = RUNNING;
}

void failure(Status *st) {
    *st = FAILURE;
}

int seq_pre(Status* dummy) {
    *dummy = SUCCESS;
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

