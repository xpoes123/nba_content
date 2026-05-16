# NBA Video Ideas — v0 Draft (for persona pressure-testing)

Working titles, hook candidates, data sources, methodology sketches. To be
reacted to by viewer-persona agents, then refined.

---

## 1. The Three GMs Who Built Half the League's Surplus

**Hook candidate:** "Of every positive-NPV contract negotiated in the NBA
right now, more than half were signed by three front offices. The other
27 teams are barely doing anything."

**Why it fits:** Direct extension of the contracts work. Same pipeline,
new question. Discord-postable headline.

**Data:** Existing surplus pipeline. Map every contract to the GM in
charge when it was signed (Spotrac, RealGM, news archives). Sum surplus
per GM.

**Methodology:**
- Re-run v4.1 NPV on every contract in the last 5 years (not just current)
- Map each contract to the signing GM
- Compute GM-WAR-like statistic: surplus generated above replacement-level GM
- Break out by acquisition channel: draft, trade, extension, FA signing

**Headline candidate:** "Stevens, Pelinka, and Presti generated 80% of
positive surplus in the last 5 years."

**Effort:** ~3 weeks. Data is largely in hand.

**Risk:** GMs come and go mid-season; attribution gets fuzzy. Also: small
sample, lots of noise.

---

## 2. The Ring-Chase Tax: What Vets Give Up to Chase a Title

**Hook candidate:** "Veterans who chase rings leave $X million on the
table per attempt. The median ring equity they buy with that discount
is Y%."

**Why it fits:** Personal/narrative hook (every fan has watched this
happen). Quant-defensible. Existing pipeline + free-agency history.

**Data:** Spotrac historical contracts, championship probabilities from
betting markets at signing time, your surplus pipeline.

**Methodology:**
- Define ring-chasers: vets 30+ who signed for ≤ 80% of expected market value
  on a team with preseason title odds ≤ 15%
- Compute the dollar discount (market value − actual signing)
- Cross-reference with whether they actually won a ring
- Build a "$ per ring %" exchange rate

**Headline candidate:** "The median ring-chaser pays $4.5M/year for a
6% increase in championship probability."

**Effort:** ~3 weeks.

**Risk:** Defining "ring-chaser" cleanly. Market-value model already has
known issues with stars.

---

## 3. Tanking Doesn't Work. Here's the Data.

**Hook candidate:** "Of the last 20 explicit tank jobs in NBA history,
exactly X made the Finals within seven years."

**Why it fits:** The thesis is academic but the video doesn't exist.
Wharton paper + Sportico data + your own NPV math = defensible.

**Data:** Historical standings, draft positions, payroll snapshots
(Spotrac), playoff results, franchise win-loss records.

**Methodology:**
- Define a tank job: team had ≥ 90% probability of missing playoffs by Jan 15
  AND finished bottom-5 in win%
- Look at next 7 seasons: Finals appearances, conference finals, playoff wins,
  net rating, attendance, owner valuation
- Build a counterfactual: what does "post-tank trajectory" look like vs
  baseline?

**Headline candidate:** "Of 18 explicit tank jobs since 2010, two reached
the Finals. The median tanking team is still bad seven years later."

**Effort:** ~4 weeks. The data is harder than it looks because franchise
strategy isn't always explicit.

**Risk:** The synthetic-control / counterfactual math is tricky and the
quant Discord will pick at it. Be honest about uncertainty.

---

## 4. The Apron Game Tree: Simulating the Next Five Years

**Hook candidate:** "I ran 10,000 simulations of what happens when every
contender is locked at the second apron. Here's how long the contending
window actually lasts."

**Why it fits:** Primer-style simulation. Direct continuation of your
cap work. Visually amazing in Manim.

**Data:** Current rosters, current contracts, cap projection, historical
trade frequency, historical aging curves.

**Methodology:**
- Build a roster-evolution simulator (signings, trades, aging) under apron
  constraints
- For each "core 3 stars + apron" team, simulate 5 years forward
- Track expected playoff wins, salary cost, forced-trade events
- Compare to "star + flexibility" archetype

**Headline candidate:** "Three-star apron rosters have a median contending
window of 2.4 years. Then they're forced to break it up."

**Effort:** ~6 weeks. Hard simulation; lots of design choices.

**Risk:** Simulator design choices can be argued. Mitigate by publishing
the code and being transparent.

---

## 5. EPV From Scratch (The Sebastian Lague Flagship)

**Hook candidate:** "Every possession in the NBA is worth a specific
number of expected points at every moment. Here's how to compute it from
the data — and what it tells you about why some players never get the
ball at crunch time."

**Why it fits:** Identity piece. Builds methodology cred for everything
after. The Cervone et al. 2014 paper exists but no one has animated it.

**Data:** SportVU 2013–16 tracking data (publicly available on GitHub
and HuggingFace) + play-by-play.

**Methodology:**
- Walk through the Cervone et al. micro/macro EPV model
- Show stock-ticker visualizations of EPV over time during one possession
- Identify "leaky" possessions where EPV peaks and then collapses
- Tag the player whose decision dropped EPV most often

**Headline candidate:** "Player X is the league's most negative EPV
decision-maker. He drops the possession value by Y% per touch."

**Effort:** ~8–10 weeks. Real model implementation. Closest to a thesis
project.

**Risk:** EPV is 11 years old; some viewers will know the academic
version. Differentiate with visualization + 2025-26 application.

---

## 6. What Gravity Actually Looks Like

