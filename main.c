#include <stdint.h>
#include "types.h"
#include "my_hash.h"
#include <string.h>
#include <stdio.h>

#include "play_hash.h"

extern void play(uint64_t user_key, uint64_t data[], int len);
extern int play_SIZE;
extern uint8_t play_COPY[];

extern uint64_t decrypt_val;
extern int decrypt_SIZE;
extern uint64_t decrypt(uint64_t user_key, uint64_t data);

int main(int argc, char *argv[])
{

    printf("Welcome to the DRM challenge!\n");
    uint64_t play_val = hash1_xor_rot((addr_t)play, play_SIZE);
    uint64_t user_key = 0x4142434445464748;


    decrypt_val = hash2_fnv1((addr_t)decrypt, decrypt_SIZE);
    uint8_t encrypted_data[] = { 0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x04, 0x0c,
    0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x04, 0x0c,
    0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x04, 0x0c,
    0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x04, 0x0c
    };
    if (play_val != play_HASH)
    {
        memcpy((addr_t)play, play_COPY, play_SIZE);
    }
    play(user_key, (uint64_t*)encrypted_data, sizeof(encrypted_data) >> 3);
}
