---
name: explain
description: Explain a topic or part of the repository simply for someone new to the codebase and save it as an HTML file, with inline SVG charts and diagrams. Use when the user types /explain <topic>.
---

# Explain
Break down the requested topic for someone seeing it for the first time using plain terms. Keep explanations clear, concise, grounded, and easy to read. Save the HTML file to ~/docs/
Add inline `<svg>` (no library, no JS) where a picture beats a paragraph — flow, architecture, before/after, real numbers from the repo. Skip it when prose already says it.

Topic: $ARGUMENTS
