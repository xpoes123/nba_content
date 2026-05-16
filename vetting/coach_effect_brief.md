# Coach Effect — Production-Ready Brief

*Deep-research synthesis from four parallel agents (paper deep-dive, Python
replication, storyboard, adversarial defense). Phone-readable; scan the
TL;DR and decision-tree sections first.*

---

## TL;DR

The Coach Effect video is **greenlight-ready in concept**, but the deep
research surfaced one important wrinkle:

**The JQAS 2025 paper is paywalled, and the specific Bayesian-shrunk coach
estimates aren't in the open record.** The much-cited "Nick Nurse +20 wins"
number is from a Towards Data Science article using **OLS fixed-effects**,
not the JQAS Bayesian method. Under JQAS's partial pooling, Nurse's 2-season
estimate almost certainly shrinks to closer to +5–10 with wide credible
intervals.

This means the video has three honest paths:

1. **Lean on the TDS OLS numbers**, cite them clearly, explicitly contrast
   to "what the JQAS Bayesian method would do to small-sample tails."
2. **Replicate the JQAS method ourselves** in Python (via R's `mBARTprobit`
   through `rpy2`) and publish OUR numbers. Most credible. Adds ~2 weeks.
3. **Email Jared Fisher (BYU)** for the preprint PDF; authors usually share.
   Cheapest if it works.

The strongest defensible headline survives all three paths:
**"Coach effects span 46 wins. The spread is the same order of magnitude
as MVP-season Win Shares."** Distribution claim, not point claim. Survives
small-sample shrinkage.

**My recommendation:** start with (3) — email today — and start (2) in
parallel since the replication code is reusable for future ideas anyway.
Plan the script around the *spread* finding so you're not gated on getting
specific numbers.

---

## Decision tree before you commit

```
Can you email Jared Fisher and get the JQAS coach table?
├── Yes → use JQAS numbers verbatim, cite paper, ship in 3-4 weeks
└── No / no reply in a week
    └── Are you willing to spend 2 weeks replicating JQAS via mBARTprobit?
        ├── Yes → ship "I replicated the paper" version in 5-6 weeks
        │         (this is the strongest Lague-mode framing)
        └── No → use TDS OLS numbers + explicit on-screen caveat,
                 ship in 3-4 weeks; frame as "an analyst's leaderboard,
                 the Bayesian version would shrink it"
```

---

## The headline you can ship under any path

> "Across 40 years of NBA coaching, the gap between the best and worst
> coach by estimated effect is 46 wins. That's the same order of magnitude
> as the spread of MVP-season Win Shares. We talk about MVP-tier players.
> We don't talk about MVP-tier coaches. That's the gap I want to fix."

