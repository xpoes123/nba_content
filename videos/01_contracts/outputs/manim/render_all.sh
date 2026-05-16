#!/usr/bin/env bash
# Render every scene. Pass quality flag: l (low/preview), m (medium), h (high).
# Defaults to low. Failures are logged but don't stop the run.
set -uo pipefail
cd "$(dirname "$0")"

QUALITY="${1:-l}"
PYTHON=/home/david/code/sports/nba_contracts/.venv/bin/python

SCENES=(
    "scenes/cold_open.py ColdOpenNames"
    "scenes/cold_open.py ColdOpenStat"
    "scenes/segment_1_buckets.py FourBuckets"
    "scenes/segment_1_buckets.py JokicCap"
    "scenes/segment_1_buckets.py BuildTheFormula"
    "scenes/segment_2_killer.py NinetySevenDots"
    "scenes/segment_2_killer_b.py NinetySevenDotsB"
    "scenes/segment_2_killer.py BucketPositiveShare"
    "scenes/segment_3_story.py PritchardTimeline"
    "scenes/segment_3_story.py ThreeReasonsCallout"
    "scenes/segment_4_method.py PriceFitScatter"
    "scenes/segment_4_method.py AgingCurve"
    "scenes/segment_4_method.py MultiplierStack"
    "scenes/segment_5_worst.py BottomFiveBars"
    "scenes/segment_5_worst.py MobleyAnnotation"
    "scenes/segment_5_worst.py MaxOnApronPattern"
    "scenes/segment_6_prit30.py Pritchard30Teams"
    "scenes/segment_6_prit30_b.py Pritchard30TeamsB"
    "scenes/segment_6_prit30.py SevenTimesCallout"
    "scenes/segment_7_next.py NextPritchardCalendar"
    "scenes/segment_7_next.py QuetaSpotlight"
    "scenes/segment_7_next.py DurenForecast"
    "scenes/segment_7_next.py DiabateUnderRadar"
    "scenes/segment_8_close.py ThreeNumbersReveal"
    "scenes/segment_8_close_b.py ThreeNumbersRevealB"
    "scenes/segment_8_close.py FinalQuestion"
)

mkdir -p logs
FAIL=0
PASS=0
for entry in "${SCENES[@]}"; do
    read -r file class <<< "$entry"
    log="logs/${class}.log"
    echo "→ rendering $class"
    if "$PYTHON" -m manim -q "$QUALITY" "$file" "$class" > "$log" 2>&1; then
        echo "  ✓ $class"
        PASS=$((PASS+1))
    else
        echo "  ✗ $class — see $log"
        FAIL=$((FAIL+1))
    fi
done

echo ""
echo "──────────────────"
echo "✓ $PASS passed"
echo "✗ $FAIL failed"
