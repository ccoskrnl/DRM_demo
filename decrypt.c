#include <stdint.h>
#include <string.h>
#include "get_key_hash.h"
#include "my_hash.h"
#include "types.h"


uint64_t decrypt_val = 0;

extern int get_key(uint64_t user_key);
extern uint8_t get_key_COPY[];
extern int get_key_SIZE;

uint64_t decrypt(uint64_t user_key, uint64_t data)
{
    uint64_t get_key_val = hash3_jenkins((addr_t)get_key, get_key_SIZE);
    if (get_key_val != get_key_HASH)
    {
        memcpy((addr_t)get_key, get_key_COPY, get_key_SIZE);
    }

    int key = get_key(user_key);
    return data ^ key;
}
