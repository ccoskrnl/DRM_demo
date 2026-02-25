#include <stdio.h>
#include <string.h>
#include "types.h"
#include "decrypt_hash.h"

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
        uint64_t decrypted_data = decrypt(user_key, data[i]);
        printf("%c", (char)(decrypted_data));
        printf("%c", (char)(decrypted_data >> 8));
        printf("%c", (char)(decrypted_data >> 16));
        printf("%c", (char)(decrypted_data >> 24));
        printf("%c", (char)(decrypted_data >> 32));
        printf("%c", (char)(decrypted_data >> 40));
        printf("%c", (char)(decrypted_data >> 48));
        printf("%c", (char)(decrypted_data >> 56));
    }

}
