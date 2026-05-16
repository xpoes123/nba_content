# v0 — Playstyle Clustering and Matchup Analysis

*Pitched 2026-05-16. v0 idea card for persona pressure-testing.*

## Hook candidates

1. **"Every NBA champion since 2015 falls into 2 of 6 playstyle clusters. Here
   are the other four that have never won."** — championship-rate framing.
2. **"Motion-heavy offenses lose 8 points of efficiency in the playoffs.
   Iso-heavy offenses lose 2. The NBA playoffs systematically punish
   movement."** — playoff-exposure framing (recommended by the cursory
   research pass as the most defensible angle).
3. **"The NBA had 8 viable playstyles in 2014. By 2024 it had 4. The meta
   has compressed faster than anyone realized."** — compression-of-the-meta
   framing.

## Channel fit

- Manim-native: cluster scatters animating in, matchup matrices, compression
  over time as a morph.
- Primer-style intuition build for high-dimensional clustering.
- Continues the "methodology-first" register of the contracts video.

## Data sources

- `nba_api.SynergyPlayTypes` — 10 possession-type frequencies per team per
  season, coverage 2015-16+. The richest team-style fingerprint.
- `nba_api.LeagueDashTeamStats` — four factors + pace.
- `hoop-math.com` — shot location splits (rim / mid / corner-3 / above-break).
- Basketball-Reference — playoff series outcomes for matchup matrix.

## Methodology sketch

- **Feature space (Tier 1+2 per the cursory research):** Synergy possession
  types + four factors (offense and defense) + shot location mix. Skip
  defensive scheme tagging — Second Spectrum data not public.
- **Window:** 2015-16 to 2024-25 (~300 team-seasons).
- **Era normalization:** z-score within season before clustering.
- **Embedding:** UMAP for visualization. **Clustering:** K-means / GMM with
  K selected via silhouette + gap statistic + bootstrap stability over K=3
  through K=8.
- **Outcomes:** championship rate per cluster, playoff-vs-RS efficiency
  delta per cluster, 6×6 matchup matrix from ~150 playoff series since 2015
  with empirical Bayes shrinkage.
- **Talent control:** regress out preseason Vegas win total or aggregate
  EPM/RAPTOR talent before crediting any finding to "playstyle."

## Risks

- **Saturated topic.** Nylon Calculus (Whitehead 2017, 2021), Owen Phillips
  (snowflakes, matchup mashup), Goldsberry's *Sprawlball* + *Hoop Atlas*,
  multiple Sloan papers, Bruin Sports Analytics tutorial, dozens of Medium
  posts.
- **Known null result.** Whitehead's 2021 piece concluded playstyle barely
  correlates with success — talent dominates. If we re-derive this
  honestly the headline is "playstyle doesn't matter much."
- **Sparse matchup cells.** 6×6 cluster matrix on 150 playoff series → 4–8
  series per cell. Easy for a skeptic to dismantle without proper
  uncertainty quantification.
- **Talent confound.** Good front offices pick winning styles. Cluster
  success rate partially reflects talent allocation, not style.
- **Defensive scheme data isn't public.** Any defense-side claim becomes
  the #1 reviewer attack vector.

## Effort

- **~2-week EDA gate first.** Spike: extract features, run clustering,
  compute the playoff-vs-RS delta and championship rate per cluster. If a
  load-bearing headline number doesn't fall out, kill the video.
- **~4-week full build** if the EDA finds the number. Most of that is
  Manim viz + writing.

## Cursory research verdict (pre-persona)

*"Weak-to-mediocre as currently framed. Reframe before committing. The
core 'cluster teams, find which wins' has been done many times. The matchup
matrix is genuinely under-explored on YouTube but the sample sizes are
brutal. The strongest defensible reframe is 'do certain styles get exposed
in the playoffs?' — playoff-vs-RS efficiency delta by cluster — with the
matchup matrix as a hedged back-third. Recommend: weekend EDA spike. If no
sharp number emerges, kill."*

— Cursory research agent, 2026-05-16
