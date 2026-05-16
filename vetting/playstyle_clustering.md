# Decision — Playstyle Clustering and Matchup Analysis

**Date:** 2026-05-16
**Status:** **KILL** (as currently framed). Parked for potential reframe;
not added to `IDEAS.md`.

**TL;DR:** Five-persona panel and cursory research converge on the same
verdict — this is a saturated topic with a known null result, and the
strongest defensible reframe still ranks below `IDEAS.md` entries
#5 (Coach Effect) and #8 (Matchup-Data Audit) on every dimension that
matters: novelty, methodology defensibility, discoverability, and
expected effort. Build Coach Effect or Matchup Audit next instead.

---

## Persona heatmap

| Persona | Verdict | Strongest hook | Headline concern |
|---|---|---|---|
| Quant Discord | reframe → leaning kill | #2 (playoff exposure) | Whitehead null wall not breakable without scheme-interaction term, which requires non-public data |
| Sharp Bettor | reframe → leaning kill | #2 (playoff exposure) | Pure retrospective; matchup-matrix cells too sparse to size on |
| Casual Fan | click then tune out | #1 (championship list) | Wants named teams in first 30s; allergic to "clustering" |
| FO Insider | kill as pitched | Action-level reframe | Cluster IDs are fan/media reduction; defensive scheme blind spot is damning |
| YouTube Strategist | reframe → tier B+ at best | #2 (playoff exposure) | No news peg, no faces; thumbnails of dots get 40% CTR of faces |

**Vote tally:** 5 of 5 panelists kill or strongly reframe. 4 of 5
recommend pursuing `IDEAS.md` entries over this idea. 1 panelist (casual)
would click but predicts low watch-through.

---

## Convergence — where the panel agreed

1. **The v0 framing is dead.** Cluster-and-rank-by-championships has been
   done by Whitehead 2017, Whitehead 2021, Phillips, Goldsberry,
   Bruin Sports Analytics, dozens of Medium posts, multiple Sloan papers.
   The known result — *playstyle barely correlates with success; talent
   dominates* — is robust. Re-deriving it earns no respect.

2. **Hook #2 (playoff exposure) is the only defensible angle.** "Motion
   offenses lose 8 points of efficiency in playoffs, iso loses 2" has
   real bones if and only if it survives talent control. The quant,
   bettor, and strategist all converge here.

3. **The defensive scheme blind spot is load-bearing.** Drop/switch/blitz
   rates aren't public; BBall Index paywalled. Any video that clusters
   offenses but can't see defenses is solving half the problem. The FO
   insider was most damning: *"inside a building, defense IS the
   playstyle."*

4. **The matchup matrix is a vibe, not a finding.** 36 cells × ~150
   playoff series = 4–8 series per cell. Empirical Bayes shrinkage will
   pull every cell to ~50% with credible intervals straddling 0.5.
   Defensible to *render*, indefensible to *claim* at the cell level.

5. **K-selection methodology is the silent killer.** Silhouette + gap
   stat + bootstrap stability gets you to "K is statistically
   defensible." It does not get you to "K is real." The Hopkins
   statistic continuity test (quant panel) and adjusted Rand Index
   between K-means and GMM solutions are the actual bars. Team styles
   almost certainly live on a continuum — K-anything is then a lie
   about the geometry.

6. **No discoverability hook.** No news peg, no named player in the
   title, no controversy. Algorithm has nothing to latch onto. Strategist
   ranks this below tracking-data video (#6) and ring-chase tax (#10).

---

## Divergence — the real creative tension

**Casual fan picks Hook #1. The other four panelists call Hook #1 the
most dunkable.**

This is genuine. What sells (a list video with stakes: "every champion
since 2015 falls into 2 of 6 clusters") is exactly what the methodology
audience will eat alive (pigeonhole bias: n=10 champions, K=6, almost
forced result).

Two ways to resolve:

- **Lead casual, hide quant**: open with Hook #1 framing for the click,
  then pivot the actual finding mid-video to the playoff-exposure angle
  the quants will defend. Risk: the Discord still sees the title and
  posts the dunk-tweet before watching.
- **Lead quant, lose casual**: Hook #2 only, with named teams sprinkled
  in. Lower CTR ceiling, but defensible.

**FO insider proposed dropping clustering entirely.** Action-level claim
instead: "5-out offenses with a non-shooting 5 collapse against teams
that switch 1-5." This is *action × coverage × personnel* — a
fundamentally different video. Not clustering at all. The FO insider
called this the only version that wouldn't get smirk-emoji'd by his GM.

---

## What would have to be true for this to survive

The reframed (Hook #2-only, action-level) version is conditionally
viable if **all** of the following hold:

1. EDA spike (1–2 weeks) shows playoff-vs-RS efficiency delta ≥ 6 points
   between clusters after **rigorous talent control** (top-8 EPM by
   minutes + Vegas win total + opponent talent).
2. The cluster solution passes Hopkins continuity test and ARI ≥ 0.7
   between K-means and GMM.
3. At least one finding can be operationalized as an *action × coverage*
   claim, not just a style aggregate — so the FO insider's mechanism
   critique is addressed even without public defensive scheme data.
4. The video opens by explicitly naming the defensive-scheme blind spot
   ("I can only see offense — here's what that limits") in the first
   90 seconds.

If any condition fails, kill.

Even if all four conditions hold, the strategist's analysis suggests
this still ranks below Coach Effect (#5) and Matchup Audit (#8) by
expected views ceiling — so the decision becomes "build it because I
care, not because it's the highest-ROI next video."

---

## Decision

**Kill for now.** Parked at `vetting/playstyle_clustering.md` (this
file). Not added to `IDEAS.md`.

If you want to revisit later, the trigger is: a specific NBA Finals
matchup or storyline that gives this a news peg (e.g., a movement
team gets bounced in round 2 by a switch-heavy defense in 2026 or
2027), combined with a willingness to commit to the action-level
reframe.

**Recommended next videos** (in order, per panel consensus):

1. **Idea 5 — The Coach Effect.** 3 weeks, replicable JQAS 2025 paper
   does the methodology, Nick Nurse +20 wins is a thumbnail.
2. **Idea 8 — Whose Defense Is Real?** 3 weeks, novel API use, named-
   player reveals ("Jrue is 90% real, Anunoby is 60%"), Discord-postable.
3. **Idea 3 — Tanking → Trade Chips.** 4 weeks, strongest title on the
   docket per the original 10-idea panel.

---

## Source materials

- v0 idea card: [`playstyle_clustering_v0.md`](playstyle_clustering_v0.md)
- Cursory research: ran inline in conversation 2026-05-16; key finding
  was the Whitehead null wall and the playoff-exposure reframe as the
  only defensible angle.
- Persona transcripts: agent task IDs `a890bd79b1ffa1408` (quant),
  `a79e17138bc38df63` (bettor), `ad4e33cfc953e81a9` (casual),
  `ac7826df1ccbf7a52` (FO), `ab84f5ffbcf879a3b` (strategist). Saved at
  `/tmp/claude-1000/.../tasks/<id>.output`.

## Methodology applied

See [`../METHODOLOGY.md`](../METHODOLOGY.md). This was a Stage 1–4 run.
Stage 5 (deep research) was skipped on the kill verdict — no point
sharpening a number for an idea we're not building.
