import os
import sys

def create_header_with_so_files(directory, output_file):
    so_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".so"):
                so_files.append(os.path.relpath(os.path.join(root, file), directory))
    with open(output_file, 'w') as hpp_file:
        header_guard = f"ALL_SO_FILES_HPP"
        hpp_file.write(f"#ifndef {header_guard}\n")
        hpp_file.write(f"#define {header_guard}\n\n")
        hpp_file.write("// Header file with all shared object (.so) filenames\n\n")
        hpp_file.write("// Blockman Launcher NEXT\n")
        hpp_file.write("namespace SharedObjects {\n")
        hpp_file.write("    const char* so_files[] = {\n")
        for so_file in so_files:
            hpp_file.write(f"        \"{so_file}\",\n")
        hpp_file.write("    };\n")
        hpp_file.write("    const size_t so_files_count = sizeof(so_files) / sizeof(so_files[0]);\n")
        hpp_file.write("}\n\n")
        hpp_file.write(f"#endif // {header_guard}\n")
    print(f"Header file created: {output_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python create_header_with_so_files.py <directory> <output_file.hpp>")
        sys.exit(1)
    directory = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)
    create_header_with_so_files(directory, output_file)

if __name__ == "__main__":
    main()