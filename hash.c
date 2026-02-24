#include <stdint.h>
#include "types.h"

uint64_t hash1(addr_t addr, long size)
{
    uint64_t h = *addr;
    int qwords = size / sizeof(uint64_t);
    int i;
    for (i = 1; i < qwords; i++)
    {
        addr++;
        h ^= *addr;
    }

    return h;
}
