#!/usr/bin/env bash
set -euo pipefail

# Optimiza capturas PNG para web usando sips (macOS).
# Mantiene los originales en images/ y genera versiones ligeras en
# images/optimized/. Luego sincroniza width/height en
# _src/templates/index.html. Tras correrlo, ejecuta `python3 build.py` para
# que las nuevas dimensiones lleguen a las páginas generadas.
#
# Uso:
#   bash _src/scripts/optimize-images.sh
#   bash _src/scripts/optimize-images.sh <source_dir> <output_dir> <max_dimension>
#   bash _src/scripts/optimize-images.sh -h | --help

print_help() {
    cat <<'EOF'
Optimize screenshots for web delivery.

Usage:
  bash scripts/optimize-images.sh
  bash scripts/optimize-images.sh <source_dir> <output_dir> <max_dimension>

Arguments:
  source_dir      Input folder with screenshot*.png files
                  and optional "IPAD SCREENSHOT.png"
                  Default: ./images
  output_dir      Output folder for optimized PNG files
                  Default: ./images/optimized
  max_dimension   Longest side after resize (pixels)
                  Default: 1200

Examples:
  bash scripts/optimize-images.sh
  bash scripts/optimize-images.sh images images/optimized 1400

Notes:
  - Original files are never modified.
  - Requires macOS `sips`.
  - Updates width/height attributes in index.html after optimization.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    print_help
    exit 0
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE_DIR="${1:-"$ROOT_DIR/images"}"
OUTPUT_DIR="${2:-"$ROOT_DIR/images/optimized"}"
MAX_DIMENSION="${3:-1200}"

if ! command -v sips >/dev/null 2>&1; then
    echo "Error: 'sips' is required but not available in PATH."
    exit 1
fi

if ! [[ "$MAX_DIMENSION" =~ ^[0-9]+$ ]]; then
    echo "Error: max_dimension must be a positive integer. Received: $MAX_DIMENSION"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

shopt -s nullglob
files=("$SOURCE_DIR"/screenshot*.png)
shopt -u nullglob

ipad_source="$SOURCE_DIR/IPAD SCREENSHOT.png"
if [ -f "$ipad_source" ]; then
    files+=("$ipad_source")
fi

if [ ${#files[@]} -eq 0 ]; then
    echo "No screenshot PNG files or IPAD SCREENSHOT.png found in: $SOURCE_DIR"
    exit 1
fi

echo "Optimizing ${#files[@]} screenshots to max dimension ${MAX_DIMENSION}px..."

for source_path in "${files[@]}"; do
    file_name="$(basename "$source_path")"
    output_path="$OUTPUT_DIR/$file_name"

    cp "$source_path" "$output_path"
    sips -Z "$MAX_DIMENSION" "$output_path" >/dev/null

    width="$(sips -g pixelWidth "$output_path" | awk '/pixelWidth/ {print $2}')"
    height="$(sips -g pixelHeight "$output_path" | awk '/pixelHeight/ {print $2}')"
    size="$(ls -lh "$output_path" | awk '{print $5}')"

    echo "- $file_name -> ${width}x${height}, ${size}"
done

echo "Done. Optimized files written to: $OUTPUT_DIR"

UPDATE_SCRIPT="$ROOT_DIR/_src/scripts/update-image-dimensions.sh"
if [ -x "$UPDATE_SCRIPT" ]; then
    bash "$UPDATE_SCRIPT" "$ROOT_DIR/_src/templates/index.html" "$OUTPUT_DIR"
else
    echo "Warning: _src/scripts/update-image-dimensions.sh not found or not executable; width/height were not updated."
fi
