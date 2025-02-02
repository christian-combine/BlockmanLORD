#!/bin/bash
SOURCE_DIR="${SOURCE_DIR:-armeabi-v7a}"
DEST_DIR="${DEST_DIR:-converted}"
mkdir -p "$SOURCE_DIR-def"
mkdir -p "$SOURCE_DIR-dll"
mkdir -p "$SOURCE_DIR-a"
mkdir -p "$DEST_DIR"
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory $SOURCE_DIR does not exist."
    exit 1
fi
SO_FILES=("$SOURCE_DIR"/*.so)
if [ ${#SO_FILES[@]} -eq 0 ] || [ ! -f "${SO_FILES[0]}" ]; then
    echo "No .so files found in $SOURCE_DIR"
    exit 1
fi
HOST_ARCH=$(uname -m)
TARGET_ARCH="arm"
if ! command -v arm-linux-gnueabi-gcc &> /dev/null; then
    echo "Cross-compilation tools not found. Attempting to install..."
    sudo apt-get update
    sudo apt-get install -y gcc-arm-linux-gnueabi binutils-arm-linux-gnueabi
fi
for SO_FILE in "${SO_FILES[@]}"; do
    if [ -f "$SO_FILE" ]; then
        BASENAME=$(basename "$SO_FILE" .so)
        DEF_FILE="$SOURCE_DIR-def/$BASENAME.def"
        DLL_FILE="$SOURCE_DIR-dll/$BASENAME.dll"
        LIB_FILE="$SOURCE_DIR-a/$BASENAME.a"
        FILE_INFO=$(file "$SO_FILE")
        if [[ ! "$FILE_INFO" =~ "ARM" ]]; then
            echo "Warning: $SO_FILE does not appear to be an ARM shared library. Skipping."
            continue
        fi
        echo "EXPORTS" > "$DEF_FILE"
        arm-linux-gnueabi-nm -D "$SO_FILE" | grep " T " | awk '{print $3}' >> "$DEF_FILE"
        arm-linux-gnueabi-ar rcs "$LIB_FILE" "$SO_FILE"
        arm-linux-gnueabi-gcc -shared \
            -o "$DLL_FILE" \
            "$SO_FILE" \
            "$LIB_FILE" \
            -Wl,--no-undefined

        if [ $? -eq 0 ]; then
            echo "Successfully converted $SO_FILE to $DLL_FILE"
        else
            echo "Failed to convert $SO_FILE. Check the library compatibility."
        fi
    fi
done
echo "Conversion process completed. Check results in $DEST_DIR."