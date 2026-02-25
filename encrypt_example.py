#!/usr/bin/env python3
import sys
import os

def xor_encrypt_8byte_blocks(data: bytes, key: bytes) -> bytes:
    """
    XOR encryption with 8-byte aligned data.
    Data is padded with 0x00 to be 8-byte aligned.
    Each 8-byte block is XORed with the key.
    """
    if not key or len(key) != 8:
        raise ValueError("Key must be exactly 8 bytes")
    
    # Pad data to be 8-byte aligned
    padding_len = (8 - (len(data) % 8)) % 8
    padded_data = data + b'\x00' * padding_len
    
    # Convert to bytearray for modification
    result = bytearray(padded_data)
    
    # Process in 8-byte blocks
    for i in range(0, len(padded_data), 8):
        block = padded_data[i:i+8]
        
        # XOR each byte in the block with corresponding key byte
        for j in range(8):
            result[i+j] = block[j] ^ key[j]
    
    return bytes(result)

def bytes_to_c_array(data: bytes, array_name: str = "encrypted_data") -> str:
    """Convert bytes to C array declaration."""
    hex_bytes = [f"0x{b:02x}" for b in data]
    
    # Format with 8 bytes per line for readability
    lines = []
    for i in range(0, len(hex_bytes), 8):
        line = ", ".join(hex_bytes[i:i+8])
        if i == 0:
            lines.append(f"uint8_t {array_name}[] = {{ {line},")
        elif i + 8 >= len(hex_bytes):
            lines.append(f"    {line}")
        else:
            lines.append(f"    {line},")
    
    lines.append("};")
    return "\n".join(lines)

def main():
    # Check arguments
    if len(sys.argv) != 2:
        print("Usage: python3 encrypt.py <8-byte-key>")
        print("Data is read from stdin")
        print("Example: echo 'ABCDABCDABCDABCDABCDABCDABCDABCD' | python3 encrypt.py SECRETKEY")
        sys.exit(1)
    
    # Get key
    key_str = sys.argv[1]
    if len(key_str) != 8:
        print(f"Error: Key must be exactly 8 bytes (got {len(key_str)} characters)")
        print("Note: If your key has special characters, make sure to quote it properly")
        sys.exit(1)
    
    key = key_str.encode('utf-8')
    
    # Read data from stdin
    if sys.stdin.isatty():
        print("Error: No data provided via stdin")
        print("Usage: echo 'data' | python3 encrypt.py KEY")
        sys.exit(1)
    
    data = sys.stdin.buffer.read()
    
    # Remove trailing newline if present
    if data.endswith(b'\n'):
        data = data.rstrip(b'\n')
    
    # Calculate padding information
    original_len = len(data)
    padding_len = (8 - (original_len % 8)) % 8
    padded_len = original_len + padding_len
    
    print(f"// Original data length: {original_len} bytes")
    print(f"// Padding added: {padding_len} bytes (0x00)")
    print(f"// Padded length: {padded_len} bytes (8-byte aligned)")
    
    # Encrypt data
    encrypted = xor_encrypt_8byte_blocks(data, key)
    
    # Output C array
    print(f"// Key: {key_str}")
    print(f"// XOR encrypted in 8-byte blocks")
    print()
    print(bytes_to_c_array(encrypted))
    
    # Optional: Show original data for debugging
    print()
    print("// Original data for reference:")
    print(f"// uint8_t original_data[] = {{", end="")
    for i, b in enumerate(data):
        if i > 0:
            print(", ", end="")
            if i % 8 == 0:
                print("\n//    ", end="")
        print(f"0x{b:02x}", end="")
    print("};")

if __name__ == "__main__":
    main()