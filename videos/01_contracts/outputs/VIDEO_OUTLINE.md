# Of 97 NBA Contracts GMs Actually Negotiated, Exactly One Will Make Money

**Format**: 15-minute analytical video. ~2,000 words of script. Built around Manim visuals — minimal B-roll, mostly animated data viz.
**Tone**: Confident, data-driven, Thinking Basketball / Goldsberry register.
**Hook**: Subvert the "best contracts" listicle by showing the entire genre is asking the wrong question.

## Manim conventions used throughout

- Color palette (matches the Python analysis):
  ```python
  TIER_COLORS = {
      "second_apron":      "#c1272d",
      "first_apron":       "#e67e22",
      "taxpayer":          "#f1c40f",
      "above_cap":         "#34495e",
      "below_cap":         "#95a5a6",
  }
  BUCKET_COLORS = {
      "rookie_scale":      "#2980b9",
      "min":               "#16a085",
      "max":               "#c0392b",
      "open_negotiation":  "#27ae60",
  }
  HIGHLIGHT_GREEN = "#27ae60"
  HIGHLIGHT_RED   = "#c0392b"
  BACKGROUND      = "#1a1a2e"
  TEXT            = "#ECECEC"
  ```
- Font: `Inter` for body text, `JetBrains Mono` for numbers (use `Text(..., font="JetBrains Mono")`).
- Default scene length: 30-90 seconds. Multi-element builds use `LaggedStart` with `lag_ratio=0.05-0.15`.
- Camera: 16:9, 1920×1080 at 60fps. `config.background_color = BACKGROUND`.

---

## Cold open (0:00–0:45) — 100 words

**Narration**:
> Every basketball channel makes the same video. Top 15 best contracts in the NBA. The names rotate — Jokić, Brunson, SGA, Wemby — but the list is always the same.
>
> So I built a model. Every contract in the NBA, all 472, priced against the open-market shadow rate. Aging curves. Cap tier multipliers. The whole thing.
>
> Then I sent it to a quant reviewer and tore it apart twice.
>
> Here's the punchline: of 97 contracts that GMs actually negotiated, exactly one will deliver positive value to the team.
>
> Just one.

### Manim scenes

**Scene 1 — `ColdOpenNames` (0:00–0:18)**

Names flicker across screen in random positions. 12-15 names, 0.4s each, overlapping fade-in/fade-out.
```python
names = ["JOKIĆ", "BRUNSON", "SGA", "WEMBY", "DURANT", "PRITCHARD",
         "KORNET", "AVDIJA", "JALEN JOHNSON", "NAW", "HALIBURTON", ...]
# each: Text() at random position, FadeIn(run_time=0.2), wait 0.2, FadeOut(run_time=0.2)
# stagger with LaggedStart(*animations, lag_ratio=0.08)
```

**Scene 2 — `ColdOpenStat` (0:18–0:45)**

Names sweep off screen. Big centered build:
```
LINE 1:  "97 contracts GMs negotiated"
LINE 2:  "1 will deliver positive value."
```
- LINE 1 written letter-by-letter via `Write(line1, run_time=1.5)`
- Pause 0.5s
- LINE 2 appears: "97" stays grey, "1" appears in `HIGHLIGHT_GREEN`, large (96pt)
- Hold 2s
- Smash cut to title card

---

## Segment 1: Why every "best contracts" list is wrong (0:45–2:45) — 270 words

