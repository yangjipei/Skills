#!/bin/sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: create_prd_workdraft.sh <target-file>" >&2
  exit 1
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
workspace_root=$(CDPATH= cd -- "$script_dir/../../../.." && pwd)
prd_source_file="$workspace_root/06_Templates/PRD骨架.md"
supplement_source_file="$workspace_root/06_Templates/PRD补充信息骨架.md"
prd_target_file=$1
target_dir=$(dirname -- "$prd_target_file")
supplement_target_file="$target_dir/PRD补充信息-工作稿.md"

if [ -e "$prd_target_file" ]; then
  echo "Target already exists: $prd_target_file" >&2
  exit 2
fi

if [ -e "$supplement_target_file" ]; then
  echo "Target already exists: $supplement_target_file" >&2
  exit 2
fi

mkdir -p "$target_dir"
cp "$prd_source_file" "$prd_target_file"
cp "$supplement_source_file" "$supplement_target_file"
printf '%s\n' "$prd_target_file" "$supplement_target_file"
