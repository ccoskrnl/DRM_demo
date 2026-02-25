import struct

def hex_string_to_bytes(hex_str: str, endian: str = 'little') -> bytes:
    """Convert a hex string to bytes with specified endianness."""
    # Remove '0x' prefix if present
    hex_str = hex_str.lower().replace('0x', '')
    
    # Ensure even length
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str
    
    # Convert to bytes
    byte_data = bytes.fromhex(hex_str)
    
    # Apply endianness
    if endian.lower() == 'little':
        byte_data = byte_data[::-1]
    
    return byte_data

def parse_search_bytes(search_str: str) -> bytes:
    """Parse a search string like 'cc ef cd ab 78 56 34 12' to bytes."""
    # Remove any '0x' prefixes and spaces
    search_str = search_str.lower().replace('0x', '').replace(',', ' ')
    
    # Split and convert to integers
    hex_values = search_str.split()
    
    # Convert to bytes
    try:
        search_bytes = bytes(int(x, 16) for x in hex_values)
    except ValueError:
        raise ValueError(f"Invalid hex value in search string: {search_str}")
    
    return search_bytes

def find_and_replace_bytes(file_path: str, search_bytes: bytes, replace_bytes: bytes, 
                          replace_all: bool = False) -> bool:
    """
    Find and replace byte sequences in a binary file.
    
    Args:
        file_path: Path to the binary file
        search_bytes: Bytes sequence to search for
        replace_bytes: Bytes sequence to replace with
        replace_all: If True, replace all occurrences; if False, replace first only
    
    Returns:
        bool: True if at least one replacement was successful, False otherwise
    """
    try:
        # Read the entire file
        with open(file_path, 'rb') as f:
            file_data = bytearray(f.read())
        
        if len(search_bytes) != len(replace_bytes):
            print(f"Warning: Search bytes length ({len(search_bytes)}) doesn't match replacement length ({len(replace_bytes)})")
        
        replacements = 0
        pos = 0
        
        while True:
            # Find the position of search_bytes
            search_pos = file_data.find(search_bytes, pos)
            
            if search_pos == -1:
                break
            
            # Check if replacement will fit
            if search_pos + len(replace_bytes) > len(file_data):
                print(f"Warning: Replacement at position 0x{search_pos:x} would exceed file bounds")
                break
            
            # Replace the bytes
            file_data[search_pos:search_pos + len(search_bytes)] = replace_bytes
            replacements += 1
            
            print(f"Replaced {len(search_bytes)} bytes at position 0x{search_pos:x}")
            
            if not replace_all:
                break
            
            # Move position past this replacement
            pos = search_pos + len(replace_bytes)
        
        if replacements == 0:
            print(f"Error: Byte sequence {search_bytes.hex()} not found in file")
            return False
        
        # Write back to file
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        print(f"Successfully made {replacements} replacement(s)")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    hex_str = ""
    with open("get_key_hash.h", "r") as f:
        hash_hex_str = f.readline().strip()
        hex_str = hash_hex_str.split(' ')[2].strip()


    obj_file = "build/get_key_and_decrypt.o" 
    search_bytes = parse_search_bytes("cc ef cd ab 78 56 34 12")
    replace_bytes = hex_string_to_bytes(hex_str)
    
    
    success = find_and_replace_bytes(obj_file, search_bytes, replace_bytes, True)