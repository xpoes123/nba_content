#!/usr/bin/env bash
# Concatenate rendered scene MP4s in narrative order.
# Usage:
#   bash stitch.sh                       # uses A versions for hero scenes
#   bash stitch.sh --b97                 # use B for NinetySevenDots
#   bash stitch.sh --b30                 # use B for Pritchard30Teams
#   bash stitch.sh --b3n                 # use B for ThreeNumbersReveal
#   (flags combinable)
# Output: ../FINAL_MASTER.mp4 (relative to outputs/manim/)
set -euo pipefail
cd "$(dirname "$0")"

USE_B97=0
USE_B30=0
USE_B3N=0
for arg in "$@"; do
    case "$arg" in
        --b97) USE_B97=1 ;;
        --b30) USE_B30=1 ;;
        --b3n) USE_B3N=1 ;;
        *) echo "Unknown arg: $arg" >&2; exit 1 ;;
    esac
done

# Pick scene-file directory and class for each hero scene
if [[ $USE_B97 -eq 1 ]]; then NIN_DIR="segment_2_killer_b"; NIN_CLASS="NinetySevenDotsB"
else NIN_DIR="segment_2_killer"; NIN_CLASS="NinetySevenDots"; fi
if [[ $USE_B30 -eq 1 ]]; then P30_DIR="segment_6_prit30_b"; P30_CLASS="Pritchard30TeamsB"
else P30_DIR="segment_6_prit30"; P30_CLASS="Pritchard30Teams"; fi
if [[ $USE_B3N -eq 1 ]]; then T3N_DIR="segment_8_close_b"; T3N_CLASS="ThreeNumbersRevealB"
else T3N_DIR="segment_8_close"; T3N_CLASS="ThreeNumbersReveal"; fi

# Narrative order: (dir, class)
SCENES=(
    "cold_open ColdOpenNames"
    "cold_open ColdOpenStat"
    "segment_1_buckets FourBuckets"
    "segment_1_buckets JokicCap"
    "segment_1_buckets BuildTheFormula"
    "$NIN_DIR $NIN_CLASS"
    "segment_2_killer BucketPositiveShare"
    "segment_3_story PritchardTimeline"
    "segment_3_story ThreeReasonsCallout"
    "segment_4_method PriceFitScatter"
    "segment_4_method AgingCurve"
    "segment_4_method MultiplierStack"
    "segment_5_worst BottomFiveBars"
    "segment_5_worst MobleyAnnotation"
    "segment_5_worst MaxOnApronPattern"
    "$P30_DIR $P30_CLASS"
    "segment_6_prit30 SevenTimesCallout"
    "segment_7_next NextPritchardCalendar"
    "segment_7_next QuetaSpotlight"
    "segment_7_next DurenForecast"
    "segment_7_next DiabateUnderRadar"
    "$T3N_DIR $T3N_CLASS"
    "segment_8_close FinalQuestion"
)

CONCAT=$(mktemp)
MISSING=0
for entry in "${SCENES[@]}"; do
    read -r dir class <<< "$entry"
    hi="media/videos/${dir}/1080p60/${class}.mp4"
    lo="media/videos/${dir}/480p15/${class}.mp4"
    if   [[ -f "$hi" ]]; then target="$hi"
    elif [[ -f "$lo" ]]; then target="$lo"
    else
        echo "✗ MISSING: $class" >&2
        MISSING=$((MISSING+1))
        continue
    fi
    abs=$(readlink -f "$target")
    echo "file '$abs'" >> "$CONCAT"
done

if [[ $MISSING -gt 0 ]]; then
    echo "⚠️  $MISSING scenes missing — stitching what we have." >&2
fi

OUT="../FINAL_MASTER.mp4"
echo "→ ffmpeg concat → $OUT"
# Try fast copy first; if streams differ, fall back to re-encode
if ! ffmpeg -y -f concat -safe 0 -i "$CONCAT" -c copy "$OUT" 2>/dev/null; then
    echo "  copy mode failed (streams differ?); re-encoding"
    ffmpeg -y -f concat -safe 0 -i "$CONCAT" -c:v libx264 -preset fast -crf 23 "$OUT" 2>&1 | tail -3
fi

echo "✓ master: $(readlink -f "$OUT")"
rm "$CONCAT"
