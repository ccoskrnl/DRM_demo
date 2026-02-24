#include "types.h"
#include "my_hash.h"
#include <string.h>

#include "play_const.h"

extern void play(uint64_t user_key, uint64_t data[], int len);
extern int play_SIZE;
extern uint8_t play_COPY[];

extern uint64_t decrypt_val;
extern int decrypt_SIZE;
extern uint64_t decrypt(uint64_t user_key, uint64_t data);

int main(int argc, char *argv[])
{
    uint64_t play_val = hash1((addr_t)play, play_SIZE);
    uint64_t user_key = 0x4847464544434241;

    decrypt_val = hash1((addr_t)decrypt, decrypt_SIZE);
    uint64_t encrypted_data[] = {0, 0, 0, 0};
    if (play_val != play_HASH)
    {
        memcpy((addr_t)play, play_COPY, play_SIZE);
    }
    play(user_key, encrypted_data, 4);
}
