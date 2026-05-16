# Voiceover Script v1 — "1 of 97 NBA Contracts"

**Format:** teleprompter for self-recording.
**Target:** ~14:00 at ~125 wpm (analytical pace with breaths).
**Inspirations:** Thinking Basketball (analytical anchor) · Sebastian Lague
(walking-through-the-build feel) · Primer (intuition-first explainers) ·
Jxmy High Roller (opinionated, personal, NBA-fluent).
**POV:** first person throughout. You built this. You're showing it.

## Reading conventions
- One phrase per line. Blank line = breath beat (~250 ms).
- Em-dash ` — ` is a short pause (~150 ms).
- `...` is a longer trailing pause (~400 ms).
- `[beat]` = explicit hold, ~600 ms.
- `[pause]` = longer hold for landing, ~1.2 s.
- ALL CAPS = lean on the word.
- *(italics in parens)* = delivery note, not spoken.
- Inline explainer cards marked `[CARD: ...]` — these are quick Primer-style
  visual asides; the narration usually narrates the card.

---

# SEGMENT 1 — Cold open (0:00–0:40)

**VISUAL @ 0:00 — `ColdOpenNames`:** Names flicker across screen — JOKIĆ,
BRUNSON, SGA, WEMBY, DURANT, PRITCHARD, KORNET, AVDIJA, JALEN JOHNSON, NAW,
HALIBURTON, ŞENGÜN, MITCHELL, ROLLINS, REAVES.

