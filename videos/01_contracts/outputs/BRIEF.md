# NBA Best Value Contracts — Analysis Brief (v4.1, adversarial-review-corrected)

Data: 2025-26 season, Basketball-Reference + Spotrac, fetched 2026-05-15.
Sample: 583 players with advanced stats; 472 with year-by-year contract data.
Played-enough filter: 1000+ minutes for headline tables (276 players).
Multi-year filter: 2+ contract years remaining for NPV (224 players).

**v4.1 update (2026-05-16):** Second adversarial pass corrected four team-tier
assignments after end-of-season payroll verification — PHI dropped out of
first-apron (under tax), BOS moved up to first-apron taxpayer, NYK and GSW
moved from second-apron to first-apron (both above first apron, below second).
The "1 of 97" headline is unchanged. Pritchard's *effective* NPV strengthens
from +$4.3M to +$9.9M because Boston is actually a first-apron team. Bottom-5
effective list shifts entirely (Embiid, Anunoby, Towns, Curry drop out).

## What changed from v1/v2

The original model had three compounding issues that an adversarial review surfaced:

1. **Aging curve applied to z-scores instead of wins** — gave negative-WA
   players a free "improvement" with age (z-score shrinks toward mean ≠ wins
   declining).
2. **β fit on above-median WA, extrapolated to full league** — the slope was
   biased by max-contract top-coding. Inflated $/z from $4.86M to $11.78M.
3. **Tax multiplier composed multiplicatively with apron premium** — tax is
   per-dollar marginal, apron is operational. Should be additive. Inflated
   extreme effective NPVs 2-3×.

Other fixes:
- **15% Bayesian shrinkage** toward league mean (was 30%, too aggressive for
  players on upward trajectories like Pritchard or Naw)
- **Median rather than total** for bucket comparisons (controls survivorship
  in the 1000-min filter)
- **Three separate leaderboards** explicitly (naive, effective, open-negotiation),
  never mixed

## Methodology (v4)

```
WA_wins      = (2.7 · VORP + WS) / 2
WA_z         = (WA_wins - μ) / σ                    on 500+ MP pool
β            = OLS slope of (salary - vet_min) on WA_z,
               fit on OPEN-NEGOTIATION contracts only           → $4.86M / z-unit
$/win        = β / σ_WA                                          → ~$1.6M / win

expected_market_salary    = vet_min + β · WA_z
naive_surplus             = expected - actual

aging_projection (year k) = current_wa_z · (age_mult[age+k] / age_mult[age])
                            with optional 15% shrinkage toward zero

NPV_naive                 = Σ (expected_k - salary_k) / 1.05^k
NPV_effective             = NPV_naive · team_multiplier

team_multiplier:
  below_cap_floor:          0.5
  above_cap_below_tax:      1.0
  taxpayer:                 1.5  (+0.5 if repeater)
  first_apron:              2.0  + 0.3 operational premium  → 2.3 base
  second_apron:             2.5  + 0.6 operational premium  → 3.1 base
```

## The headline finding

**Of 97 openly negotiated NBA contracts with 1000+ MP and 2+ years remaining,
exactly one is projected to deliver positive NPV: Payton Pritchard.**

Bucket positive-NPV share:

| Bucket | N | Median NPV | % Positive |
|---|---:|---:|---:|
| Veteran minimum | 22 | +$0.3M | **55%** |
| Rookie scale | 72 | −$13.0M | 10% |
| Max contracts | 33 | −$133.7M | 0% |
| **Open negotiation** | **97** | **−$40.4M** | **1%** (Pritchard) |

The CBA-mandated veteran-minimum bucket produces more positive contracts than
all GM-negotiated contracts in the league combined. The min bucket is the
*only* bucket where teams reliably get value.

## Top 5 (team-neutral NPV)

1. **Neemias Queta** (BOS) — +$13.0M • vet min, 2 yrs
2. **Cam Spencer** (MEM) — +$10.9M • vet min, 4 yrs
3. **Ryan Kalkbrenner** (CHO) — +$9.9M • vet min, 4 yrs
4. **Moussa Diabaté** (CHO) — +$9.1M • vet min, 2 yrs
5. **Sandro Mamukelashvili** (TOR) — +$8.0M • vet min, 2 yrs

All five are vet minimum. The "top contracts in the NBA" — by the model's
honest open-market price — are players that 90% of NBA fans cannot name.

## Top 5 open-negotiation (the headline list)

1. **Payton Pritchard** (BOS) — +$4.3M ← THE ONLY POSITIVE
2. Jaime Jaquez Jr. (MIA) — −$2.6M
3. Saddiq Bey (NOP) — −$2.7M
4. Miles McBride (NYK) — −$3.9M
5. Kevin Porter Jr. (MIL) — −$4.5M

## Top 5 effective NPV (team-adjusted)

1. **Neemias Queta** (BOS, 1st apron, 2.3×) — **+$29.8M**
2. **Cam Spencer** (MEM) — +$10.9M
3. **Payton Pritchard** (BOS, 1st apron, 2.3×) — **+$9.9M** ← appears in effective top 5 once Boston is correctly tiered
4. **Ryan Kalkbrenner** (CHO) — +$9.9M
5. **Moussa Diabaté** (CHO) — +$9.1M

