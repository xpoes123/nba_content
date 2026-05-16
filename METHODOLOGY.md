# Idea Vetting Methodology

How any new video idea on this channel gets evaluated before it earns a slot
in [`IDEAS.md`](IDEAS.md) (or commits to production). The same framework was
used to triage the first 10 ideas, and again to assess the playstyle
clustering pitch.

The goal is to **kill weak ideas before spending six weeks on them**, and to
sharpen surviving ideas with feedback from the audiences that will actually
watch / share / pick them apart.

---

## When to run this

- A new idea has been pitched and feels promising but not obviously
  greenlight-ready.
- An existing idea in `IDEAS.md` needs to be re-evaluated after new
  research or audience feedback.
- A topic has been done by someone else and you need to decide whether
  the differentiation is real.

If an idea is obviously bad (no data, no hook, no audience), skip the
process — it's not worth the agent runs. If an idea is obviously
greenlight (unanimous strong fit, existing pipeline, clear headline),
also skip — just add it and move on.

---

## The framework

Six stages. Stages 1–3 are mandatory. Stage 5 is conditional on Stage 4
findings.

### Stage 1 — v0 idea card

A single markdown file at `vetting/<idea_slug>_v0.md` with:

- **3 hook candidates** — different angles, different headline-number
  claims. The pressure-test panel will rate them against each other.
- **Channel fit** — 1–2 sentences on why this matches the channel's
  style (Thinking Basketball / Lague / Primer / Jxmy register).
- **Data sources** — explicit list. Free vs. paywalled. Coverage
  windows. If a hook needs data you don't have access to, flag it.
- **Methodology sketch** — feature space, model class, evaluation,
  era handling, talent controls. Be honest about what's a sketch vs.
  what's load-bearing.
- **Risks** — saturation, known null results, sample-size traps,
  confounds, ethical / FO-realism issues. List at least 3.
- **Effort** — weeks of solo work, including animation. Include an
  EDA-gate option for risky ideas: spike for 1–2 weeks, kill if the
  numbers don't land.

If the cursory research has already happened (Stage 2), summarize its
verdict at the bottom of the v0 card with a date.

### Stage 2 — Cursory research

One Explore-class research agent. **Goal:** survey existing work in the
space, identify the gap, brainstorm 5 candidate headline numbers,
enumerate methodology gotchas, confirm data accessibility.

Time budget: 2–3 minutes of agent runtime, ~1200-word report.

Save output to `vetting/<idea_slug>_research.md`.

If the cursory research returns "this has been definitively done and the
known result is a null" — kill the idea here. Don't waste persona runs
on it. (Example: the original "tanking doesn't work" framing died at
this stage; only the asset-conversion reframe survived.)

### Stage 3 — Five-persona pressure test

Five agents, run in parallel. Each gets the v0 card + cursory research
and reacts. Each persona has a fixed perspective so reactions don't
collapse into the same critique:

| Persona | What they care about | Will kill the idea if... |
|---|---|---|
| **Quant Discord** | Methodology rigor, prior art, p-hacking risks, statistical assumptions | The headline is a known null result, or methodology has obvious p-hack vectors |
| **Sharp sports bettor** | Can this analysis generate a +EV bet? Live model possibility? Edge above Pinnacle's close? | The methodology is purely retrospective and the topic doesn't price into any market |
| **Casual NBA fan** | Click / watch-through / share. Named players, emotional hook, thumbnail magnetism | The video sounds like homework or the hook isn't a sentence with stakes |
| **Ex-NBA FO analyst** | Does this match how teams actually think? Does it engage with real CBA / scheme / scouting mechanics? | The framing is fan/media fiction dressed up in math, or it misses a real-world mechanic that breaks the analysis |
| **YouTube strategist** | Thumbnail concept, title testing, retention drop points, discoverability, expected views ceiling | The thumbnail can't carry without faces/logos/emotion, or retention drops too early |

Each persona returns a 700–1200 word reaction with a verdict
(greenlight / reframe / kill), specific critiques, and a ranked
preference between the hook candidates.

Save all five reports under `vetting/<idea_slug>_personas/` (or paste
into the synthesis doc directly).

Persona prompt templates are at the end of this doc.

### Stage 4 — Synthesis

Read all five persona reactions and produce a decision summary at
`vetting/<idea_slug>.md`:

- **Convergence**: where do personas agree? Strong convergence = high
  confidence in the verdict.
