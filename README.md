# Setup Notes → Checklist Generator

A small Python tool that converts CNC setup notes into a structured checklist (JSON).

## What it does
- Reads setup notes (from a text file or pasted into the terminal)
- Extracts:
  - job name (if present)
  - material (if present)
  - tools list (if a `Tools:` line exists)
  - setup steps / inspection items / risk points
- Outputs clean JSON that can plug into other workflows

## How to run

### Run with sample notes
~~~bash
python main.py sample_notes.txt
~~~
### Paste notes into the terminal
~~~bash
python main.py
~~~
Paste notes, then press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows).
