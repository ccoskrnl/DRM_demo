from cffi import FFI
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

ffi = FFI()
libhash = ffi.dlopen("./libhash.so")

ffi.cdef("""
        typedef uint64_t* addr_t;
        uint64_t hash1_xor_rot(addr_t addr, long size);
        uint64_t hash2_fnv1(addr_t addr, long size);
        uint64_t hash3_jenkins(addr_t addr, long size);
""")

def func_name_with_hash_func(filename: str) -> list[tuple[str, str]]:
    func_name_map: List[Tuple[str, str]] = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            func_name_map += [tuple(line.split(' '))]

    return func_name_map

def extract_function_from_object_file(obj_file, func_name):

    """从可重定位目标文件中提取函数机器码"""
    
    with open(obj_file, 'rb') as f:
        elf = ELFFile(f)
        
        # 寻找符号表
        symtab = None
        for section in elf.iter_sections():
            if isinstance(section, SymbolTableSection):
                symtab = section
                break
        
        if not symtab:
            print(f"错误: {obj_file} 中没有符号表")
            return None
        
        # 查找函数符号
        func_symbol = None
        for symbol in symtab.iter_symbols():
            if symbol.name == func_name:
                func_symbol = symbol
                break
        
        if not func_symbol:
            print(f"错误: 未找到函数 '{func_name}'")
            return None
        
        # 检查是否是函数
        if func_symbol.entry['st_info']['type'] != 'STT_FUNC':
            print(f"警告: '{func_name}' 不是函数类型")
        
        # 获取函数大小和所在节的索引
        func_size = func_symbol.entry['st_size']
        section_index = func_symbol.entry['st_shndx']
        
        # 检查是否是未定义的符号
        if section_index == 'SHN_UNDEF':
            print(f"错误: 函数 '{func_name}' 未定义")
            return None
        
        if func_size == 0:
            print(f"错误: 函数 '{func_name}' 大小为0")
            return None
        
        # 找到函数所在的节
        target_section : 'Section' = elf.get_section(section_index)
        if not target_section:
            print(f"错误: 找不到函数所在的节")
            return None
        
        # 在可重定位文件中，st_value 是节内的偏移量
        func_offset = func_symbol.entry['st_value']
        
        # 读取函数代码
        section_data = target_section.data()
        
        # 确保偏移量和大小在节数据范围内
        if func_offset + func_size > len(section_data):
            print(f"错误: 函数偏移超出节范围")
            print(f"节大小: {len(section_data)}, 函数偏移: {func_offset}, 函数大小: {func_size}")
            return None
        
        # 提取函数机器码
        func_code = section_data[func_offset:func_offset + func_size]
        
        return func_code

def calculate_hash(obj_file_name, func_name, hash_func_name):
    func_code = extract_function_from_object_file(obj_file_name, func_name)
    if func_code is None:
        return None
    
    # 将函数机器码转换为CFFI可接受的格式
    func_code_array = ffi.new("uint8_t[]", func_code)
    
    # 调用hash函数计算hash值
    hash_func = getattr(libhash, hash_func_name)
    hash_value = hash_func(ffi.cast("addr_t", func_code_array), len(func_code))
    
    return hash_value

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("用法: python calc_hash.py <object_file> <function_name> <hash_function>")
        print("示例: python calc_hash.py get_key_and_decrypt.o get_key hash1_xor_rot")
        sys.exit(1)
    
    obj_file = sys.argv[1]
    func_name = sys.argv[2]
    hash_func_name = sys.argv[3]
    
    hash_value = calculate_hash(obj_file, func_name, hash_func_name)
    if hash_value is not None:
        print(f"#define {func_name}_HASH {hash_value:#x}")