# Hero Scene A/B Judging

Background: VIDEO_OUTLINE.md targets ~65s for NinetySevenDots, ~60s for
Pritchard30Teams, ~60s for ThreeNumbersReveal. All A versions render
significantly under spec (11s / 8.8s / 11s). All B versions render closer
to spec (19s / 45s / 50s). Visual punch and legibility were the deciding
factors below.

## Pair 1 — NinetySevenDots: **B wins**

Both versions land the basic visual, but A clips Pritchard's `+$4.3M NPV`
caption against the bottom edge of the frame (visible at 95% — the dollar
label is half-cut). B has a clean callout box with both name and NPV
inside the visible area, dims the 96 red dots so Pritchard pops harder,
and ends on the punchline cut — fading everything except Pritchard +
callout to center stage. B also breathes (longer suspense beat) and is
closer to the 65s narration window.

## Pair 2 — Pritchard30Teams: **B wins**

A is fatally short (8.8s vs ~60s spec) and the GSW callout text gets
clipped against the right frame edge (`$15…` truncated at 80% and 95%).
B introduces the tier color legend first (orienting the quant audience
before the numbers fly), animates bars in tier groups so the cap-tier
story reads at a glance, and ends with a curved bracket + "7x range" label
that directly visualizes the punchline. B's pacing (45s) sits much closer
to the narration window without rushing through 30 rows.

## Pair 3 — ThreeNumbersReveal: **B wins**

A has a real bug: the third number is rendered as "0" while the first two
count up (visible at 50% frame), and the final state at 95% shows the "x"
suffix wrapped onto the caption line ("x value range" reading awkwardly)
instead of attached as "7x" — the punchline number doesn't land. A also
runs 11s vs the ~60s narration window, so the three numbers blow past the
viewer. B reveals each number hero-scale with proper "%" and "x"
suffixes, then re-flows into a colored triplet with a unifying caption
("of 97 · % positive · 7x range"). The B pacing matches narration and
each number is visually anchored by a bucket-colored ribbon.

## Stitch flags

For the winning set, pass all three B flags:

```
bash stitch.sh --b97 --b30 --b3n
```