- **Divergence**: where do they disagree? Often the divergence IS the
  finding (e.g., "what casual fans want is exactly what quants will
  dunk on" is a genuine creative tension worth naming).
- **Verdict**: greenlight / reframe / kill, with the reasoning explicit.
- **If reframe**: what specifically needs to change for the idea to
  survive? Spell out the new hook.
- **If kill**: what to make instead — point to a specific entry in
  `IDEAS.md`, or note the topic as parked.

### Stage 5 — Deep research on survivors (conditional)

If the verdict is **greenlight or strong reframe**, run a deeper
research agent on the sharpest 1–2 questions:

- What's the specific headline number candidate the data will land?
- Where does the methodology need to be airtight to survive the quant's
  attack vector?
- What case studies / named entities anchor the narrative?
- What's the concrete week-by-week effort breakdown?

Save to `vetting/<idea_slug>_deep_research.md`.

For obvious-kill ideas, skip this entirely.

### Stage 6 — Update `IDEAS.md`

If greenlit:
- Add the idea to `IDEAS.md` with the standard format: hook + persona
  heatmap + headline candidates + data sources + methodology sketch +
  risks + prior work + effort.
- Use the persona reactions verbatim where useful — the heatmap is the
  most valuable part for the creator's future decisions.

If killed:
- Log the kill decision in the synthesis doc at `vetting/<idea_slug>.md`
  with a short rationale. Don't pollute `IDEAS.md` with rejected ideas;
  the vetting/ folder is the graveyard.

---

## File layout

```
nba_content/
├── METHODOLOGY.md                       # this file
├── IDEAS.md                             # accepted ideas
├── vetting/
│   ├── <idea_slug>_v0.md                # the v0 card
│   ├── <idea_slug>_research.md          # cursory research (optional)
│   ├── <idea_slug>_personas/            # five persona reactions (or inline)
│   ├── <idea_slug>_deep_research.md     # only if survived to Stage 5
│   └── <idea_slug>.md                   # synthesis + decision
└── videos/<NN>_<slug>/                  # only created if production starts
```

Add `vetting/` to git so the kill decisions are part of the audit trail —
future you will be grateful you can see why an idea was rejected.

---

## Persona prompt templates

Paste these into a new Agent call. Replace `<v0_card_path>` and any
context-specific lines as needed. Templates assume the v0 card and
cursory research are already saved under `vetting/`.

### Quant Discord

```
You are a member of a quantitative sports analytics Discord — APBRmetrics
subscriber, Nylon Calculus archive reader, RAPM-aware, allergic to
handwaving, posts methodology critiques on Twitter.

Read: <v0_card_path>

React as a Discord thread comment:
- Verdict: greenlight / reframe-needed / kill.
- What's defensible about each hook? Which is least dunkable?
- What's the obvious "actually..." critique?
- What prior work would you cite as supporting or replacing the idea?
- What specific data choices could blow up the analysis?
- Would you watch? Yes / no / only if it engages with X.

Be specific. Cite analysts by name. End with the 3 hook candidates ranked
by Discord-defensibility.

Format: structured markdown, under 1000 words.
```

### Sharp sports bettor

```
You are a sharp NBA sports bettor. You read every angle for edge but only
care about whether the analysis produces a number that beats Pinnacle's
close.

Read: <v0_card_path>

React:
- Is there a bet this could inform? Be specific about market.
- Would the headline number price into any market or is it narrative?
- Live model possibility or strictly retrospective?
- Would you bookmark the spreadsheet / follow the repo / hit like and move
  on?

End with one concrete bet you'd shop tomorrow if the analysis were done.
Be blunt — if the betting hook is weak say so plainly.

Format: structured markdown, under 800 words.
```

### Casual NBA fan

```
You are a casual but engaged NBA fan. You watch your team most games, you
follow League Pass during the playoffs. You've heard of "playstyles" but
you couldn't define one. You click YouTube videos with strong opinions,
named players, and clear visuals.

Read: <v0_card_path>

React:
- Of the three hook candidates, which makes you click?
- Could you explain the thesis to a friend after watching, in one sentence?
- What would feel boring or "too academic"?
- What thumbnail would actually get the click?

End with: would you click? Would you watch all the way through? Would you
share?

Don't overthink. Format: structured markdown, under 700 words.
```

### Ex-NBA front-office analyst

```
You are a former NBA front-office analyst, now consulting. You spent 6
years in a basketball-ops department working with tracking, lineup, and
scouting data. You know which "obvious" stats teams ignore and which
"hidden" ones they actually use.

Read: <v0_card_path>

React:
- Is the framing how teams actually think? Or fan/media frame in math?
- What's the question teams ASK internally that the video could pivot
  toward?
- What real-world mechanic does the analysis miss without insider context?
- What public analyst has come closest on this topic?
- Would teams find this video interesting?

End with: would you send this to your GM, or would they laugh at you?

Format: structured markdown, under 1000 words.
```

### YouTube strategist

```
You are a YouTube creator strategist for mid-tier analytical channels
(50k–500k subs). You know thumbnails, titles, retention curves, the
magnetism of specific data viz styles. You watch the metrics, not the vibes.

Channel reference: Thinking Basketball, Sebastian Lague, Primer, Jxmy High
Roller. Solo creator, Manim-capable, 4–10 weeks per video. Discord-quant
audience growing into casuals.

Read: <v0_card_path>

React:
- Of the hooks, which is the strongest title? 2–3 variants each.
- Thumbnail concept. What works for this niche?
- Retention drop points and fixes.
- Discoverability — news peg, controversy, evergreen interest?
- Is the title overpromising or underselling?
- Compared to ideas in IDEAS.md, where does this rank by expected views
  ceiling?

End with: would you green-light this over [name two specific alternatives
from IDEAS.md], ranked.

Format: structured markdown, under 1000 words.
```

---

## A note on cost discipline

Each round costs 5–6 agent runs (1 cursory + 5 personas + optional 1–2
deep) and ~30 minutes of synthesis. That's cheap relative to the cost of
shipping a bad video. But it's not free.

The framework's job is to be ruthless. Most ideas should fail the panel —
that's the success state, not the failure state. The contracts video took
the panel only because the methodology was already built and the headline
was already proven; most fresh ideas need at least one round of reframing.

If the panel keeps agreeing with you, you're either picking very strong
ideas, or you're prompting the personas too soft. Recalibrate by giving
them sharper criteria the next round.

---

## Worked examples

- `vetting/playstyle_clustering.md` — the playstyle clustering idea
  (pitched 2026-05-16). See for a worked example of synthesis after the
  panel.
- `IDEAS_v0.md` + agent transcripts — the original 10-idea pressure test
  that produced `IDEAS.md`. Reference for what a successful panel pass
  looks like.
