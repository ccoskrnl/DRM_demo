#!/usr/bin/env python3
"""
修复版：从可重定位目标文件(.o)中提取指定函数的机器码
"""

import sys
import argparse
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

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
        target_section = elf.get_section(section_index)
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

def bytes_to_c_array(bytes_data, array_name="func_body"):
    """将字节数据转换为C数组格式"""
    if not bytes_data:
        return ""
    
    hex_lines = []
    for i in range(0, len(bytes_data), 16):
        line_bytes = bytes_data[i:i+16]
        hex_strs = [f"0x{b:02x}" for b in line_bytes]
        hex_lines.append("    " + ", ".join(hex_strs))
    
    c_code = f"uint8_t {array_name}_COPY[] = {{\n"
    c_code += ",\n".join(hex_lines)
    c_code += "\n};\n"
    c_code += f"int {array_name}_SIZE = sizeof({array_name}_COPY);\n"
    
    return c_code

def main():
    parser = argparse.ArgumentParser(description='从.o文件中提取函数机器码')
    parser.add_argument('obj_file', help='可重定位目标文件 (.o)')
    parser.add_argument('func_name', help='要提取的函数名')
    parser.add_argument('--output', '-o', help='输出文件 (默认为标准输出)')
    parser.add_argument('--array-name', '-a', help='C数组名称')
    
    args = parser.parse_args()
    
    # 提取函数代码
    func_code = extract_function_from_object_file(args.obj_file, args.func_name)
    
    if not func_code:
        sys.exit(1)
    
    # 设置数组名
    array_name = args.array_name or f"{args.func_name}"
    
    # 生成C代码
    c_code = bytes_to_c_array(func_code, array_name)
    
    # 添加注释信息
    info = f"// 函数: {args.func_name}\n"
    info += f"// 文件: {args.obj_file}\n"
    info += f"// 大小: {len(func_code)} 字节\n\n"
    
    full_output = info + c_code
    
    # 输出
    if args.output:
        with open(args.output, 'w') as f:
            f.write(full_output)
        print(f"已写入: {args.output}")
    else:
        print(full_output)

if __name__ == "__main__":
    main()