This survives:
- Small-sample tail shrinkage (it's about the range, not the tip)
- Endogenous hiring (the range exists regardless of who hires whom)
- VORP contamination (the range exists regardless of attribution)
- Era confound (the spread is within-era, not across)

The other two candidate headlines are weaker but usable as **B-roll
landings** inside the video:

- **Frank Vogel** — 89th percentile coaching, 75th percentile winning,
  11-season sample = narrow CIs. Strong narrative case ("the roster hid
  him").
- **Nick Nurse +20** — *only* as the teaching moment for sample-size
  shrinkage. Not as the standalone headline.

---

## Storyboard — 12 minutes, 7 segments

| # | Name | Window | Beat |
|---|---|---|---|
| 1 | Cold open | 0:00–0:45 | "LeBron is worth 20 wins, we have receipts. Pop is worth 20 wins, we're guessing. Until now." — Show the 46-win spread vs MVP-season WS range as overlapping bars |
| 2 | Premise | 0:45–2:00 | Coaching valuation is the last unquantified seat in basketball ops. Players have BPM/VORP/RAPM. GMs got their reckoning (callback to *1 of 97*). Coaches got vibes. |
| 3 | Methodology setup | 2:00–4:00 | Endogeneity problem → player-season fixed effects via ΔtVORP → BART with monotone constraint. Two micro-scenes: confounding DAG + BART tree growing. |
| 4 | The reveal | 4:00–7:00 | Bar race of top coaches with credible-interval shadows. Build to a static "headline frame" at 6:45 (the screenshot moment). |
| 5 | The contrarian case | 7:00–9:30 | Frank Vogel underrated case (89/75 split). Optionally Spo as the alignment case (model agrees with the public). Coach-tenure trajectory plot. |
| 6 | Methodology defense | 9:30–11:00 | Three-critique card: endogenous hiring, VORP contamination, small-sample tail bias. Posterior-shrinkage demo: re-show Nurse's bar with proper CI width. |
| 7 | Close | 11:00–12:00 | "Steve Kerr is paid like a luxury accessory. The math says he's a max contract. The coach market is the last inefficient market in the NBA." |

### Key scene-by-scene notes

- **Bar race in Segment 4 must show credible intervals as visible shadows.**
  Without that, Segment 6's "we walked back the precision but not the
  ranking" beat doesn't land.
- **Segment 6's calibration framing is critical.** Frame the shrinkage as
  "the leaderboard is real, the exact numbers have uncertainty" — not as a
  retraction. The contracts video used the same move on Mobley's $9M; same
  audience reaction expected.
- **Lead Segment 5 with a non-consensus result.** The Vogel reframe ("coach
  the NBA undervalued") is the credibility move that proves the model isn't
  just confirming the ESPN top-5.

### Thumbnail variants (run A/B)

- **Variant A (CTR play):** Massive "+20" in purple, Nick Nurse's face on
  left, faded LeBron silhouette right with smaller "+15."
  Title: *Coaches Are MVPs.*
- **Variant B (retention play):** Top-5 bar chart left half, Kerr's face
  large on right with overlay "$17M IN WINS."

Skip the quadrant-plot thumbnail (Variant C) — high watch time, low CTR.

### Title test candidates

1. **The NBA Coach Effect Is Bigger Than the MVP** ← CTR lead
2. **Steve Kerr Is Worth 17 Wins (And He's Underpaid)**
3. **Coaches Span 46 Wins. We've Been Pricing Them Wrong.** ← Discord lead

Run #1 first 48 hours, swap to #3 if CTR underperforms.

---

## Adversarial defense — what to acknowledge on-screen

The contracts video's lesson: concede the strongest attack *on camera*
before the audience can. Three on-screen acknowledgements (priority order):

### 1. Small-sample tail bias (the #1 attackable line)

**The dunk:** "Nurse +20 because he coached 6 seasons. Pop coached 27 and is
at +9. You're ranking variance, not skill."

**Defense:** Show every coach's point estimate *with* its 95% credible
interval as a forest plot. Nurse's CI is wide; Pop's is tight. Replace
"Nurse > LeBron's WS" with "the *posterior range* spans -25 to +21." This
is the single most credibility-buying move available.

### 2. VORP contamination (most technically serious)

**The dunk:** "VORP is a function of minutes, role, lineups — all coach
decisions. You're regressing the coach's output on the coach's output."

**Defense:** 15-second on-screen acknowledgement. *"We're not separating
tactical IQ from deployment skill. ΔtVORP captures both. That's a feature,
not a bug — coaching IS deployment."* Pre-empts the strongest technical
objection.

### 3. Endogenous coach hiring

**The dunk:** "Good orgs hire good coaches. Coach effect = front-office
effect."

**Defense:** Show 2-3 same-roster coach transitions where the *coach*
changed but the org didn't. **Tom Thibodeau (Bulls → Wolves → Knicks) is
the gold case study here** — show how the model treats him across orgs.
Frame as "coach + system they're empowered to install."

### Description-appendix concessions (don't lead with these on-screen)

- Era confound (Phil's 90s ≠ Nurse's 2020s)
- Health/injury luck (mostly handled by per-player ΔtVORP)
- Frank Vogel reframe (he was fired pre-equilibrium)
- MVP-comparison units (diffuse vs concentrated wins)

---

## Replication path

**Recommended stack:** R `BART` + Fisher's `mBARTprobit` package, driven
from Python via `rpy2`. The PyMC-BART alternative lacks the monotonicity
constraint, which is the load-bearing identifying restriction of the
paper. Build a soft-monotonicity PyMC-BART fallback only if `rpy2` eats
more than half a day to set up.

### Week-by-week

**Week 1 — Data pipeline** (reuses ~30% of the contracts scraper)
- D1–2: extend `videos/01_contracts/src/fetch.py` to multi-season VORP
  scrape (1996–2024, ~29 seasons × ~600 players).
- D3–4: `nba_api.LeagueDashLineups` puller with per-season parquet caching.
- D5: coach tenure scrape + game-log scrape.
- D6–7: ΔtVORP computation + join → one row per (game, coach) with W/L.

**Week 2 — BART fitting**
- D8–9: `rpy2` setup, install `mBARTprobit`, smoke-test on toy data.
- D10–11: fit `probit_monbart(y=win, x=[ΔtVORP, coach_id])` on full panel.
- D12–13: posterior win-probability extraction per coach at fixed ΔtVORP
  grid.
- D14: coach rankings + credible intervals.

**Week 3 — Validation + Manim**
- D15–16: compare top/bottom 5 to JQAS paper's table (Spearman ρ > 0.7 =
  success).
- D17–19: Manim animation.
- D20–21: buffer for the Week 1 lineup pull breaking.

### What can be skipped (with on-screen caveat)

- Injury control variable (~3% explanatory power, days of scraping)
- Multi-year coach-tenure interactions (paper has them, marginal effect)
- Pre-1996 coaches (play-by-play coverage cutoff)

### Load-bearing — do NOT cut

- Probit + monotonicity constraint (the entire identification frame)
- ΔtVORP itself (not team-season VORP)
- Per-coach posterior intervals (not point estimates)

**Fallback if BART fails Week 2:** isotonic regression of P(win) on
ΔtVORP + coach fixed effects via logistic GLM. Frame as "two specs,
they agreed."

---

## Open questions / next actions

**Before filming:**
1. **Email Jared Fisher (BYU Stats) for the JQAS preprint PDF.** Cheapest
   path to the actual top-10 table with credible intervals. Most likely to
   succeed.
2. **Confirm whether the JQAS paper has the bottom-5 named.** The public
   record (TDS) names top coaches but not the bottom. Need this for the
   "range" claim to be visualizable.
3. **Decide replication vs. TDS-citation framing.** Replication is 2 extra
   weeks but enables a Lague-style "I rebuilt the paper because it was
   paywalled" narrative — which is in itself a video-worthy story moment.

**After this video ships:**
- The replication infrastructure (BR multi-season VORP, lineup
  possessions, ΔtVORP pipeline) is directly reusable for: Idea 2 (Two
  Stars, Two Halves — same lineup-RAPM machinery), Idea 8 (Whose Defense
  Is Real — needs matchup data on top of this), and any future "lineup-
  level model" video. The video pays back twice.

---

## Persona heatmap (from original IDEAS.md panel)

Carried forward from the original 10-idea pressure test:

| Persona | Verdict | Lead concern |
|---|---|---|
| Quant Discord | Strong yes (replicable peer-reviewed paper) | Tail bias on small-N coaches |
| Sharp Bettor | Soft yes — coaching-change futures gain a baseline | Pure retrospective, no live model |
| Casual Fan | Strong yes — named coaches, surprising arguments | Don't get lost in BART math |
| FO Insider | Strong yes — privately benchmarked internally | Acknowledge VORP-contamination directly |
| YouTube Strategist | **TOP 1 highest-ROI-per-week on the doc** | Lead Variant A thumbnail with Kerr's face |

Consensus: this is the next video. The deep research confirmed every
panel verdict.

---

## Effort estimate

| Path | Weeks | Risk |
|---|---|---|
| TDS-numbers + storyboard | 3–4 | Discord dunk on "Nurse > LeBron" line — must rewrite headline |
| Email Fisher for paper + ship | 3–4 | Depends on his response time |
| Full JQAS replication + ship | 5–6 | Real engineering risk on `rpy2` + monotone BART |

**My take:** start the email today, start data scrape Week 1 regardless.
By end of Week 1 you'll know if Fisher replied; commit to the replication
path then.

---

## File pointers

- Source paper: [JQAS 2025 DOI](https://doi.org/10.1515/jqas-2025-0025) (paywalled)
- Methodology arxiv: [Fisher 2025, Probit Monotone BART](https://arxiv.org/abs/2509.00263)
- TDS comparator: [Quantifying the Contribution of NBA Coaches](https://towardsdatascience.com/quantifying-the-contribution-of-nba-coaches-using-fixed-effects-56f77f22153a/)
- R package to clone: `github.com/jareddf/mBARTprobit`
- PyMC-BART fallback: [pypi.org/project/pymc-bart/](https://pypi.org/project/pymc-bart/) v0.11.0 (Oct 2025)
- Existing scraper to reuse: `videos/01_contracts/src/fetch.py`
- Existing VORP CSV: `videos/01_contracts/data/raw/advanced_stats.csv`

## Agent transcripts

Full agent outputs are at `/tmp/claude-1000/.../tasks/<id>.output`:

- Paper deep-dive: `ae2c6b9154a2ebe62`
- Python replication: `a7fe3bcaabb40b202`
- Storyboard: `a38f4d524c6c2b764`
- Adversarial defense: `a8dca2d07024c9635`

Methodology applied: [`../METHODOLOGY.md`](../METHODOLOGY.md), Stage 5
deep research (panel verdict greenlit in original IDEAS.md pass).
