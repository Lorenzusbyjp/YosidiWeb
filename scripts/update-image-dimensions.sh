#!/usr/bin/env bash
set -euo pipefail

# Actualiza width/height en index.html para las imágenes de images/optimized/.
#
# Uso:
#   bash scripts/update-image-dimensions.sh
#   bash scripts/update-image-dimensions.sh <html_file> <optimized_dir>

print_help() {
    cat <<'EOF'
Update width/height attributes in HTML for optimized screenshots.

Usage:
  bash scripts/update-image-dimensions.sh
  bash scripts/update-image-dimensions.sh <html_file> <optimized_dir>

Arguments:
  html_file       HTML file to update
                  Default: ./index.html
  optimized_dir   Directory containing screenshot*.png optimized files
                  and optional "IPAD SCREENSHOT.png"
                  Default: ./images/optimized
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    print_help
    exit 0
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HTML_FILE="${1:-"$ROOT_DIR/index.html"}"
OPTIMIZED_DIR="${2:-"$ROOT_DIR/images/optimized"}"

if ! command -v sips >/dev/null 2>&1; then
    echo "Error: 'sips' is required but not available in PATH."
    exit 1
fi

if ! command -v perl >/dev/null 2>&1; then
    echo "Error: 'perl' is required but not available in PATH."
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: HTML file not found: $HTML_FILE"
    exit 1
fi

if [ ! -d "$OPTIMIZED_DIR" ]; then
    echo "Error: optimized images directory not found: $OPTIMIZED_DIR"
    exit 1
fi

shopt -s nullglob
files=("$OPTIMIZED_DIR"/screenshot*.png)
shopt -u nullglob

ipad_optimized="$OPTIMIZED_DIR/IPAD SCREENSHOT.png"
if [ -f "$ipad_optimized" ]; then
    files+=("$ipad_optimized")
fi

if [ ${#files[@]} -eq 0 ]; then
    echo "No screenshot PNG files or IPAD SCREENSHOT.png found in: $OPTIMIZED_DIR"
    exit 1
fi

echo "Updating width/height attributes in $(basename "$HTML_FILE")..."

for image_path in "${files[@]}"; do
    image_name="$(basename "$image_path")"

    # Skip images that are not currently referenced in HTML.
    if ! rg -q "src=\"\\./images/optimized/${image_name}\"" "$HTML_FILE"; then
        echo "- $image_name -> not referenced in HTML (skipped)"
        continue
    fi

    width="$(sips -g pixelWidth "$image_path" | awk '/pixelWidth/ {print $2}')"
    height="$(sips -g pixelHeight "$image_path" | awk '/pixelHeight/ {print $2}')"

    IMAGE_NAME="$image_name" IMG_WIDTH="$width" IMG_HEIGHT="$height" perl -0777 -i -pe '
        my $count = s{
            (<img\b[^>]*\bsrc="\./images/optimized/\Q$ENV{IMAGE_NAME}\E"[^>]*\bwidth=")\d+("\s+height=")\d+(")
        }{$1.$ENV{IMG_WIDTH}.$2.$ENV{IMG_HEIGHT}.$3}gex;

        if ($count == 0) {
            die "No width/height attributes found for $ENV{IMAGE_NAME}. Ensure width and height are present in HTML.\n";
        }
    ' "$HTML_FILE"

    echo "- $image_name -> width=$width height=$height"
done

echo "Done. Updated dimensions in: $HTML_FILE"
