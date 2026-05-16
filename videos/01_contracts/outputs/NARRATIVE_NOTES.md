# NARRATIVE_NOTES.md — companion to FINAL_MASTER.mp4

This is a silent rough cut. Narration goes on top in post. Scene timings below
are silent-clip durations; the script timing column shows the target spoken
window from `VIDEO_OUTLINE.md`. Most scenes are tighter than the script window
on purpose — the editor pads with holds + camera/narration breathing.

## Tooling pointers
- Re-render any one scene: `cd outputs/manim && /home/david/code/sports/nba_contracts/.venv/bin/python -m manim -q l scenes/<file>.py <Class>`
- Re-render all at low quality: `bash outputs/manim/render_all.sh l` (~3 min total)
- Re-render at HIGH quality for delivery: `bash outputs/manim/render_all.sh h` (slow — ~30 min)
- Re-stitch master: `bash outputs/manim/stitch.sh` (A defaults) or with `--b97 --b30 --b3n` flags for B variants

## Scene log (narrative order)

| # | Class | Script window | Narration cue |
|--:|---|---|---|
| 1 | ColdOpenNames | 0:00–0:18 | "Every basketball channel makes the same video. Top 15 best contracts in the NBA. The names rotate — Jokić, Brunson, SGA, Wemby — but the list is always the same." |
| 2 | ColdOpenStat | 0:18–0:45 | "So I built a model. Every contract in the NBA, 472 of them, priced against the open-market shadow rate ... Here's the punchline: of 97 contracts that GMs actually negotiated, exactly one will deliver positive value." |
| 3 | FourBuckets | 0:45–1:45 | "Every NBA contract falls into one of four buckets. Three of them are set by the CBA before any GM picks up the phone..." |
| 4 | JokicCap | 1:45–2:10 | "Jokić would make a hundred million on an open market. The CBA forbids more than fifty-five." |
| 5 | BuildTheFormula | 2:10–2:45 | "Composite Wins Added — VORP converted to wins, plus Win Shares. Regression line fit only on open-negotiation contracts ... Four point eight six million per standard deviation." |
| 6 | NinetySevenDots (A or B) | 2:45–3:50 | THE moment. "Then ask: how many are projected positive? ... One. Payton Pritchard." |
| 7 | BucketPositiveShare | 3:50–4:30 | "Veteran minimum deals: fifty-five percent projected positive. The CBA's mandated floor produces more good contracts than every GM combined." |
| 8 | PritchardTimeline | 4:30–5:30 | "October 8th, 2023. Brad Stevens signs Payton Pritchard to a four-year, thirty-million-dollar extension." |
| 9 | ThreeReasonsCallout | 5:30–6:45 | "Three reasons — extended before breakout, length compounds, price anchored LOW (Avdija/J.Johnson also pre-breakout but at market price → still net-negative)." |
| 10 | PriceFitScatter | 6:45–7:25 | "Four point eight six million dollars per standard deviation of production, fit on open-negotiation contracts only." |
| 11 | AgingCurve | 7:25–7:55 | "Population aging curve. Peak at twenty-six, seven-eight percent decline per year." |
| 12 | MultiplierStack | 7:55–8:15 | "On a tax team, $1.50. On a second-apron team, three and a half." |
| 13 | BottomFiveBars | 8:15–9:15 | "Bottom five contracts ... Mobley negative $642M effective, then Jaylen Brown, Dončić, Edwards, Mitchell." |
| 14 | MobleyAnnotation | 9:15–9:45 | "Mobley is the worst contract in the league. He's a top-thirty player. He's twenty-four years old. Five-year max in year one." |
| 15 | MaxOnApronPattern | 9:45–10:00 | "Every bottom-5 contract: max deal on an apron team." |
| 16 | Pritchard30Teams (A or B) | 10:00–11:00 | "Same player, same contract. Thirty different team contexts." |
| 17 | SevenTimesCallout (now displays "6x") | 11:00–11:30 | "Six times the value, same contract, two different teams." |
| 18 | NextPritchardCalendar | 11:30–12:15 | "The model says three names to watch." |
| 19 | QuetaSpotlight | 12:15–12:40 | "Neemias Queta. Boston Celtics. Twenty-six years old. Top-thirty defense for $2.3M." |
| 20 | DurenForecast | 12:40–13:05 | "Jalen Duren. Detroit. They missed the Oct 2025 extension deadline — he's an RFA in Summer 2026." |
| 21 | DiabateUnderRadar | 13:05–13:30 | "Moussa Diabaté. Charlotte. The under-the-radar pick." |
| 22 | ThreeNumbersReveal (A or B) | 13:30–14:30 | "Three numbers to take with you." |
| 23 | FinalQuestion | 14:30–15:00 | "Did the GM negotiate this? Or did the CBA? Almost always, it was the CBA." |

## A/B winners (final cut uses B for all 3)
The judge sweep picked **all three B versions** (see `outputs/manim/judging_results.md` for keyframe-by-keyframe rationale). Summary:
- **NinetySevenDots → B**: A clips the NPV caption off-screen and runs only 11s vs the 65s window; B has a clean callout box, dims red dots, and ends on an isolated "Pritchard alone" punchline frame.
- **Pritchard30Teams → B**: A renders only 8.8s (broken timing) with the top callout clipped at the right edge; B groups bars by tier, draws a curved 6× bracket between CLE and BRK. (Re-rendered with v4.1 corrected tiers — CLE is now top, GSW dropped to first-apron.)
- **ThreeNumbersReveal → B**: A has a rendering bug where the third number reads "0" mid-count and the "x" suffix wraps onto the caption line; B does proper hero-scale reveals with `%` and `x` suffixes baked into the big glyph.

To regenerate the master with these picks:
```
bash outputs/manim/stitch.sh --b97 --b30 --b3n
```

If editorially you want to test A variants for any of those, drop the corresponding flag.

## Known caveats
- Silent video. Pacing inside each scene is animation-density, not narration-density. The editor will hold beats during voiceover.
- Some text uses ASCII fallbacks (e.g. "Diabate" without the é, "7x" instead of "7×") because the project's default Inter font fallback was inconsistent on combining diacritics.
- Axis tick labels are placed manually as Text mobjects (LaTeX is not installed in this env).
- The B version of NinetySevenDots ends with a "Pritchard alone" punchline frame that's especially nice if the editor wants to land hard on the "Just one." narration.
