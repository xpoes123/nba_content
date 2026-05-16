# ElevenLabs Narration Script — "1 of 97 NBA Contracts"

**Target length:** 15:00 (about 2,000 words at ~135 wpm for analytical pacing).
**Voice recommendation:** Daniel or Adam (low-mid male, analytical, similar
to Goldsberry / Thinking Basketball register). Stability ~45, similarity ~70.

## Prosody conventions used in this script
- `<break time="0.5s"/>` — SSML pause, supported by ElevenLabs v3+
- Em-dash ` — ` — short natural pause, ~250 ms (read aloud as a beat)
- Ellipsis `...` — trailing thought, ~400 ms
- ALL CAPS — verbal emphasis on the word
- All numbers are spelled out for consistent pronunciation
- Each segment is one ElevenLabs generation request (avoids prosody drift
  across 15 min of audio). Split at the `===` separators.

## On-screen imagery format
- `[VISUAL @ MM:SS — SceneName]` — what's on screen when this line is read.
  Manim scene class names match `outputs/manim/scenes/*.py`.

---

## SEGMENT 1 — Cold open (0:00–0:45)

[VISUAL @ 0:00 — ColdOpenNames: names flicker on/off in random screen positions —
JOKIĆ, BRUNSON, SGA, WEMBY, DURANT, PRITCHARD, KORNET, AVDIJA, JALEN JOHNSON,
NAW, HALIBURTON, SHENGUN, MITCHELL, ROLLINS, REAVES]

Every basketball channel makes the same video. <break time="0.4s"/> Top fifteen
best contracts in the NBA. The names rotate — Jokić, Brunson, S-G-A, Wemby —
but the list is always the same.

<break time="0.7s"/>