*(conversational, like you're starting a chat)*

Every basketball channel makes the same video.

Top fifteen best contracts in the NBA.

[beat]

**VISUAL @ 0:08 — Screenshot / animated reveal of the CBS Sports article
"Ranking the 15 best contracts in the NBA," March 2026. Names of the top 3
(Avdija, Johnson, Brunson) highlight as they're spoken.**

Two months ago,
CBS Sports ran the thoughtful version of it.

Sam Quinn's piece — seven evaluation factors,
cross-referenced against an independent surplus-value model.

Avdija number one.
Jalen Johnson number two.
Brunson number three.

[beat]

It's a good article.
Better than the genre normally produces.

[beat]

**VISUAL @ 0:22 — `ColdOpenStat`:** Title-card build. "97 contracts.
1 positive." The "1" in green.

*(slight grin — you're about to share something you spent way too long on)*

And then I spent a month building my own model.

Every contract in the NBA — four hundred seventy-two of them —
priced against what the open market would actually pay,
projected forward across remaining years,
with aging and cap-tier penalties built in.

[beat]

And my model gets a different answer.

[pause]

*(slow, clean — this is the thesis)*

Of ninety-seven contracts that GMs actually negotiated...

exactly one is projected to deliver positive value over its remaining life.

[pause]

Just one.

[pause]

**VISUAL @ 0:42 — Smash cut to title card.**

---

# SEGMENT 2 — Why the question is wrong (0:40–2:00)

**VISUAL @ 0:40 — `FourBuckets`:** CBA box at top, four branches sprout
downward into labeled buckets — rookie scale, max, vet min, open negotiation.

*(stepping into teaching mode)*

Before I show you the model, I have to fix the question.

When somebody tells you Wemby has the best contract in the league —
they're sort of cheating.

[beat]

Every NBA contract falls into one of four buckets.

Rookie scale.
Max contracts.
Vet minimum.
And — open negotiation.

[beat]

The first three are written by the league, not the team.

A first-round pick gets paid on a CBA-fixed scale for four years.

[CARD: simple "rookie scale" graphic showing 4 fixed years]

A superstar's max is capped at thirty-five percent of the salary cap —
which is why Jokić, who'd make a hundred million on a true open market,
is "only" allowed to make fifty-five.

**VISUAL @ 1:15 — `JokicCap`:** Two bars — $100M green vs $55M red — with
a "CAP" line slicing the green.

A veteran on a minimum is on a salary FLOOR the league sets,
around two-point-three million.

[beat]

In none of those three cases
is the team really doing the negotiating.

The number was decided by the collective bargaining agreement
before anyone sat down at a table.

[pause]

So when I want to ask "did this front office make a smart contract decision" —

I have to throw out three quarters of the league
and look only at the fourth bucket.

Open negotiation.

Everything else.

The contracts where a GM and an agent actually had to argue
about a number.

[beat]

That's what I priced.

---

# SEGMENT 3 — Cap basics, in plain English (2:00–3:30)

*(warmer here — you're inviting the casual viewer in)*

Quick aside before I get to the math —

because the punchline depends on knowing how NBA payroll actually works,
and I don't want to assume.

[beat]

**VISUAL @ 2:08 — `CapLadder` (NEW):** Vertical ladder graphic. Five
horizontal lines stacked, labeled bottom to top: cap floor · salary cap ·
luxury tax · first apron · second apron. Dollar values float in next to
each line.

There's a salary cap.

Every team is supposed to spend
between a floor and a cap.

The floor is about a hundred forty million dollars this year.
The cap is about a hundred fifty-five.

[beat]

But this is the NBA, so nobody actually obeys the cap.

There's a soft cap with exceptions —
which means most teams spend more than the limit
and pay a luxury tax for the privilege.

Go a little over — you pay one-fifty per dollar.
Go a lot over — you pay three or four dollars on the dollar.

[beat]

And then on top of THAT, the new CBA introduced two new lines.

The first apron.
And the second apron.

If you cross the first apron — about a hundred ninety-six million in salary —
you lose roster-building tools.

[CARD: list, items appear one at a time]
"No mid-level exception."
"No sign-and-trade."
"No buyout players from teams over the apron."

The mid-level exception, by the way, is how teams normally sign
their best non-superstar free agents — like a four or five million
dollar slot that doesn't count against the cap normally.

Apron teams don't get it.

[beat]

If you cross the SECOND apron — about two-oh-eight million —
it gets worse.

[CARD: list]
"Your first-round pick seven years out gets frozen."
"You can't aggregate salaries in trades."
"You can't trade picks at all in some windows."

The second apron is the league's way of saying —

if you want to spend like the Dodgers, fine.
But you're not allowed to also have the best front office.

[beat]

And there's one more wrinkle.

The repeater tax.

If you've been a taxpayer for several years running,
your tax bill gets multiplied even more.

So a contract on, say, the Warriors —
who are a repeater AND near the second apron —
costs ownership maybe three times what it would on a non-taxpayer team.

[beat]

Hold onto that.

It's going to matter at the end.

---

# SEGMENT 4 — What I'm actually measuring (3:30–5:00)

**VISUAL @ 3:30 — `BuildTheFormula`:** Term-by-term equation build.
`predicted_salary = $2.3M + $4.86M · WA_z`. The slope highlighted.

*(faster — you're building intuition, not lecturing)*

OK. Back to the model.

I want one number for each contract that tells me —
did this player produce more value than he cost?

[beat]

To get there, I need three ingredients.

[beat]

One — how much value does a player produce in a season.

I take a composite of two box-score numbers — VORP and Win Shares —
and convert them into "wins above replacement."

A guy with a wins-added of zero is a fungible roster filler.
A wins-added of five is one of the best fifty players in the league.

[beat]

Two — what's a win actually worth on the market.

For every player on an OPEN-NEGOTIATION contract,
I plotted their wins-added against their salary,
and ran the regression line.

**VISUAL @ 4:00 — `PriceFitScatter`:** Scatter plot. Green dots clustered
along a regression line. Max contracts visibly above the line (top-coded).

The slope of that line is what GMs are actually willing to pay
for a standard deviation of production.

Four point eight six million dollars.

I only fit on open-negotiation contracts
because max deals get top-coded at the CBA ceiling
and minimums get floored at the bottom —
both ends would warp the slope.

[beat]

Three — I have to project that forward.

A four-year contract on a twenty-eight-year-old isn't worth the same
as a four-year contract on a twenty-three-year-old,
because players age.

For that I use a curve from Vaci et al. —
a twenty-nineteen paper in Behavior Research Methods
that fit Bayesian aging models across the entire Basketball-Reference dataset.

**VISUAL @ 4:25 — `AgingCurve`:** Population aging curve plotted. Y-axis is
"% of peak production." Key ages annotated.

Their result, which my model uses:
peak production at age twenty-six.
Roughly flat through twenty-seven.
Then progressive decline —
three percent at twenty-eight,
about five percent a year through your early thirties,
double digits by your mid-thirties.

[beat]

*(this is the important caveat — slow down a little)*

Big asterisk on that curve.

It's fit on the entire NBA POPULATION —
which is mostly role players and bench guys,
the kind who are out of the league by thirty-two.

Elite players age better than the average.

Curry at thirty-eight is producing way above what the curve predicts.
LeBron at forty broke the curve entirely.

[beat]

So if you're watching this thinking
"that decline schedule feels aggressive for the stars" —
you're right.
The curve underestimates outliers.

I use it anyway because it's the best openly available aging model
that I can plug in.
But every time we hit a player in their thirties later in this video —
Curry, KD, anyone graceful —
mentally tack on a "but the model is probably too harsh on him."

[beat]

**VISUAL @ 4:35 — `NPVExplainer` (NEW):** Animated breakdown. Year-by-year
boxes showing production value vs salary; discount factor shrinks the
future years; arrow sums to a final NPV number.

Now I have everything I need for the headline number.

For every year of every contract — and I have to define this once because
it'll come up a lot —

I subtract salary from production value to get the year's surplus.

A guy producing fifteen million of value who's paid ten million
gives the team five million of surplus that year.

Then I sum that across every remaining year of the contract,
discounting future years a little — same logic as a savings account,
a dollar five years out is worth less than a dollar today.

That total is the NPV.

[CARD overlay: "NPV = net present value. The total value of a contract
in today's dollars."]

Net present value.

It's the one number that tells me whether a contract is
a net win for the team or a net loss.

That's the stat.

---

# SEGMENT 5 — The killer stat (5:00–6:15)

**VISUAL @ 5:00 — `NinetySevenDots`:** 97 dots populate one by one in a
grid, then 96 turn red and 1 stays green.

So.

Ninety-seven open-negotiation contracts in the league this season
with multi-year horizons.

I run the NPV calculation on every one of them.

[beat]

How many are projected positive?

[pause]

[beat]

One.

[pause]

Payton Pritchard. Boston Celtics.

Four-year, thirty-million-dollar extension signed October eighth,
twenty twenty-three —
two years before he won Sixth Man of the Year.

Projected NPV — four point three million dollars.

[beat]

*(matter-of-fact, almost amused)*

Every other openly negotiated contract in the league
is projected to lose the team money on a multi-year horizon.

Jaime Jaquez. Saddiq Bey. Tre Jones.
Deni Avdija. Luke Kornet.

Every name your favorite YouTuber listed —
underwater.

[beat]

**VISUAL @ 5:50 — `BucketPositiveShare`:** Four bars by bucket — vet min
55%, rookie 10%, max 0%, open negotiation 1%.

And then compare that to the CBA-mandated buckets.

The veteran minimum bucket —
the floor the league imposes —
has fifty-five percent projected positive.

[pause]

*(lean in)*

The wage floor the league forces on every team
is generating more good contracts
than every front office in the NBA combined.

[beat]

That's the result I want to defend.

---

# SEGMENT 6 — How Pritchard happened (6:15–8:00)

**VISUAL @ 6:15 — `PritchardTimeline`:** Horizontal timeline 2020–2026
with career events and WA trajectory line graph above.

*(quieter — you're telling a story now)*

I want to walk through how Pritchard's contract happened,
because it's the template for everything I'm going to say later.

[beat]

October eighth, twenty twenty-three.

Pritchard at this point in his career is —
a backup guard averaging about six-and-a-half points a game
over three NBA seasons.

He's publicly asked Boston for a trade
because he wasn't getting minutes.

Boston had just lost the Eastern Conference Finals.

And as he's approaching restricted free agency,
the Celtics could have just let his rookie deal expire.

[beat]

Brad Stevens — the Celtics' president of basketball operations —
instead signs him to a four-year, thirty-million extension.

Less than the mid-level exception, on a guy who'd publicly asked out.

[beat]

Two years later, Pritchard wins Sixth Man of the Year.

His wins-added is in the top ten percent of the league.

And he's still on Stevens' extension —
making seven million dollars.

[pause]

**VISUAL @ 7:00 — `ThreeReasonsCallout`:** Three numbered callouts build
one at a time. Below reason 3: comparison rows for Avdija $13.75M/yr,
J. Johnson $30M/yr, Pritchard $7.5M/yr — only Pritchard's row gets a green
check.

Why is he the only one?

*(counting through, but conversational — not a checklist read)*

He was extended before the breakout, sure.

He's on a multi-year deal that lets the surplus compound, sure.

But the real lesson is the third thing.

[beat]

Other teams have tried the same playbook.

Atlanta extended Jalen Johnson in October twenty twenty-four,
before his All-Star season —
five years, one-fifty.

Washington extended Deni Avdija in October twenty twenty-three,
before he was traded to Portland and broke out —
four years, fifty-five.

[beat]

Both of those extensions came BEFORE the breakouts.

And both of them are still net-negative on my model.

[beat]

The difference is the price.

Pritchard's number was anchored on a six-points-per-game backup.
Avdija's number was anchored on a fifteen-points-per-game wing.
Johnson's number was anchored on a borderline-starter.

You need timing AND a low anchor.

Get one without the other and the math doesn't work.

[pause]

**VISUAL @ 7:55 — Side-by-side: CBS article ranking Avdija #1 vs. our
model's flat/slightly-negative NPV bar for Avdija. Two arrows pointing at
the same player.**

*(slowing down, sincere — the "let me steelman the other side" beat)*

Now — Avdija specifically is where this argument gets pushback.

Remember that CBS Sports piece from the cold open.
They ranked Avdija's contract the BEST in the NBA.

Their argument is real.
He's twenty-five and probably pre-peak.
His contract DESCENDS — Portland gets him cheaper each year.

[beat]

Where we disagree is the aging.

Remember the Vaci curve from earlier —
fit on the entire NBA population.
For a twenty-five-year-old at Avdija's production level,
it says he's roughly flat through twenty-seven,
then loses a few percent a year after that.

Quinn's model — and his eye test — say Avdija is going to KEEP improving.
He's exactly the kind of young-and-trending-up player
the population curve undershoots.

If they're right, Avdija is the steal of the decade.
If I'm right, the contract just about breaks even.

[beat]

Honest answer — somewhere between us, probably.

But here's the part that doesn't depend on Avdija.

Even if you give Quinn the full benefit of the doubt
and move Avdija from negative to positive on my model —

ninety-five of the other ninety-six open-negotiation contracts
are still net-negative.

Pritchard is still the only one we both agree on.

---

# SEGMENT 7 — How Boston pulled this off (8:00–9:45)

**VISUAL @ 8:00 — `BostonStory` (NEW):** Boston roster timeline. Porziņģis
+ Holiday appear in 2024 alongside title trophy. Then arrows out of Boston
(trade graphics). Then Queta + Pritchard ext. appear on the roster.

*(warmer — this is the segment where you let the basketball fan come out)*

But here's the thing that made me actually go build this whole model.

[beat]

In twenty twenty-four, Boston wins the championship.

Their team is Tatum, Brown, Holiday, Porziņģis, and Derrick White.

And then they immediately can't afford it.

[beat]

After the title, they're so far over the second apron
that the new CBA penalties start to bite.

So that offseason — July twenty twenty-five — they make two trades
on the same day that aren't really about basketball.
They're about payroll.

[beat]

Kristaps Porziņģis — gone.
Jrue Holiday — gone.

Both shipped out for cheaper salary and picks.

[beat]

And here's the part that should not have worked.

Boston in twenty twenty-five-twenty-six was supposed to fall off a cliff.

They didn't.

They had a great regular season.
Top seed in the East.

*(small grin)*

Lost to the Sixers in round one, but that's a different video.

[beat]

[CARD: roster strip showing six players. Pritchard, Queta, White,
Tatum, Brown, Kornet (struck out).]

How they pulled it off is the entire thesis of this model.

[beat]

They replaced Porziņģis and Holiday — two max-adjacent deals
that were collectively north of seventy million —
with the Pritchard extension already on the books,
Neemias Queta on the veteran minimum,
and Derrick White's pre-extension contract.

[beat]

Pritchard at seven million.
Queta at two point three.
A defensive anchor at center for less than
a top-twenty position-by-position salary.

[beat]

The Celtics' winning formula in twenty twenty-five
wasn't "we have stars."

Most of the league has stars.

It was — we found two open-negotiation contracts that priced low
AND turned into top-of-the-league production.

Which... is basically impossible to do twice.

Which is why my model says it happened ONCE in the entire NBA this year.

[pause]

And then they ran into a healthy Sixers team in the playoffs
and that's how basketball works.

---

# SEGMENT 8 — The same contract, thirty teams (9:45–11:00)

**VISUAL @ 9:45 — `Pritchard30Teams`:** Horizontal bar chart of 30 teams
sorted by Pritchard's effective NPV.

OK. One more model run before we land.

[beat]

I asked the model — what if Pritchard's exact contract,
seven million dollars a year for three more years,
were on every team in the league?

How does the math change?

[beat]

Brooklyn is under the cap floor.
Cap space is cheap to them.
Pritchard on the Nets would be worth — two point two million.

The middle of the league — twenty-two teams sitting between the cap and the
luxury tax — Pritchard's worth his open-market four point three.

[beat]

On Boston, where he actually plays,
the team is over the first apron.
Every dollar of his contract is leveraged against tax dollars
AND lost roster tools.
Pritchard's effective value to Boston is nine point nine million.

[beat]

The Lakers and Warriors — first apron with repeater bills — twelve.

Cleveland — second apron — thirteen point three million.

[pause]

**VISUAL @ 10:30 — `SixTimesCallout`:** CLE and BRK bars pulled out, "6×"
multiplier text between them.

Same player.
Same contract.
Same three years.

On Cleveland it's worth six times what it's worth on Brooklyn.

[beat]

*(landing — the conceptual punchline of the whole video)*

Which means the question "is this contract good"
doesn't have a single answer.

A great contract on a rebuilding team is a fine contract on a contender,
and a fine contract on a rebuilding team is a great contract on an
apron team.

The team you're on is doing half the work.

---

# SEGMENT 9 — The next one (11:00–12:15)

**VISUAL @ 11:00 — `NextPritchardCalendar`:** Three decision points
highlighted on a vertical timeline.

So which contracts might be the next Pritchard.

[beat]

Three names.

[beat]

**VISUAL @ 11:15 — `QuetaSpotlight`:** Queta isolated, four-stat callout,
"Jun 2026 — team option" badge.

Neemias Queta.
I just spent a segment on him so I won't repeat it.

But the model loves him.

Twenty-six years old.
Boston's defensive anchor at the center spot
(top-five defensive rating through the first month of the season).
On a veteran minimum with a team option for next year.

[beat]

**VISUAL: split-screen — left side shows our v4.1 Queta surplus at +$29.8M;
right side shows Stephen Noh's Sporting News surplus tool at +$30M+. Two
different colored model logos.**

And here's the moment to sanity-check the whole thing.

Stephen Noh at Sporting News runs an independent surplus-value tool.
Different stat foundation. Different methodology entirely.

His model puts Queta at a thirty-million-dollar surplus
on his two-point-three-million contract.

Mine puts him at twenty-nine point eight.

[beat]

When two unrelated models agree to within a million dollars —

that's the closest you get to "this is just real."

[beat]

If Stevens picks up the option in June and then extends him cheaply
before he hits free agency in twenty twenty-seven —

that's the second-generation Pritchard.

[beat]

**VISUAL @ 11:40 — `DurenForecast`:** Two-column scenario, but reframed —
left column showing "what could have happened," right "what actually
happened."

Jalen Duren in Detroit.

Twenty-two years old.
Top-ten in the league by my wins-added measure.
First-time All-Star this season.

Last summer, Detroit had a chance to extend him on his rookie scale —
the standard rookie-extension window for a 2022 draftee.

[CARD: short text "Reporting suggests Duren held out for more than
Detroit's offer."]

According to the reporting at the time,
Detroit offered something Duren felt was too low,
and Duren chose not to sign before the October twentieth deadline.

[beat]

He made the right bet.

He's now headed to restricted free agency this summer,
the All-Star vote ratified his ask,
and the market is going to pay him something like thirty million a year.

Detroit is almost certainly going to match the offer sheet.

[beat]

*(slight rueful tone)*

The gap between "Pritchard outcome" and "Duren outcome" —
same model says about fifty million dollars of surplus over five years —
comes down to whoever was more willing to take risk last October.

It looks like neither party blinked.

[beat]

**VISUAL @ 12:00 — `DiabateUnderRadar`:** Diabaté card with Charlotte
roster context.

And quickly — Moussa Diabaté in Charlotte.

Twenty-four, vet min, two years left.
Charlotte has Knueppel and Kalkbrenner on similar cheap deals.

If they play it right — that's the Pritchard pattern on a rebuilding budget.

---

# SEGMENT 10 — How to spot a good contract on your team (12:15–14:00)

**VISUAL @ 12:15 — `SpotterChecklist` (NEW):** Animated checklist. Three
questions appear one at a time, each with a "yes / no" branch beneath.

*(this is the takeaway — slow down, talk to the viewer directly)*

OK. I want to finish with something useful.

The reason I built this model
was that I wanted a way to look at my own team's roster
and tell whether the contracts the GM was signing
were actually a good idea.

[beat]

So here's the heuristic I came out with.

Three questions, in this order.

[beat]

**VISUAL: question 1 fades in.**

One — was this an open-negotiation contract?

If your team's "good contract" is a rookie scale or a vet min,
your GM didn't actually do anything.
The league mandated the price.

Pat them on the back, but it's not a roster-building skill.

[beat]

**VISUAL: question 2 fades in.**

Two — was the player a non-star when the contract was signed?

A contract signed AFTER a player breaks out
is paying for production the market has already seen.

The market will price it correctly, plus or minus a normal error.

A contract signed BEFORE a breakout
is one of the only ways to actually generate surplus.

So the question is —
when your GM signed this player,
was anyone outside your fanbase paying attention?

If yes, the deal is probably fine, not great.

If no — and the player has since gotten better —
that's the magic combination.

[beat]

**VISUAL: question 3 fades in.**

Three — and this is the one most people skip —
where is the team on the cap.

A surplus contract on a non-tax team
is a nice savings — maybe a few million in real dollars.

A surplus contract on a second-apron team
is the difference between contending and being forced
to trade your starting power forward.

[beat]

If your team's on the apron
and they keep finding cheap contributors —
that's a championship-level front office.

If your team's under the cap and your contracts are vibes —
the cap room is being wasted.

[pause]

*(closing — quiet, sincere)*

The reason "best contracts in the NBA" videos all feel kind of empty
is that they're showing you Wemby on his rookie scale
and pretending the Spurs front office did something.

[beat]

What I wanted —
and what I think you might want too —
is a way to look at YOUR team
and figure out whether the GM is actually playing this game well.

This is what I came up with.

[beat]

The model's not perfect.
I'll put the code in the description.

But the next time someone tells you their team has a great contract —

ask which bucket it's in.

Ask what the player was worth at signing.

Ask where the team is on the cap.

If the answers are good — they really did pull off something hard.

And if not — well —

[beat]

There's only ever been one Pritchard.

[pause]

**VISUAL @ 13:50 — End card / channel logo.**

---

## Things to call out for our next pass

1. **Cold open length** — trimmed from 45s to 40s by cutting one beat.
   If you want more setup, the easiest place to add is right before
   "So I spent a month building a model" — could insert one personal line
   about why the question bugs you.

2. **Cap basics segment (Segment 3)** — currently ~1:30. This is the
   biggest expansion vs v0. If it feels lecture-y when you read it aloud,
   the easiest cut is the repeater-tax line (60s in) — it's only relevant
   for the Pritchard scenario at the end.

3. **NPV explainer (Segment 4)** — I put the formal definition inline
   inside a card. If you want it as its own beat with a longer pause,
   move "Net present value. It's the one number..." up by 30 seconds and
   give it its own visual scene.

4. **Boston segment (Segment 8)** — the playoff-loss joke is written as a
   throwaway. Could be punched up or cut entirely depending on whether you
   want to sound more analytical (cut) or more like Jxmy (punch up).

5. **Duren framing** — I wrote it as "reporting suggests Duren held out."
   If you can confirm with a specific source you trust, name it on-screen
   in the card. If you can't, the current hedge works.

6. **Ending** — three-question heuristic. If you'd rather end with a
   personal note ("here's what I learned building this") instead of a
   how-to, let me know — I have a version of that I can swap in.

7. **Runtime** — current draft is ~2,250 words, which at 125 wpm is
   about 18 minutes. That's longer than the original 15-min target.
   Options: trim Diabaté segment (easy), tighten cap-basics (medium),
   cut Boston segment (hard — but it's a real option). Tell me which
   direction.

8. **LLM-trope sweep** — went through and killed every "not X, it's Y"
   I could find. There might still be one or two — flag any that read
   formulaic and I'll rework.

## Pronunciation hits
- Avdija — *AHV-dee-yah*
- Diabaté — *dee-ah-bah-TAY*
- Knueppel — *NUH-pul*
- Dončić — *DON-chitch*
- Şengün — *SHEN-gun*
- Jokić — *YOH-kitch*
- Porziņģis — *por-ZING-iss*
