#!/usr/bin/bash

OPTIMIZATION="-O2 -g"
BUILD_DIR="build"

mkdir -p ${BUILD_DIR}

echo "#include <stdint.h>" > func_body.c
echo "#define get_key_HASH 0x12345678abcdefcc" > get_key_hash.h
echo "" > decrypt_hash.h
echo "" > play_hash.h

gcc -shared -fPIC -O2 hash.c -o libhash.so

gcc ${OPTIMIZATION} -c get_key.c -o ${BUILD_DIR}/get_key.o
gcc ${OPTIMIZATION} -c decrypt.c -o ${BUILD_DIR}/decrypt.o

# 合并get_key.o和decrypt.o，生成一个包含两个函数的可重定位目标文件
ld -r ${BUILD_DIR}/get_key.o ${BUILD_DIR}/decrypt.o -o ${BUILD_DIR}/get_key_and_decrypt.o

# 计算get_key函数的hash，将其写入get_key_hash.h。在get_key_and_decrypt.o中找到
# decrypt函数的机器码，找到临时的get_key_HASH值(应该为 0x12345678abcdefcc)，使用
# 刚刚计算的get_key_HASH值替换它。计算decrypt函数的hash并写入decrypt_hash.h。

python3 calc_hash.py ${BUILD_DIR}/get_key_and_decrypt.o get_key hash3_jenkins > get_key_hash.h

python3 decrypt_replace_hash.py

python3 calc_hash.py ${BUILD_DIR}/get_key_and_decrypt.o decrypt hash2_fnv1 > decrypt_hash.h

python3 extract_func_code.py ${BUILD_DIR}/get_key_and_decrypt.o get_key >> func_body.c
python3 extract_func_code.py ${BUILD_DIR}/get_key_and_decrypt.o decrypt >> func_body.c

gcc ${OPTIMIZATION} -c play.c -o ${BUILD_DIR}/play.o

# 计算play函数的hash，将其写入play_hash.h中
python3 calc_hash.py ${BUILD_DIR}/play.o play hash1_xor_rot > play_hash.h

python3 extract_func_code.py ${BUILD_DIR}/play.o play >> func_body.c

gcc ${OPTIMIZATION} -c func_body.c -o ${BUILD_DIR}/func_body.o 
gcc ${OPTIMIZATION} -c main.c -o ${BUILD_DIR}/main.o 

gcc ${OPTIMIZATION} -o drm ${BUILD_DIR}/main.o ${BUILD_DIR}/play.o ${BUILD_DIR}/get_key_and_decrypt.o ${BUILD_DIR}/func_body.o hash.c