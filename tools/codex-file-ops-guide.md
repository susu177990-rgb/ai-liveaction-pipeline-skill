# Codex File Ops Guide

Use the bundled `scripts/` helpers as the default deterministic layer for:

- project scaffold creation
- video probing
- frame extraction
- frame index generation
- scene match sheet generation
- manifest validation
- QC compilation

Do not hide file operations in prose only. Whenever a stage can be made deterministic, prefer the script plus manifest path contract.