[VISUAL @ 0:18 — ColdOpenStat: names sweep off, big centered "97 contracts GMs
negotiated / 1 will deliver positive value" — the "1" in green]

So I built a model. Every contract in the NBA — four hundred seventy-two of
them — priced against the open-market shadow rate. Aging curves. Cap-tier
multipliers. The whole thing.

<break time="0.5s"/>

Then I sent it to a quant reviewer, and tore it apart twice.

<break time="0.8s"/>

Here's the punchline: of ninety-seven contracts that GMs actually negotiated...
<break time="0.6s"/> exactly ONE will deliver positive value to the team.

<break time="1.0s"/>

Just one.

<break time="1.2s"/>

[VISUAL @ 0:43 — smash cut to title card]

===

## SEGMENT 2 — Why every "best contracts" list is wrong (0:45–2:45)

[VISUAL @ 0:45 — FourBuckets: CBA box at top, four branches sprout downward
into labeled buckets (rookie scale, max, vet min, open negotiation)]

Every NBA contract falls into one of four buckets. <break time="0.3s"/> Three
of them are set by the collective bargaining agreement BEFORE any GM picks up
the phone.

<break time="0.5s"/>

Rookie scale — first-rounders, cost-controlled for four years.

<break time="0.4s"/>

Max contracts — superstars capped at thirty-five percent of the salary cap.
Jokić would make a hundred million on an open market. The C-B-A forbids more
than fifty-five.

[VISUAL @ 1:45 — JokicCap: two bars side by side, $100M green vs $55M red,
with a "CAP" line slicing the green]

<break time="0.5s"/>

Veteran minimum — a salary FLOOR for vets at two-point-three million.

<break time="0.5s"/>

And — <break time="0.3s"/> open negotiation. Everything else. The only bucket
where a GM and an agent actually negotiate a number.

<break time="0.7s"/>

So when a YouTuber tells you Wemby has the best contract in the league —
what they actually mean is — the C-B-A wrote his contract before any front
office got involved. Same for Brunson taking the max. Same for any second-
rounder on a vet min.

<break time="0.5s"/>

The interesting question isn't which C-B-A-mandated bargains exist. It's
which contracts that GMs ACTUALLY negotiated... beat the market.

<break time="0.6s"/>

[VISUAL @ 2:10 — BuildTheFormula: term-by-term equation build]

I priced them. Composite Wins Added — VORP converted to wins, plus Win
Shares. Regression line fit only on open-negotiation contracts. The slope
identifies what the market pays for a unit of production, free of C-B-A
constraints.

<break time="0.4s"/>

Four point eight six million dollars per standard deviation. Aging curve
from Vaci et al. Discount at five percent. Apply.

===

## SEGMENT 3 — The killer stat (2:45–4:30)

[VISUAL @ 2:45 — NinetySevenDots: 97 dots populate one by one in a grid,
then 96 turn red and 1 turns green]

Here's every contract in the league that's openly negotiated, played a
thousand minutes this season, and has at least two years remaining.
<break time="0.4s"/> Ninety-seven contracts.

<break time="0.5s"/>

For each, project remaining production with the aging curve. Apply Bayesian
shrinkage toward the league mean. Price against the open-market slope. Sum
the discounted surplus across remaining years.

<break time="0.6s"/>

Then ask — <break time="0.4s"/> how many are projected positive?

<break time="1.5s"/>

One.

<break time="1.0s"/>

Payton Pritchard. Boston Celtics. Four-year, thirty-million-dollar extension
signed October eighth, twenty twenty-three — two years before he won Sixth
Man of the Year. <break time="0.4s"/> Projected N-P-V surplus —
<break time="0.3s"/> four point three million dollars.

<break time="0.7s"/>

Every other openly negotiated contract in the league is projected
net-negative. <break time="0.3s"/> Jaime Jaquez. Saddiq Bey. Tre Jones. Deni
Avdija. Luke Kornet. <break time="0.4s"/> Every name your favorite YouTuber
listed — all underwater on a multi-year horizon.

<break time="0.7s"/>

[VISUAL @ 3:50 — BucketPositiveShare: four horizontal bars by bucket showing
% positive — vet min 55%, rookie 10%, max 0%, open negotiation 1%]

Now compare to the C-B-A-mandated buckets. <break time="0.3s"/> Veteran
minimum deals — fifty-five percent projected positive. <break time="0.5s"/>
The C-B-A's mandated FLOOR produces more good contracts than every GM in
the league combined.

===

## SEGMENT 4 — How is Pritchard the only one? (4:30–6:45)

[VISUAL @ 4:30 — PritchardTimeline: horizontal timeline 2020-2026 with career
events; WA_z trajectory line above]

So how. <break time="0.5s"/> Why him.

<break time="0.8s"/>

October eighth, twenty twenty-three. Brad Stevens signs Payton Pritchard to
a four-year, thirty-million-dollar extension. <break time="0.4s"/> At the
time, Pritchard is averaging five points per game over three N-B-A seasons.
He's publicly asked for a trade because he isn't getting minutes. He's a
restricted free agent in waiting. <break time="0.3s"/> Boston has just lost
the Eastern Conference Finals.

<break time="0.6s"/>

Stevens doesn't trade him. He extends him — <break time="0.3s"/> for less
than the mid-level exception.

<break time="0.7s"/>

Two seasons later, Pritchard wins Sixth Man of the Year. His Wins Added
composite — top ten percent of the league — gets him onto a deal that pays
him seven million dollars.

<break time="0.8s"/>

[VISUAL @ 5:30 — ThreeReasonsCallout: three numbered reasons build one at a
time; below reason 3, comparison rows for Avdija / J. Johnson / Pritchard]

Three reasons he's the only positive contract on the board.

<break time="0.5s"/>

One — he was extended BEFORE the breakout. The price was set on his pre-
twenty-twenty-four production. The market had no idea he was about to become
a seventeen-points-a-night scorer.

<break time="0.5s"/>

Two — length compounds. Three years remaining at seven million ascending to
eight, all guaranteed. Every season at his current level produces seven-
figure surplus.

<break time="0.6s"/>

Three — and this is the subtle one. <break time="0.4s"/> Pritchard is the
only one whose price was anchored LOW and stayed there. Other teams have
tried the same playbook — extend a guy before he breaks out — but at a
market-rate number.

<break time="0.4s"/>

Atlanta extended Jalen Johnson in October twenty twenty-four, pre-All-Star,
for one-fifty over five years. <break time="0.3s"/> Washington extended Deni
Avdija in October twenty twenty-three, pre-Portland trade, for fifty-five
over four. <break time="0.5s"/> Both of those came before the breakout.
Both are still underwater — because the PRICE was too high.

<break time="0.7s"/>

Pritchard's extension is the only one in the league where the price was
anchored on a five-points-per-game backup, <break time="0.3s"/> and then
the player turned into a Sixth Man of the Year. <break time="0.5s"/>
Price plus timing. <break time="0.4s"/> Everyone else got one... or the
other.

===

## SEGMENT 5 — The framework, briefly (6:45–8:15)

[VISUAL @ 6:45 — PriceFitScatter: scatter of WA_z vs salary, regression line
through open-negotiation dots, max dots visibly above the line]

Brief detour for the quants. The model was built skeptically.

<break time="0.5s"/>

The price. <break time="0.3s"/> Four point eight six million dollars per
standard deviation of production, fit on open-negotiation contracts only.
Max-contract slopes are misleading because they're top-coded at the C-B-A
ceiling. Min deals are floored. Only the open-negotiation bucket reveals
the unconstrained market slope.

<break time="0.6s"/>

[VISUAL @ 7:25 — AgingCurve: population aging curve, player dot moving right]

The aging. <break time="0.3s"/> Population aging curve. Peak at twenty-six,
seven-to-eight percent decline per year through thirty-two, accelerating
after. <break time="0.3s"/> Applied in win units, not z-units. An earlier
version applied aging directly to z-scores, which gave negative-W-A players
a free improvement from regression to the mean. <break time="0.3s"/> Bug,
fixed.

<break time="0.5s"/>

[VISUAL @ 7:55 — MultiplierStack: five stacked bars for tier multipliers]

The team context. A dollar of salary doesn't cost a dollar. On a tax team —
a buck fifty. On a second-apron team — three-and-a-half. Apron premium added
on top — lost mid-level exception, no aggregation in trades, frozen first-
round picks.

<break time="0.5s"/>

Bayesian shrinkage of fifteen percent. The model is conservative. Pritchard
survives a more aggressive prior. <break time="0.3s"/> Most of the overpays
at the bottom survive shrinkage too.

===

## SEGMENT 6 — The worst contracts (8:15–10:00)

[VISUAL @ 8:15 — BottomFiveBars: five horizontal bars descending into
negative territory; Mobley longest, then Brown, Dončić, Edwards, Mitchell]

Apply the same model to the worst end of the league. Bottom five contracts
in the N-B-A, in effective owner-dollars.

<break time="0.6s"/>

Evan Mobley. Cleveland. Second apron. <break time="0.3s"/> Negative six
hundred forty-two million dollars in projected effective value over five
years.

<break time="0.6s"/>

Jaylen Brown. Boston. First apron. <break time="0.3s"/> Negative four
hundred twenty-nine.

<break time="0.5s"/>

Luka Dončić. Lakers. First apron, repeater. <break time="0.3s"/> Negative
three hundred sixty-three.

<break time="0.5s"/>

Anthony Edwards. Minnesota. First apron. <break time="0.3s"/> Negative
three hundred fifty.

<break time="0.5s"/>

Donovan Mitchell. Cleveland. Second apron. <break time="0.3s"/> Negative
three hundred forty-two.

<break time="0.8s"/>

[VISUAL @ 9:15 — MobleyAnnotation: Mobley's bar highlighted with three
callout boxes — "5-year max — year 1 of 5", "Cleveland: 2nd apron",
"Top-30 production, not top-5"]

Mobley is the worst contract in the league. He's a top-thirty player. He's
twenty-four years old. His five-year max is in year ONE this season.
<break time="0.4s"/> The problem isn't him — it's the combination. Max
contract plus Cleveland's deep second-apron status equals a tax multiplier
on every dollar he makes for the rest of the decade.

<break time="0.8s"/>

And look at Boston. <break time="0.4s"/> Pritchard — the ONLY positive
contract in the openly-negotiated bucket — is on the same roster as Jaylen
Brown, who's bottom-five worst. <break time="0.5s"/> Same team. Same GM.
The bucket determines the outcome — not the front office.

<break time="0.8s"/>

[VISUAL @ 9:45 — MaxOnApronPattern: five bars rearrange into 5-by-2 grid
of (max contract) × (apron team)]

The pattern in every bottom-five contract — max deal on an apron team. The
single most expensive failure mode in modern N-B-A roster construction is
signing a max while already at the apron. Once you're locked in, you can't
trade the player without taking back equivalent salary, you can't use the
M-L-E to add depth, and the tax compounds annually.

===

## SEGMENT 7 — The Pritchard scenario (10:00–11:30)

[VISUAL @ 10:00 — Pritchard30Teams: horizontal bar chart of 30 teams sorted
by Pritchard's effective NPV, colored by tier]

Pritchard's contract is positive on Boston at nine point nine million.
Boston's a first-apron team, so every dollar of his contract is amplified
two-point-three times. <break time="0.4s"/> But what about on the other
twenty-nine teams?

<break time="0.6s"/>

Same player. Same contract. Same three years. Thirty different team
contexts.

<break time="0.7s"/>

Brooklyn — under the cap floor — two point two million.

<break time="0.4s"/>

Twenty-two teams — non-taxpayers — four point three.

<break time="0.4s"/>

The Clippers — taxpayer with a repeater multiplier — eight point six.

<break time="0.4s"/>

The first-apron group — Boston, the Knicks, Houston, Minnesota — nine point
nine million.

<break time="0.4s"/>

Golden State and the Lakers — first apron with repeater — twelve.

<break time="0.4s"/>

Cleveland — second apron — thirteen point three million.

<break time="0.9s"/>

[VISUAL @ 11:00 — SixTimesCallout: CLE and BRK bars pulled out, "6×"
multiplier text grows large between them, tagline "Same contract. Same
player. 6x the value."]

Six times the value. <break time="0.4s"/> Same contract. Two different teams.

<break time="0.6s"/>

Because the marginal dollar of cap space costs Cleveland three-point-one
times what it costs Brooklyn. <break time="0.4s"/> Pritchard on Cleveland
doesn't just save salary — he saves the operational flexibility the team
would otherwise lose under apron rules.

<break time="0.6s"/>

Which is why every "best contracts" list disproportionately features
contender role players. It's not that contenders find better bargains.
<break time="0.5s"/> Contenders are the only teams whose math is amplified.
A rebuilding team with cap room sitting idle gets no apron savings. A
contender stacks every minimum-deal sharpshooter because each one represents
triple-digit thousand-dollar tax savings against the marginal alternative.

===

## SEGMENT 8 — The next Pritchard (11:30–13:30)

[VISUAL @ 11:30 — NextPritchardCalendar: vertical timeline running now to
Oct 2027, three decision points highlighted in green]

Last question. <break time="0.5s"/> Who's next?

<break time="0.7s"/>

The model says three names to watch. None of them are stars yet. All three
are on the same setup that made Pritchard's deal — young, underpriced, and
one decision away from either becoming the next Brad Stevens steal — or
breaking out and getting market-rate elsewhere.

<break time="0.9s"/>

[VISUAL @ 12:15 — QuetaSpotlight: Queta isolated, four-stat callout box,
"Jun 2026 — team option decision" badge, PP comparison badge]

Number one. <break time="0.3s"/> Neemias Queta. Boston Celtics. Twenty-six
years old. Playing top-five defensive rating in the N-B-A at the center
spot — for two point three million on a vet-min deal with a twenty
twenty-six-twenty-seven club option. <break time="0.4s"/> Underpaid by
EIGHT million dollars in a single season.

<break time="0.5s"/>

On Boston — a first-apron team — Queta's effective surplus is twenty-nine
point eight million dollars. <break time="0.3s"/> Highest single-player
surplus on any contract in the league.

<break time="0.5s"/>

The Stevens decision isn't "extend or lose him" — it's pick up the team
option for next year, then negotiate an extension before he walks in
twenty twenty-seven. <break time="0.4s"/> That window is open right now.
Same playbook as Pritchard. Same team. <break time="0.4s"/> And on the
apron — three times the leverage.

<break time="0.9s"/>

[VISUAL @ 12:40 — DurenForecast: two-column scenario — left "Counterfactual:
ext. by Oct 2025" green, right "What happened: deadline closed" red]

Number two. <break time="0.3s"/> Jalen Duren. Detroit Pistons. Age twenty-
two. Final year of rookie scale at six point five million. Wins-Added
z-score of two point five — top-ten production in the league. First-time
All-Star this season.

<break time="0.6s"/>

And the Pistons already missed the window.

<break time="0.7s"/>

Detroit's rookie extension deadline was October twentieth, twenty twenty-
five — the day before the season opened. They didn't reach a deal. So
Duren is now headed straight to restricted free agency this summer.
<break time="0.4s"/> The Pritchard playbook — extend the player BEFORE the
market reprices — was available to Detroit four months before he made the
All-Star team. <break time="0.4s"/> And they passed.

<break time="0.7s"/>

My contrarian bet — they pay for it. The market sets him at thirty million
a year. Detroit matches the offer sheet. And the difference between
"Pritchard outcome" and "Duren outcome" — same model says fifty million
dollars of surplus over five years — comes down to one front-office
hesitation in October.

<break time="0.9s"/>

[VISUAL @ 13:05 — DiabateUnderRadar: Diabaté card, Charlotte bullet list
(Knueppel, Kalkbrenner, Diabaté)]

Number three. <break time="0.3s"/> Moussa Diabaté. Charlotte Hornets. Age
twenty-four. Vet minimum, two years remaining. <break time="0.4s"/>
Charlotte's already shown the playbook — Knueppel, Kalkbrenner — all on
cheap multi-year deals. Diabaté is next. <break time="0.4s"/> He's the
under-the-radar pick.

===

## SEGMENT 9 — Close (13:30–15:00)

[VISUAL @ 13:30 — ThreeNumbersReveal: three numeric counters race up to
final values — 1, 55%, 6×]

Three numbers to take with you.

<break time="1.0s"/>

ONE of ninety-seven. <break time="0.4s"/> Of every openly negotiated N-B-A
contract with multi-year horizons — exactly one is projected to deliver
positive surplus. <break time="0.3s"/> Payton Pritchard. Signed by Brad
Stevens BEFORE Pritchard's breakout.

<break time="0.9s"/>

Fifty-five percent. <break time="0.4s"/> The share of veteran-minimum
contracts projected positive. <break time="0.3s"/> The C-B-A-mandated
bargain bucket produces more good contracts than the entire GM-negotiated
bucket combined. <break time="0.4s"/> The system that's keeping the N-B-A
economy functional isn't competent front offices. <break time="0.3s"/>
It's the floor the league imposed.

<break time="0.9s"/>

Six times. <break time="0.4s"/> The same Pritchard contract is worth two
point two million dollars on the Nets — and thirteen point three million
on Cleveland. <break time="0.4s"/> The best contract in the N-B-A is a
property of the team-contract fit — not the player.

<break time="1.2s"/>

[VISUAL @ 14:30 — FinalQuestion: closing title card]

So the next time you watch a "best contracts" video — ask two questions.
<break time="0.4s"/> Did the GM negotiate this? <break time="0.5s"/> And
if so... <break time="0.5s"/> was the player a sub-replacement nobody
three months before they signed?

<break time="0.8s"/>

Because that's the only contract... <break time="0.5s"/> anyone's ever
genuinely negotiated well.

<break time="1.5s"/>

[VISUAL @ 14:55 — end card / channel logo]

===

## Notes for delivery

**If ElevenLabs doesn't honor `<break time="X.Xs"/>` tags** (some lower
tiers strip SSML), regenerate with a comma-and-ellipsis-only version — the
em-dashes and ellipses already encode most of the pacing. Drop the explicit
breaks; the punctuation will carry it.

**Pronunciation hints for the model:**
- "Pritchard" — standard, no overemphasis on the "tch"
- "Avdija" — *AHV-dee-yah* (not "ah-vuh-dee-jah")
- "Jokić" — *YOH-kitch*
- "Diabaté" — *dee-ah-bah-TAY* (French final stress)
- "Knueppel" — *NUH-pul*
- "Dončić" — *DON-chitch*
- "Antetokounmpo" — not in this script; if you reference him in pickup
  edits, *AHN-teh-toh-KOON-poh*
- "Šengün" / "Şengün" — *SHEN-gun* (script writes "Şengün"; ElevenLabs may
  prefer "SHEN-gun" inline)
- "NPV" / "MLE" / "CBA" / "RFA" — script spells these out letter-by-letter
  via hyphens ("N-P-V") so the model doesn't try to say them as words

**Per-segment generation:** generate each `===` block separately, then
concat. Prevents prosody drift across the 15 min, and lets you re-roll a
single segment if the read is off.

**Music bed:** Keep under −18 dB during narration. Drop out entirely during
the "Just one." beat at 0:40 and the "ONE of ninety-seven" reveal at
13:35. Bring back up under each `[VISUAL]` transition.
