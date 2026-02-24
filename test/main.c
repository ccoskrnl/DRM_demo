#include <stdio.h>
extern void foo();
extern void bar();
int main(void)
{
    printf("Hello, I'm main.\n");
    foo();
    bar();
    return 0;
}
