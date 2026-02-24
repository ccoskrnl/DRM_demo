#include <stdio.h>
#include <string.h>
#include "types.h"
#include "decrypt_const.h"

extern uint64_t decrypt_val;

extern uint64_t decrypt(uint64_t user_key, uint64_t data);
extern uint8_t decrypt_COPY[];
extern int decrypt_SIZE;



void play(uint64_t user_key, uint64_t data[], int len)
{
    if (decrypt_val != decrypt_HASH)
    {
        memcpy((addr_t)decrypt, decrypt_COPY,decrypt_SIZE);
    }

    int i = 0;
    for (i = 0; i < len; i++)
    {
        printf("0x%lx\n", decrypt(user_key, data[i]));
    }

}
