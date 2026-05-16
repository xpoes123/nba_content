# nba_content

Analytical NBA video projects. Each video lives in its own subdirectory
under `videos/`, with its own data pipeline, model code, outputs, and
animation scenes.

## Current and planned videos

| # | Slug | Status | Headline |
|---|------|--------|----------|
| 01 | `contracts` | Script complete, model v4.1 frozen | *"Of 97 GM-negotiated NBA contracts, exactly one delivers positive value."* |
| 02+ | TBD | See [`IDEAS.md`](IDEAS.md) | Ten seed concepts, persona-pressure-tested |

## Repo layout

```
nba_content/
├── IDEAS.md             # Final 10 video ideas with research, persona heatmaps, headline candidates
├── IDEAS_v0.md          # v0 draft used for persona pressure-testing (kept for reference)
├── videos/
│   └── 01_contracts/
│       ├── data/        # Scraped + processed contract / advanced-stats data
│       ├── src/         # Pipeline (fetch → clean → value → final)
│       └── outputs/     # CSVs, charts, brief, video outline, animator brief, manim
└── .venv/               # Python env (gitignored)
```

## Tooling

- Python 3.13 via mise
- pandas, numpy, scikit-learn for the modeling pipelines
- [Manim Community](https://www.manim.community/) for animation
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for transcript pulls when researching prior art

## Conventions

- Each video subdir is self-contained: its `src/` scripts use
  `Path(__file__).resolve().parents[1]` so they keep working regardless
  of where the video subdir lives.
- Heavy render artifacts (`outputs/manim/logs/`, `outputs/manim/media/`)
  are gitignored. The scene source and `data_loader.py` are tracked,
  so any video can be re-rendered from a fresh clone with `bash
  outputs/manim/render_all.sh h`.
- Methodology is defensible-first: every published claim has to survive
  an adversarial review pass. See `videos/01_contracts/outputs/BRIEF.md`
  for the format.

## Inspirations

[Thinking Basketball](https://www.youtube.com/@ThinkingBasketball) ·
[Sebastian Lague](https://www.youtube.com/@SebastianLague) ·
[Primer](https://www.youtube.com/@PrimerBlobs) ·
[Jxmy High Roller](https://www.youtube.com/@JxmyHighroller)