Boston shows up twice in the top 5 — both Queta and Pritchard hit because
they're cheap-on-apron, the highest-multiplier configuration that produces
positive surplus. Same playbook (Brad Stevens, vet-min / pre-breakout
extension) running in the highest-leverage tier.

## Bottom 5 naive NPV

1. **Devin Booker** (PHO) — −$245M • ascending 5-year max
2. **Jaren Jackson Jr.** (MEM→UTA mid-season trade) — −$214M • new 5-year max
3. **Joel Embiid** (PHI) — −$208M • played 46% of season
4. **Evan Mobley** (CLE) — −$207M • 5-year max in year 1 this season
5. **De'Aaron Fox** (SAS) — −$203M

## Bottom 5 effective NPV (apron-amplified)

1. **Evan Mobley** (CLE, 2nd apron, 3.1×) — **−$642M**
2. **Jaylen Brown** (BOS, 1st apron, 2.3×) — **−$429M**
3. **Luka Dončić** (LAL, 1st apron repeater, 2.8×) — **−$363M**
4. **Anthony Edwards** (MIN, 1st apron, 2.3×) — **−$350M**
5. **Donovan Mitchell** (CLE, 2nd apron, 3.1×) — **−$342M**

Pattern: every contract in the effective bottom 5 is a max deal on an apron
team. The single most expensive failure mode in modern NBA roster construction
is "sign a max while already at the apron."

**Boston irony:** Boston has both the *only* positive open-negotiation contract
in the league (Pritchard, +$9.9M effective) AND a bottom-5 worst contract
(Brown, −$429M effective). Same team, two contracts at opposite poles. Cleanest
illustration in the dataset that bucket — not team competence — drives outcome.

## Pritchard scenario across 30 teams

Same player, same $7M/yr contract, same 3 years remaining. Effective NPV:

| Team | Tier | Multiplier | Pritchard NPV |
|---|---|---:|---:|
| CLE | 2nd apron | 3.1× | **$13.3M** |
| GSW | 1st apron, repeater | 2.8× | $12.0M |
| LAL | 1st apron, repeater | 2.8× | $12.0M |
| NYK / HOU / MIN / BOS | 1st apron | 2.3× | $9.9M |
| LAC | taxpayer, repeater | 2.0× | $8.6M |
| 22 teams | above cap, below tax | 1.0× | $4.3M |
| BRK | below cap floor | 0.5× | $2.2M |

**6× spread on the same contract.** Boston (his actual team) is at 2.3×, so
his real effective NPV is +$9.9M, not the +$4.3M team-neutral number. The
range from BRK ($2.2M) to CLE ($13.3M) is still the strongest single
visualization in the video.

## Caveats to include in the video description

- Box-score WA misses defensive specialists (Naw, McDaniels). EPM would be
  tighter but isn't scrapeable.
- Open-market β fit on open-negotiation only; an all-sample slope would be
  ~2× higher but biased by max-contract top-coding.
- 15% Bayesian shrinkage applied to one-season WA. Multi-year priors would
  shift some rankings slightly (Pritchard would actually rise — career
  trajectory has been upward).
- Aging curve is population mean. Outliers like Curry are over-discounted by
  the model — the −$390M Curry number is probably half-true.
- Team multipliers are tier-level approximations. Real cap economics are
  continuous within tier and dynamic across the contract life.
- 1000-min filter introduces survivorship in the rookie/min buckets. Reported
  aggregates are conditional on "played meaningfully."

## Suggested video structure (15 min)

See `VIDEO_OUTLINE.md` for the full beat-by-beat script outline. Headline
structure:

1. **Cold open** — "I modeled every NBA contract; 96 of 97 GM deals are underwater."
2. **The four CBA buckets** — explain why 3 of 4 are pre-rigged
3. **The killer stat** — 1 of 97 reveal
4. **Pritchard story** — pre-breakout extension, the only way to win this game
5. **Methodology** — brief, defensible (4 fixes from adversarial review)
6. **Worst contracts** — Mobley, max-on-apron disasters
7. **Pritchard 30-team chart** — the team-context insight
8. **Close** — three numbers: 1 of 97, 55% (min bucket), 6× (Pritchard range)

## Data files

- `outputs/v4_top10_all.csv` — top 10 NPV across all buckets
- `outputs/v4_top10_unrigged.csv` — top 10 open-negotiation only
- `outputs/v4_top10_effective.csv` — top 10 by team-adjusted NPV
- `outputs/v4_bottom10.csv` — worst 10 naive
- `outputs/v4_bottom10_effective.csv` — worst 10 effective (apron-amplified)
- `outputs/v4_pritchard_scenario.csv` — Pritchard's NPV across 30 teams
- `data/processed/values_v4_final.csv` — full per-player NPV with all features

## Source code

- `src/fetch.py` — Basketball-Reference scrapers
- `src/clean.py` — dedup traded players, parse salaries, join
- `src/value_v4.py` — composite WA, open-market slope fit, aging, shrinkage
- `src/team_context.py` — additive tax + apron multipliers
- `src/final_v4.py` — full pipeline producing the headline outputs

Replace the original `value.py` with `value_v4.py` if you want to keep one
canonical script. The older `value.py` / `value_v2.py` are kept for the
methodology section's "what changed" comparison.