**Narration**:
> Every NBA contract falls into one of four buckets. Three of them are set by the CBA before any GM picks up the phone.
>
> Rookie scale — first-rounders cost-controlled for four years.
>
> Max contracts — superstars *capped* at 35% of the salary cap. Jokić would make a hundred million on an open market. The CBA forbids more than fifty-five.
>
> Veteran minimum — a salary floor for vets at $2.3 million.
>
> And **open negotiation** — everything else. The only bucket where a GM and an agent actually negotiate a number.
>
> So when a YouTuber tells you Wemby has the best contract in the league, what they mean is: the CBA wrote his contract before any front office got involved. Same for Brunson taking the max. Same for any second-rounder on a vet min.
>
> The interesting question isn't which CBA-mandated bargains exist. It's which contracts that GMs *actually negotiated* beat the market.
>
> I priced them. Composite Wins Added — VORP converted to wins, plus Win Shares. Regression line fit only on open-negotiation contracts. The slope identifies what the market pays for a unit of production, free of CBA constraints.
>
> Four point eight six million dollars per standard deviation. Aging curve from Vaci et al. Discount at five percent. Apply.

### Manim scenes

**Scene 3 — `FourBuckets` (0:45–1:45)**

CBA box at top of screen. Four branches sprout downward, each landing in a labeled bucket.
```python
cba_box = Rectangle().set_fill(opacity=0.3, color=TEXT)
cba_label = Text("CBA")
# four branches grow with Create()
branch1 → Text("Rookie scale")   color=BUCKET_COLORS["rookie_scale"]
branch2 → Text("Max contracts")  color=BUCKET_COLORS["max"]
branch3 → Text("Vet minimum")    color=BUCKET_COLORS["min"]
branch4 → Text("Open negotiation") color=BUCKET_COLORS["open_negotiation"]
# branch4 visually grows AWAY from CBA box (curves out, dotted line back to CBA)
```
LaggedStart: each bucket appears as it's mentioned in narration. Use cue-card-style timing.

**Scene 4 — `JokicCap` (1:45–2:10)**

Jokić salary visualized as two bars side by side.
```python
ax = NumberLine(x_range=[0, 110, 10])
open_market_bar = Rectangle(width=ax.n2p(100)[0], height=0.5).set_fill(HIGHLIGHT_GREEN)
cba_capped_bar = Rectangle(width=ax.n2p(55)[0], height=0.5).set_fill(HIGHLIGHT_RED)
labels: "Open market: $100M" and "CBA max: $55M"
# Show open_market_bar first, then slice it visually with a downward "CAP" line
# The capped portion fades to red, the rest greys out
```

**Scene 5 — `BuildTheFormula` (2:10–2:45)**

Term-by-term equation build.
```python
formula = MathTex(
    r"\text{salary}_{\text{predicted}}",
    "=",
    r"\$2.3\text{M}",
    "+",
    r"\$4.86\text{M}",
    r"\cdot",
    r"\text{WA}_z"
)
# Write each piece sequentially. After complete, fade vet_min to grey,
# highlight $4.86M in yellow with a callout: "OPEN-MARKET SHADOW PRICE"
# Then a smaller line below appears: "fit on open-negotiation contracts only (n=127)"
```

---

## Segment 2: The killer stat (2:45–4:30) — 260 words

**Narration**:
> Here's every contract in the league that's openly negotiated, played a thousand minutes this season, and has at least two years remaining. Ninety-seven contracts.
>
> For each, project remaining production with the aging curve. Apply Bayesian shrinkage toward the league mean. Price against the open-market slope. Sum the discounted surplus across remaining years.
>
> Then ask: how many are projected positive?
>
> One.
>
> Payton Pritchard. Boston Celtics. Four-year, thirty-million-dollar extension signed October 2023 — two years before he won Sixth Man of the Year. Projected NPV surplus: four point three million dollars.
>
> Every other openly negotiated contract in the league is projected net-negative. Jaime Jaquez. Saddiq Bey. Tre Jones. Deni Avdija. Luke Kornet. Every name your favorite YouTuber listed — all underwater on a multi-year horizon.
>
> Now compare to the CBA-mandated buckets. Veteran minimum deals: fifty-five percent projected positive. The CBA's mandated floor produces more good contracts than every GM in the league combined.

### Manim scenes

**Scene 6 — `NinetySevenDots` (2:45–3:50)**

