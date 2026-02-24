#include <stdio.h>
extern void foo();

void bar()
{
    void* foo_ptr = foo;
    printf("Hello, I'm bar. foo_ptr = %p.\n", foo_ptr);
}
