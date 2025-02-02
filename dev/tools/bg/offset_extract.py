import sys
import os
import subprocess
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

def demangle(symbol_name):
    try:
        result = subprocess.run(['c++filt', symbol_name], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error demangling symbol '{symbol_name}': {e}")
        return symbol_name 

def extract_offsets(so_file):
    offsets = []
    with open(so_file, 'rb') as f:
        elf = ELFFile(f)
        for section in elf.iter_sections():
            if isinstance(section, SymbolTableSection):
                for symbol in section.iter_symbols():
                    symbol_name = symbol.name
                    symbol_value = symbol['st_value']
                    if symbol_value != 0:
                        demangled_name = demangle(symbol_name)
                        offsets.append((demangled_name, symbol_value))
                    else:
                        demangled_name = demangle(symbol_name)
                        offsets.append((demangled_name, symbol_value))
    return offsets

def save_offsets_to_header(output_folder, so_file, offsets):
    header_file = os.path.join(output_folder, os.path.splitext(os.path.basename(so_file))[0] + ".hpp")
    os.makedirs(output_folder, exist_ok=True)
    with open(header_file, 'w') as h_file:
        header_guard = f"OFFSET_{os.path.basename(header_file).upper().replace('.', '_')}_HPP"
        h_file.write(f"#ifndef {header_guard}\n")
        h_file.write(f"#define {header_guard}\n\n")
        h_file.write("// Offsets extracted from {}\n".format(so_file))
        h_file.write("// Blockman Launcher NEXT\n")
        h_file.write("#include <string>\n")
        h_file.write("#include <stdexcept>\n")
        h_file.write("#include <new>\n")
        h_file.write("#include <type_traits>\n")
        h_file.write("#include <memory>\n")
        h_file.write("#include <cstddef>\n")
        h_file.write("#include <iostream>\n")
        h_file.write("#include <exception>\n")
        h_file.write("#include <functional>\n")
        h_file.write("#include <vector>\n")
        h_file.write("#include <unordered_map>\n")
        h_file.write("#include <unordered_set>\n")
        h_file.write("#include <map>\n")
        h_file.write("#include <set>\n")
        h_file.write("#include <list>\n")
        h_file.write("#include <array>\n")
        h_file.write("#include <queue>\n")
        h_file.write("#include <stack>\n")
        h_file.write("#include <deque>\n")
        h_file.write("#include <tuple>\n")
        h_file.write("#include <utility>\n")
        h_file.write("#include <algorithm>\n")
        h_file.write("#include <atomic>\n")
        h_file.write("#include <mutex>\n")
        h_file.write("#include <thread>\n")
        h_file.write("#include <future>\n")
        h_file.write("#include <chrono>\n")
        h_file.write("#include <condition_variable>\n")
        h_file.write("#include <semaphore>\n")
        h_file.write("#include <barrier>\n")
        h_file.write("#include <optional>\n")
        h_file.write("#include <variant>\n")
        h_file.write("#include <any>\n")
        h_file.write("#include <filesystem>\n")
        h_file.write("#include <limits>\n")
        h_file.write("#include <locale>\n")
        h_file.write("#include <codecvt>\n")
        h_file.write("#include <regex>\n")
        h_file.write("#include <atomic>\n")
        h_file.write("#pragma GCC diagnostic push\n")
        h_file.write("#pragma GCC diagnostic ignored \"-fpermissive\"\n")
        h_file.write("#pragma GCC diagnostic ignored \"-Wunused-variable\"\n")
        h_file.write("#pragma once\n\n")
        h_file.write("namespace Offsets {\n")
        for idx, symbol in enumerate(offsets):
            name = symbol[0]  
            address = hex(symbol[1])  
            h_file.write(f"    const uintptr_t {name} = {address};\n")
        h_file.write("}\n")
        h_file.write("#endif // {}\n".format(header_guard))
    print(f"Offsets saved to {header_file}")
    return header_file 

def create_all_offsets_header(output_folder, all_offsets_file):
    with open(all_offsets_file, 'w') as all_offsets:
        all_offsets.write("// Automatically generated header including all offsets\n\n")
        for root, _, files in os.walk(output_folder):
            for file in files:
                if file.endswith('.hpp'):
                    relative_path = os.path.relpath(os.path.join(root, file), output_folder)
                    all_offsets.write(f'#include "{relative_path}"\n')
    print(f"all_offsets.hpp generated with all includes at {all_offsets_file}")

def process_file(output_folder, so_file):
    offsets = extract_offsets(so_file)
    if not offsets:
        print(f"No offsets found in {so_file}.")
        return
    header_file = save_offsets_to_header(output_folder, so_file, offsets)
    return header_file

def process_directory(directory):
    output_folder = f"{directory}-offsets"
    os.makedirs(output_folder, exist_ok=True)
    all_offsets_file = os.path.join(output_folder, 'offsets.hpp') 
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.so'):
                so_file = os.path.join(root, file)
                print(f"Processing {so_file}...")
                process_file(output_folder, so_file)
    create_all_offsets_header(output_folder, all_offsets_file)

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_offsets.py <path_to_file_or_directory>")
        sys.exit(1)
    path = sys.argv[1]
    if os.path.isfile(path) and path.endswith('.so'):
        output_folder = os.path.dirname(path) + "-offsets"
        os.makedirs(output_folder, exist_ok=True)
        process_file(output_folder, path)
        create_all_offsets_header(output_folder, os.path.join(output_folder, 'all_offsets.hpp'))
    elif os.path.isdir(path):
        process_directory(path)
    else:
        print("Please provide a valid .so file or directory containing .so files.")
        sys.exit(1)

if __name__ == "__main__":
    main()