THE headline visual. 97 dots populate one by one, then 96 turn red and 1 stays green.
```python
N = 97
GRID_COLS = 12
GRID_ROWS = 9  # 108 cells, 97 used

# Phase 1 (5s): dots populate from top-left in reading order
dots = VGroup(*[Dot(radius=0.18, color=TEXT) for _ in range(N)])
dots.arrange_in_grid(rows=GRID_ROWS, cols=GRID_COLS, buff=0.35)
self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.02), run_time=4)

# Phase 2 (3s): label appears
label = Text("97 openly negotiated NBA contracts").scale(0.6)
self.play(Write(label))

# Phase 3 (4s): suspense beat. Then colorize.
# Sort dots by their player's NPV (data from v4_one_of_97 figure).
# Pritchard's dot (precomputed position) turns green and grows.
# 96 others turn red with LaggedStart.
self.play(
    dots[pritchard_idx].animate.set_color(HIGHLIGHT_GREEN).scale(1.5),
    LaggedStart(*[d.animate.set_color(HIGHLIGHT_RED) for i, d in enumerate(dots) if i != pritchard_idx],
                lag_ratio=0.01),
    run_time=3,
)

# Phase 4 (3s): label appears under Pritchard's dot.
pritchard_label = Text("Payton Pritchard\n+$4.3M NPV", font_size=24, color=HIGHLIGHT_GREEN)
pritchard_label.next_to(dots[pritchard_idx], DOWN, buff=0.4)
self.play(Write(pritchard_label))
```

**Scene 7 — `BucketPositiveShare` (3:50–4:30)**

Four horizontal bars showing % positive by bucket.
```python
buckets = ["vet min", "rookie scale", "max", "open negotiation"]
shares = [55, 10, 0, 1]
colors = [BUCKET_COLORS[k] for k in ["min","rookie_scale","max","open_negotiation"]]

bars = BarChart(values=shares,
                bar_names=buckets,
                bar_colors=colors,
                y_range=[0, 70, 10],
                y_length=4,
                x_length=8)
# After bars draw in, add labels showing the absolute counts in parens
# e.g., "55% (n=22)" floating above each bar
# Then a Text label appears: "1% = Pritchard" with arrow pointing to that bar
```

---

## Segment 3: How is Pritchard the only one? (4:30–6:45) — 330 words

**Narration**:
> So how. Why him.
>
> October 8th, 2023. Brad Stevens signs Payton Pritchard to a four-year, thirty-million-dollar extension. At the time, Pritchard is averaging five points per game over three NBA seasons. He's publicly asked for a trade because he isn't getting minutes. He's a restricted free agent in waiting. Boston has just lost the Eastern Conference Finals.
>
> Stevens doesn't trade him. He extends him for less than the mid-level exception.
>
> Two seasons later, Pritchard wins Sixth Man of the Year. His Wins Added composite — top ten percent of the league — gets him onto a deal that pays him seven million dollars.
>
> Three reasons he's the only positive contract on the board.
>
> One: he was extended *before* the breakout. The price was set on his pre-2024 production. The market had no idea he was about to become a seventeen-points-a-night scorer.
>
> Two: length compounds. Three years remaining at seven million ascending to eight, all guaranteed. Every season at his current level produces seven-figure surplus.
>
> Three: Pritchard is the only one whose price was anchored *low* and stayed there. Other teams have tried the same playbook — extend a guy before he breaks out — but at a market-rate number. Atlanta extended Jalen Johnson in October 2024, pre-All-Star, for one-fifty over five years. Washington extended Avdija in October 2023, pre-Portland trade, for fifty-five over four. Both of those came before the breakout. Both are still underwater because the *price* was too high. Pritchard's extension is the only one in the league where the price was anchored on a five-points-per-game backup, and then the player turned into a Sixth Man of the Year. Price plus timing. Everyone else got one or the other.

### Manim scenes

**Scene 8 — `PritchardTimeline` (4:30–5:30)**

