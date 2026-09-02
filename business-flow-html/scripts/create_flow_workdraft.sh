#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: create_flow_workdraft.sh <target-file>" >&2
  exit 1
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_file="$script_dir/../references/reference-business-flow-v3.html"
target_file=$1

if [ -e "$target_file" ]; then
  echo "Target already exists: $target_file" >&2
  exit 2
fi

mkdir -p "$(dirname -- "$target_file")"
cp "$source_file" "$target_file"
printf '%s\n' "$target_file"
