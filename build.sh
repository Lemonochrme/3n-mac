#!/bin/bash

SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname "${SCRIPT_PATH}")

# Function to clean the build folder
gr_clean() {
  gr_path=$SCRIPT_DIR"/gr-"$1
  echo "[build.sh] Switching to 'gr-$1'..."
  cd $gr_path || return 1
  rm -rf build
}

gr_remove() {
  full_path=$SCRIPT_DIR"/gr-"$1"/build"
  echo "[build.sh] Switching to 'gr-$1/build'..."
  cd $full_path || return 1
  sudo make uninstall
  sudo ldconfig
}

# Function to compile a GNU component
gr_compile() {
  gr_path=$SCRIPT_DIR"/gr-"$1
  echo "[build.sh] Switching to 'gr-$1'..."
  cd $gr_path || return 1
  mkdir -p build
  cd build
  cmake ..
  cmake --build .
  sudo make install
  sudo ldconfig
}

# Check command line arguments
if [ "$1" == "compile" ]; then
  gr_compile $2
elif [ "$1" == "clean" ]; then
  gr_clean $2
elif [ "$1" == "remove" ]; then
  gr_remove $2
else
  echo -e $RED"Usage: $0 {compile|remove|clean}"$RESET
fi