Horizontal timeline. Career-arc graph above it.
```python
timeline = NumberLine(x_range=[2020, 2026, 1], length=10).shift(DOWN*1.5)
events = [
    (2020, "Drafted #26"),
    (2022, "Trade demand"),
    (2023.75, "Extension signed\n4yr / $30M"),
    (2025, "6MOY winner"),
    (2026, "Now"),
]
# Each event: a Dot on the line + a callout box above. Appear sequentially.

# Above timeline: line plot of WA_z over those 5 seasons
wa_line = Axes(x_range=[2021, 2026, 1], y_range=[-0.5, 2.0, 0.5])
wa_values = [-0.4, 0.2, 0.5, 1.4, 1.8]  # rough trajectory
graph = wa_line.plot_line_graph(x_values=[2021,...], y_values=wa_values)
# After timeline events build, the WA graph draws across left-to-right
# An annotation appears at 2023.75: "Extension signed HERE" with a vertical
# dashed line connecting the timeline to the graph
```

**Scene 9 — `ThreeReasonsCallout` (5:30–6:45)**

Three numbered callouts that build one at a time.
```python
reasons = VGroup(
    Text("1. Extended BEFORE the breakout").scale(0.7),
    Text("2. Length compounds (3 yrs × $7M)").scale(0.7),
    Text("3. Price anchored LOW — not just signed early").scale(0.7),
).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

# As each reason is narrated, FadeIn that line.
# After all three present, the third one (most important) animates:
#   - Background highlight box appears behind reason 3
#   - Small subgraphic to the right: three comparison rows:
#     - Avdija — pre-breakout extension, $13.75M/yr  → still net-negative
#     - J. Johnson — pre-breakout extension, $30M/yr → still net-negative
#     - Pritchard — pre-breakout extension, $7.5M/yr → ONLY positive
#   - Each row has a green check (timing) and either a green or red dollar
#     icon (price). Only Pritchard gets both green.
```

---

## Segment 4: The framework, briefly (6:45–8:15) — 230 words

**Narration**:
> Brief detour for the quants. The model was built skeptically.
>
> The price. Four point eight six million dollars per standard deviation of production, fit on open-negotiation contracts only. Max-contract slopes are misleading because they're top-coded at the CBA ceiling. Min deals are floored. Only the open-negotiation bucket reveals the unconstrained market slope.
>
> The aging. Population aging curve. Peak at twenty-six, seven-eight percent decline per year through thirty-two, accelerating after. Applied in win units, not z-units. An earlier version applied aging directly to z-scores, which gave negative-WA players a free improvement from regression to the mean. Bug, fixed.
>
> The team context. A dollar of salary doesn't cost a dollar. On a tax team, $1.50. On a second-apron team, three and a half. Apron premium added on top — lost mid-level exception, no aggregation in trades, frozen first-round picks.
>
> Bayesian shrinkage of fifteen percent. The model is conservative. Pritchard survives a more aggressive prior. Most of the overpays at the bottom survive shrinkage too.

### Manim scenes

**Scene 10 — `PriceFitScatter` (6:45–7:25)**

Scatter plot of WA_z vs salary, with regression line.
```python
ax = Axes(x_range=[-2, 5.5, 1], y_range=[0, 60, 10],
          x_length=8, y_length=4,
          axis_config={"include_numbers": True})
# Three sets of dots, colored by bucket:
#   - open_negotiation: green dots (the fit sample)
#   - max contracts: red dots (clustered at top, $50M+)
#   - rookie/min: blue/teal dots (clustered low)
self.play(FadeIn(open_neg_dots))
# Regression line draws through them
line = ax.plot(lambda x: 2.3 + 4.86 * x, color=HIGHLIGHT_GREEN)
self.play(Create(line))
# Then the max contracts fade in — visibly above the line (top-coded)
self.play(FadeIn(max_dots))
# Callout: "max contracts cap at $55M — slope flattens artificially if included"
```

**Scene 11 — `AgingCurve` (7:25–7:55)**

