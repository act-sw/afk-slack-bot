# Contributing

Issues and pull requests are welcome — bug reports, translations for a new
locale, or small features in the spirit of the project (see the
architectural invariants in [README.md](README.md#-architectural-invariants)
before touching the queue/state/Canvas plumbing).

There's no CI or test suite yet, so:

- Keep changes focused and easy to review.
- If you touch `duration_parser.py`, `canvas_renderer.py`, or `i18n.py`,
  sanity-check by hand against a few real inputs (including non-English
  locales, if relevant) and mention what you checked in the PR description.
- Match the existing code style (no docstrings beyond a one-line "why" where
  genuinely non-obvious, no speculative abstractions).

For anything bigger than a small fix, opening an issue first to discuss the
approach is appreciated.
