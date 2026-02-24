#include <stdio.h>
extern void bar();

void foo()
{
    void* bar_ptr = bar;
    printf("Hello, I'm foo. bar_ptr = %p.\n", bar_ptr);
}