Population aging curve, with a player dot moving along it.
```python
ax = Axes(x_range=[19, 40, 1], y_range=[0, 1.1, 0.2])
curve = ax.plot(aging_fn, x_range=[19, 40])
# Player dot starts at age 22 (Wemby), moves to right
# Y-value drops from 0.9 → 0.4 over the animation
# Caption: "wins decline ~5%/yr from age 28"
```

**Scene 12 — `MultiplierStack` (7:55–8:15)**

Five stacked bars showing how the multiplier grows.
```python
tiers = ["under cap", "above cap", "taxpayer", "1st apron", "2nd apron"]
mults = [0.5, 1.0, 1.5, 2.3, 3.1]
# Vertical bar chart, each bar appears as the tier is named
# A "$" symbol multiplier appears next to each bar
```

---

## Segment 5: The worst contracts (8:15–10:00) — 290 words

**Narration**:
> Apply the same model to the worst end of the league. Bottom five contracts in the NBA, in effective owner-dollars:
>
> Evan Mobley. Cleveland. Second apron. Negative six hundred forty-two million dollars in projected effective value over five years.
>
> Jaylen Brown. Boston. First apron. Negative four hundred twenty-nine.
>
> Luka Dončić. Lakers. First apron, repeater. Negative three hundred sixty-three.
>
> Anthony Edwards. Minnesota. First apron. Negative three hundred fifty.
>
> Donovan Mitchell. Cleveland. Second apron. Negative three hundred forty-two.
>
> Mobley is the worst contract in the league. He's a top-thirty player. He's twenty-four years old. His five-year max is in year one this season. The problem isn't him — it's the combination. Max contract plus Cleveland's deep second-apron status equals a tax multiplier on every dollar he makes for the rest of the decade.
>
> And look at Boston. Pritchard — the only positive contract in the openly-negotiated bucket — is on the same roster as Jaylen Brown, who's a bottom-five worst. Same team. Same GM. The bucket determines the outcome, not the front office.
>
> The pattern in every bottom-five contract: max deal on an apron team. The single most expensive failure mode in modern NBA roster construction is signing a max while already at the apron. Once you're locked in, you can't trade the player without taking back equivalent salary, you can't use the MLE to add depth, and the tax compounds annually.

### Manim scenes

**Scene 13 — `BottomFiveBars` (8:15–9:15)**

Horizontal bars descending into negative territory.
```python
players = ["Mobley", "J. Brown", "Dončić", "Edwards", "Mitchell"]
effective_npvs = [-642, -429, -363, -350, -342]  # in $M
teams = ["CLE", "BOS", "LAL", "MIN", "CLE"]
tier_colors_list = ["second_apron", "first_apron", "first_apron",
                    "first_apron", "second_apron"]

# Bars draw from zero downward, longest to shortest, with LaggedStart
# Number labels animate in from -$0 down to their target via ValueTracker
# After draw, the team logos appear in small frames next to each bar
# After the draw: highlight that Brown is on BOSTON (same team as Pritchard
#   from segment 3). Small Pritchard +$9.9M green callout floats in next to
#   Brown's red bar with a dotted-line: "same roster, opposite poles."
```

**Scene 14 — `MobleyAnnotation` (9:15–9:45)**

Mobley's bar highlights. Three callout boxes appear around it:
- "5-year max — year 1 of 5 this season"
- "Cleveland: 2nd apron"
- "Top-30 production, not top-5"
Each callout connects via a thin line to Mobley's bar.

**Scene 15 — `MaxOnApronPattern` (9:45–10:00)**

The five bars rearrange into a 5×2 grid showing (max contract) × (apron team) for each. A header animates in: "Every bottom-5 contract: max deal on apron team."

---

## Segment 6: The Pritchard scenario (10:00–11:30) — 250 words