**Hook candidate:** "The NBA released its own 'gravity' stat last year.
Curry's number leads by 50%. But the leaderboard misses the entire
point. Here's gravity as a visual field."

**Why it fits:** Pure Primer territory. NBA's new official stat is the
news peg.

**Data:** SportVU 2013–16 (for the off-ball density-field viz) +
NBA's current Gravity leaderboard.

**Methodology:**
- For each possession, compute the empirical defensive-position density
  around each offensive player
- Build a vector field of defender displacement caused by each offensive
  player's presence
- Compare top 5 vs middle 5 vs bottom 5 on the official Gravity stat
- Find moments where gravity does/doesn't translate to scoring

**Headline candidate:** "Curry generates 4.2 feet of average defender
displacement off-ball — twice the league median. But the bottom of the
gravity leaderboard isn't 'bad' — it's 'covered tight regardless.'"

**Effort:** ~5 weeks. Visualization is the bulk of the work.

**Risk:** Density-field visualizations can be misleading. Be explicit
about the methodology.

---

## 7. Adding a Second Star Costs You 0.8 of His Wins

**Hook candidate:** "When teams add a second star, the duo produces about
1.2x the wins of either star alone — not 2x. Here's the chemistry math
nobody is doing."

**Why it fits:** Counterintuitive, Discord-postable, fits the "everyone
thinks X, the data says Y" template. Builds on APBRmetrics skill-synergy
literature.

**Data:** Lineup data (nba_api `LeagueDashLineups`), historical RAPM,
roster archives.

**Methodology:**
- For every "star pair" since 2010, compute the actual lineup +/- vs
  expected from each player's solo numbers
- Decompose by skill overlap: two ball-handlers, two rim-protectors,
  shooter + creator, etc.
- Find which pairings under-perform additivity most

**Headline candidate:** "Two elite ball-handlers in a lineup retain 78%
of their additive value. Two elite stoppers retain 102%."

**Effort:** ~4 weeks.

**Risk:** RAPM noise + small-sample lineups. Use Bayesian priors. Will
need defending.

---

## 8. The NBA's Own Data Disagrees About Load Management

**Hook candidate:** "In 2024 the NBA published a report saying load
management doesn't reduce injury risk. Last month a peer-reviewed paper
using the same data found a 75% reduction. Here's who's right."

**Why it fits:** Adversarial methodology piece. Personal/opinionated
register (Jxmy-style). Hits hard on a topic everyone has takes on.

**Data:** NBA's 2024 report, the arXiv March 2026 reanalysis, public
injury data (Rotowire), minutes data.

**Methodology:**
- Recreate both analyses
- Identify where the methodologies differ (definition of "load," control
  group, lag windows)
- Run both side-by-side on the same dataset
- Show which conclusion is more robust

**Headline candidate:** "Three out of four times you can flip the NBA's
load-management conclusion just by changing how you define 'rest.'"

**Effort:** ~3 weeks. Recreation work, not heavy modeling.

**Risk:** The actual answer might be "both papers are noisy."
Embrace that.

---

## 9. When DARKO, EPM, and LEBRON All Disagree

**Hook candidate:** "The NBA's three best impact metrics agree on most
players. The five they disagree most on tell you what each model is
secretly measuring."

**Why it fits:** Methodology-defense piece. Builds reputation. Teaches
the audience how to read impact metrics.

**Data:** DARKO + EPM publicly downloadable. RAPTOR archived. LEBRON
behind paywall — may need to subscribe.

**Methodology:**
- Z-score each metric across the league
- Compute disagreement (variance across z-scores per player)
- Top 10 disagreement cases: dig into what's driving the gap
- For each gap, predict which model is right using out-of-sample season
  performance

**Headline candidate:** "DARKO loves him. EPM hates him. The market
agrees with whichever metric won last year — but they almost never agree."

**Effort:** ~3 weeks.

**Risk:** Requires careful normalization. The "right answer" is fuzzy.

---

## 10. The NBA Pulled the Tracking Data. It's Still on GitHub.

**Hook candidate:** "In 2017 the NBA stopped releasing player tracking
data to the public. 600 games of 25 Hz movement data from 2015–16 are
still sitting on GitHub. Here's everything we can still learn from
it — and what the league doesn't want us to see."

**Why it fits:** Story-driven. Personal/investigative angle. Real CV /
data engineering. Manim-ideal.

**Data:** `neilmj/BasketballData`, HuggingFace `dcayton/nba_tracking_data_15_16`.

**Methodology:**
- Inventory what 600 games can tell us (trajectories, screens, off-ball
  movement)
- Pick 5–7 questions answerable only with tracking data
- E.g., "How tight does LeBron play the pick-and-roll?" / "Curry's actual
  off-ball mileage per game" / "Which shooter generates the most defender
  movement?"
- Each question gets a Manim segment with real possessions overlaid

**Headline candidate:** "Curry ran 2.4 miles per game off-ball in
2015–16. The league average was 1.6. No public dataset since has been
able to verify whether that changed."

**Effort:** ~6 weeks. The data is clean; the visualizations are the work.

**Risk:** Data is 10 years old. Framing has to lean into "what we can
still learn" not "current insights."

---

## Open questions for persona pressure-test

- Which ideas have the strongest Discord-shareable hook?
- Which ideas are sport-bettor actionable (edge generation)?
- Which ideas are casual-fan-friendly vs. quant-only?
- Which ideas have already been done by someone whose work I'm not aware of?
- Which ideas have the highest payoff per week of effort?
- Which ideas, if executed perfectly, would land as a Goldsberry-grade
  ESPN feature?
