#include <stdint.h>
#include "types.h"

uint64_t hash1_xor_rot(addr_t addr, long size)
{
    volatile uint64_t hash = 0x234accef123ff;
    int qwords = size / sizeof(uint64_t);
    int i;
    for (i = 0; i < qwords; i++)
    {
        uint64_t val = *addr++;
        hash = (hash ^ val) + ((hash << 5) | (hash >> 27));
        volatile uint64_t dummy = hash * 3 + val;
        (void)dummy;
    }
    return hash;
}

uint64_t hash2_fnv1(addr_t addr, long size)
{
    volatile uint64_t hash = 0xcbf29ce484222325;
    int qwords = size / sizeof(uint64_t);
    uint64_t ch;
    for (int i = 0; i < qwords; i++)
    {
        ch = *addr++;
        hash = hash * 16777619U;
        hash = hash ^ ch;
        volatile uint64_t* p = &hash;
        (void)*p;
    }

    return hash;
}

uint64_t hash3_jenkins(addr_t addr, long size)
{
    uint64_t hash = 0;
    int qwords = size / sizeof(uint64_t);
    int i;
    for (i = 0; i < qwords; i++)
    {
        hash += *addr++;
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }

    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);

    return hash;
}