**Narration**:
> Pritchard's contract is positive on Boston at nine point nine million. Boston's a first-apron team, so every dollar of his contract is amplified two point three times. But what about on the other twenty-nine teams?
>
> Same player, same contract, same three years. Thirty different team contexts.
>
> Brooklyn — under the cap floor — two point two million.
>
> Twenty-two teams — non-taxpayers — four point three.
>
> The Clippers — taxpayer with a repeater multiplier — eight point six.
>
> The first-apron group — Boston, Knicks, Houston, Minnesota — nine point nine million.
>
> Golden State and the Lakers — first apron with repeater — twelve.
>
> Cleveland — second apron — thirteen point three million.
>
> Six times the value, same contract, two different teams.
>
> Because the marginal dollar of cap space costs Cleveland three point one times what it costs Brooklyn. Pritchard on Cleveland doesn't just save salary — he saves the operational flexibility the team would otherwise lose under apron rules.
>
> Which is why every "best contracts" list disproportionately features contender role players. It's not that contenders find better bargains. **Contenders are the only teams whose math is amplified.** A rebuilding team with cap room sitting idle gets no apron savings. A contender stacks every minimum-deal sharpshooter because each one represents triple-digit thousand-dollar tax savings against the marginal alternative.

### Manim scenes

**Scene 16 — `Pritchard30Teams` (10:00–11:00)**

Horizontal bar chart. All 30 teams stacked vertically, sorted by effective NPV. Bars colored by tier.
```python
# Data: read from outputs/v4_pritchard_scenario.csv
teams_sorted = pritchard_scenario.sort_values("pritchard_effective_npv_m")
bars = BarChart(
    values=teams_sorted["pritchard_effective_npv_m"].tolist(),
    bar_names=teams_sorted["Tm"].tolist(),
    bar_colors=[TIER_COLORS[t] for t in teams_sorted["tier"]],
    y_range=[0, 16, 2],
)
bars.rotate(PI/2)  # make horizontal
# Bars draw in from left, longest last (most dramatic reveal)
# Annotations appear next to specific bars: BRK arrow → "$2.2M",
#   CLE arrow → "$13.3M"
```

**Scene 17 — `SixTimesCallout` (11:00–11:30)**

Two specific bars (BRK at top of negative, CLE at bottom = most positive)
pulled out and isolated. A "6×" multiplier text grows large between them.
Underneath: "Same contract. Same player. 6× the value."

---

## Segment 7: The next Pritchard (11:30–13:30) — 300 words

**Narration**:
> Last question. Who's next?
>
> The model says three names to watch. None of them are stars yet. All three are on the same setup that made Pritchard's deal: young, underpriced, and one decision away from either becoming the next Brad Stevens steal — or breaking out and getting market-rate elsewhere.
>
> Number one: **Neemias Queta**. Boston Celtics. Twenty-six years old. Playing top-five defensive rating in the NBA at the center spot for two point three million on a vet-min deal with a 2026-27 club option. Underpaid by eight million dollars in a single season. Stevens has the option, and on Boston — a first-apron team — Queta's effective surplus is twenty-nine point eight million. Highest single-player surplus on any contract in the league.
>
> The Stevens decision isn't "extend or lose him" — it's "pick up the team option for next year, then negotiate an extension before he walks in 2027." That window is open right now. Same playbook as Pritchard. Same team. And on the apron, three times the leverage.
>
> Number two: **Jalen Duren**. Detroit Pistons. Age twenty-two. Final year of rookie scale at six point five million. WA z-score of two point five — top-ten production in the league. First-time All-Star this season. And the Pistons already missed the window.
>
> Detroit's rookie extension deadline was October twentieth, 2025 — the day before the season opened. They didn't reach a deal. So Duren is now headed straight to restricted free agency this summer. The Pritchard playbook — extend the player before the market reprices — was available to Detroit four months before he made the All-Star team, and they passed.
>
> My contrarian bet: they pay for it. The market sets him at thirty million a year, Detroit matches the offer sheet, and the difference between "Pritchard outcome" and "Duren outcome" — same model says fifty million dollars of surplus over five years — comes down to one front-office hesitation in October.
>
> Number three: **Moussa Diabaté**. Charlotte Hornets. Age twenty-four. Vet minimum, two years remaining. Charlotte's already shown the playbook — Knueppel, Kalkbrenner, all on cheap multi-year deals. Diabaté is next. He's the under-the-radar pick.

