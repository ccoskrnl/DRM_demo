#include <stdint.h>
#include "my_hash.h"

extern uint64_t decrypt_val;
extern int decrypt_SIZE;
extern uint64_t decrypt(uint64_t user_key, uint64_t data);

uint64_t get_key(uint64_t user_key)
{
    decrypt_val = hash2_fnv1((addr_t)decrypt, decrypt_SIZE);
    uint64_t secret_key = 0x4142434445464748;
    return user_key ^ secret_key;
}
