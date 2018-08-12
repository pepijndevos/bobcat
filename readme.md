# Bobcat

Bobcat is a tiny concatenative programming language inspired by Cat and Joy with the goal of writing expressive and fast behavior trees.

Bobcat compiles to C, and uses C functions for words. A Bobcat word has the following C signature:

    int word(const T input, const T input, ..., T* output, T* output, ...);

Where a non-zero return value returns the outer block.

## Syntax

The usual sequential functional composition

    2 dup mul # 4

The [comma operator](https://suhr.github.io/papers/calg.html), for function concatentation. Think of it as concatenating the input argument lists and output argument lists of each function.

    2 4 dup add,sqrt # 8 1.4142

Function declaration

    def name { word word word }

Bobcat does not have loops and if statements.
It has behavior tree nodes with the following syntax

    node( word word word )

Which is equivalent to

    node_pre word node word node word node node_post

## Functions

TODO

## Types

### `Status`

    typedef enum {FAILURE, SUCCESS, RUNNING} Status;

## Built-in nodes

### `seq`

    int seq_pre(Status*);
    int seq(const Status, const Status, Status*);
    int seq_post(const Status);

### `memseq`

### `sel`

    int sel_pre(Status*);
    int sel(const Status, const Status, Status*);
    int sel_post(const Status);

### `memsel`

### `par`

### `mempar`