### Manim scenes

**Scene 18 — `NextPritchardCalendar` (11:30–12:15)**

Vertical timeline running from now to October 2027. Three decision points highlighted.
```python
timeline = NumberLine(x_range=[2026.4, 2027.9, 0.25], length=8)
timeline.rotate(PI/2)  # vertical

decisions = [
    (2026.4, "Jun 2026", "Queta — Boston team option pickup"),
    (2026.6, "Summer 2026", "Duren — DET restricted free agent"),
    (2027.6, "Summer 2027", "Diabaté — CHO RFA window"),
]
# Each decision: a Dot on the timeline, a labeled callout to its left
# As each is narrated, the callout appears + the Dot pulses green
```

**Scene 19 — `QuetaSpotlight` (12:15–12:40)**

Queta isolated. Four-stat callout.
```python
stat_box = VGroup(
    Text("Neemias Queta — BOS", weight=BOLD),
    Text("Age 26   WA z = 1.7 (top 4%)"),
    Text("Salary: $2.3M    Market value: $10.4M"),
    Text("Underpaid by $8.0M • $29.8M effective on 1st apron"),
).arrange(DOWN, aligned_edge=LEFT)

# Below: timeline arrow pointing to "Jun 2026 — team option decision"
# Compare badge: small Pritchard portrait icon with text "Same template, same team, same GM"
```

**Scene 20 — `DurenForecast` (12:40–13:05)**

Two parallel scenarios.
```python
scenario_a = VGroup(  # left side
    Text("Detroit extends pre-deadline").set_color(HIGHLIGHT_GREEN),
    Text("4yr / $80M @ age 22"),
    Text("→ next Pritchard"),
)
scenario_b = VGroup(  # right side
    Text("Detroit waits → RFA").set_color(HIGHLIGHT_RED),
    Text("Market resets to $35M/yr"),
    Text("Detroit matches → no value"),
)
# Both scenarios appear simultaneously
# Then a model probability label appears between them: "Model: 65% scenario B"
```

**Scene 21 — `DiabateUnderRadar` (13:05–13:30)**

Diabaté card with team-pattern annotation.
```python
# Card-style layout. Stats. Then:
charlotte_pattern = VGroup(
    Text("Charlotte already extended cheap:"),
    BulletedList("Knueppel — 4yr rookie",
                 "Kalkbrenner — 4yr min",
                 "Diabaté — ???"),
)
# The "???" pulses with a "next" indicator
```

---

## Segment 8: Close (13:30–15:00) — 250 words

**Narration**:
> Three numbers to take with you.
>
> One of ninety-seven. Of every openly negotiated NBA contract with multi-year horizons, exactly one is projected to deliver positive surplus. Payton Pritchard. Signed by Brad Stevens *before* Pritchard's breakout.
>
> Fifty-five percent. The share of veteran-minimum contracts projected positive. The CBA-mandated bargain bucket produces more good contracts than the entire GM-negotiated bucket combined. The system that's keeping the NBA economy functional isn't competent front offices. It's the floor the league imposed.
>
> Six times. The same Pritchard contract is worth $2.2 million on the Nets and $13.3 million on Cleveland. The best contract in the NBA is a property of the team-contract fit, not the player.
>
> So the next time you watch a "best contracts" video, ask two questions. Did the GM negotiate this? And if so — was the player a sub-replacement nobody three months before they signed?
>
> Because that's the only contract anyone's ever genuinely negotiated well.

### Manim scenes

**Scene 22 — `ThreeNumbersReveal` (13:30–14:30)**

