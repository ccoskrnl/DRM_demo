#ifndef __MY_HASH_H__
#define __MY_HASH_H__

#include <stdint.h>
#include "types.h"

uint64_t hash1_xor_rot(addr_t addr, long size);
uint64_t hash2_fnv1(addr_t addr, long size);
uint64_t hash3_jenkins(addr_t addr, long size);

#endif
