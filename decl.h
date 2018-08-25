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

int seq(const int status) {
  return 0;
}