Big numeric counters that race up to their final value.
```python
# Three stat blocks arranged left-to-center-to-right
n1 = DecimalNumber(0, num_decimal_places=0)
n2 = DecimalNumber(0, num_decimal_places=0)
n3 = DecimalNumber(0, num_decimal_places=0)

# Sequential: each one counts up while narration says the number
self.play(n1.animate.set_value(1), run_time=1)
# label appears: "of 97 GM-negotiated contracts"
# pause
self.play(n2.animate.set_value(55), run_time=1.5)
# label: "% of vet min deals projected positive"
# pause
self.play(n3.animate.set_value(7), run_time=1)
# label: "× value range for Pritchard's contract"
```

**Scene 23 — `FinalQuestion` (14:30–15:00)**

Two-part question card.
```python
q1 = Text("Did the GM negotiate this?", weight=BOLD)
q2 = Text("Or did the CBA?")
# q1 fades in, then q2
# Q1 fades to red strikethrough on the second-to-last line
# Underneath, the punchline appears:
final = Text("Almost always, it was the CBA.").scale(0.8).set_color(HIGHLIGHT_GREEN)
self.play(Write(final))
# Hold 3s. End card.
```

---

## Production notes

### Word count summary

| Segment | Words | Time |
|---|---:|---:|
| Cold open | 100 | 0:45 |
| 1. Why lists are wrong | 270 | 2:00 |
| 2. Killer stat | 260 | 1:45 |
| 3. Pritchard story | 330 | 2:15 |
| 4. Methodology | 230 | 1:30 |
| 5. Worst contracts | 290 | 1:45 |
| 6. Pritchard 30 teams | 250 | 1:30 |
| 7. Next Pritchard | 300 | 2:00 |
| 8. Close | 250 | 1:30 |
| **Total** | **2,280** | **15:00** |

At 130 wpm, raw read time is 17:30. Manim scene holds and natural pauses account for the difference. If overshoot in edit, trim Segment 4 (methodology) first — it's the most cuttable for mainstream audience.

### Data files referenced

- `outputs/v4_one_of_97.png` → reference for Scene 6 dot layout (Pritchard's grid position)
- `outputs/v4_pritchard_scenario.csv` → Scene 16 data source
- `outputs/v4_bottom10_effective.csv` → Scene 13 data source
- `outputs/v4_next_pritchard_candidates.csv` → Scene 18-21 data source
- `outputs/BRIEF.md` → methodology reference for Scenes 5, 10-12

### Manim execution stack

- Manim Community v0.18+ recommended
- Render at 1080p for production, 540p for previews
- Background music: keep under -18 dB during narration. Drop out during the "1" reveal in Scene 6 for emphasis.

### Caveats for description (not script)

- Production model: composite z-score of VORP (×2.7) + WS. EPM would be tighter but not openly scrapeable.
- Open-market slope identifies $4.86M/z; an "all-sample" slope would be ~2× higher but biased by max top-coding.
- Bayesian shrinkage 15% toward zero. Multi-year priors would shift some rankings (Pritchard would actually rise — career trajectory has been upward).
- Aging curve is population mean. Outliers like Curry over-discounted by ~30-50%.
- Team multipliers are tier-level approximations. Real cap economics are continuous within tier.
- "1 of 97" sample: 1000+ minute players with 2+ contract years remaining.

### v2 → v4 → v4.1 number movements (do not reference v2 in script)

| Stat | v2 | v4 | v4.1 |
|---|---:|---:|---:|
| Pritchard naive NPV | $53M | $4.3M | $4.3M |
| Pritchard *effective* NPV (BOS) | — | $4.3M | **$9.9M** (BOS is 1st apron) |
| Mobley effective NPV | −$907M | −$642M | −$642M |
| Pritchard 30-team range | 14× | 7× | **6×** |
| Open-negotiation positive | many | 1 of 97 | **1 of 97** |
| Bottom-5 effective list | Mobley/Embiid/Anunoby/Towns/Curry | same | **Mobley/J.Brown/Dončić/Edwards/Mitchell** (PHI dropped from 1st apron; NYK/GSW dropped from 2nd; BOS moved up) |
